from logging import Logger
from pathlib import Path
import functools
import re

from ..compat import Callable, Any
from .interface import DataPath, Data, ActionContext, Action
from .drivers import Driver


class Log(Action):
    def __init__(
        self,
        log_func: Callable[[Logger,Data],None],
        summary: bool = False
    ):
        self._log_func = log_func
        self._summary = summary

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            logger = context.summary if self._summary else context.logger
            self._log_func(logger, input)
        except Exception as e:
            context.logger.error(f"Failed to log message: {e}")
        return input


class Apply(Action):
    def __init__(self, func: Callable[[Data],Data]):
        self._func = func

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            return self._func(input)
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")


class Source(Action):
    def __init__(self, driver: Driver, cwdir: Path):
        self._driver = driver
        self._cwdir = cwdir

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            paths = self._driver.source(self._cwdir)
            result = Data.homogenous(self._driver, self._cwdir, paths)
            context.logger.debug(f"Sourced files: {[str(path) for path in paths]}")
            return input.merge(result)
        except Exception as e:
            context.logger.error(f"Failed to list files: {e}")
            return input


class Filter(Action):
    def __init__(self, predicates: list[Any]):
        self._predicates = predicates

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            return input.filter(_predicate_any(self._predicates, context.selector))
        except Exception as e:
            context.logger.error(f"Failed to filter files: {e}")
            return Data.empty()


class Switch(Action):
    def __init__(self, cases: list[Any,Action]):
        self._cases = cases

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            predicates = []
            actions = []
            for predicate, action in self._cases:
                prepared_predicate = _prepare_predicate(predicate, context.selector)
                if prepared_predicate is not None:
                    predicates.append(prepared_predicate)
                    actions.append(action)

            return Data.join([
                action.execute(data, context)
                for action, data in zip(actions, input.split(*predicates))
            ])
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")
            return Data.empty()


class Branch(Action):
    def __init__(self, predicate: Any, action: Action):
        self._predicate = predicate
        self._action = action

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            prepared_predicate = _prepare_predicate(self._predicate, context.selector)
            succ, fail = input.ifelse(prepared_predicate)
            result = self._action.execute(succ, context)
            return result.merge(fail)
        except Exception as e:
            context.logger.error(f"Unexpected error: {e}")
            return Data.empty()


class Collect(Action):
    def __init__(self, name: str, consume: bool = False):
        self._name = name
        self._consume = consume

    def execute(self, input: Data, context: ActionContext) -> Data:
        try:
            if self._consume:
                return input.consume(self._name)
            else:
                return input.collect(self._name)
        except Exception as e:
            context.logger.error(f"Failed to collect files: {e}")
            return input


class FileOp(Action):
    def __init__(self,
        driver: Driver,
        outdir: Path,
        names: tuple[str,str,str],
        dst_func: Callable[[DataPath],Path],
        put_func: Callable[[Driver,DataPath,Path],list[DataPath]],
        cd: bool = False
    ):
        self._driver = driver
        self._outdir = outdir
        self._noun, self._verb, self._past = names
        self._dst_func = dst_func
        self._put_func = put_func
        self._cd = cd

    def execute(self, input: Data, context: ActionContext) -> Data:
        result_paths = []
        failures = 0
        for src in input:
            dst = None
            try:
                dst = DataPath(
                    driver = self._driver if self._driver is not None else src.driver(),
                    cwdir = self._outdir if self._cd else src.cwdir(),
                    path = self._outdir.joinpath(self._dst_func(src)),
                    name = src.name()
                )
            except Exception as e:
                context.logger.error(f"Unexpected error: {e}")
                continue
            try:
                context.logger.info(f"{self._verb} {src}")
                dst_paths = self._put_func(src, dst)
                if len(dst_paths) == 0:
                    dst_paths = [dst]
                head, tail = dst_paths[0], dst_paths[1:]
                context.logger.info(f"{' ' * (len(self._verb) - 3)} to {head}")
                for path in tail:
                    context.logger.info(f"{' ' * len(self._verb)} {path}")

                result_paths.extend(dst_paths)
            except Exception as e:
                context.logger.error(f"Failed to {self._noun} {src.path()}")
                context.logger.error(f"{' ' * (len(self._noun) + 7)} to {dst}")
                context.logger.error(str(e))
                failures += 1

        if failures > 0:
            context.summary.error(f"Failed to {self._noun} {failures}/{input.len()} files.")
        return input.with_paths(result_paths)


class StatefulAction(Action):
    def __init__(self, action: Action, context: ActionContext):
        self._action = action
        self._context = context

    def execute(self, input: Data, context: ActionContext) -> Data:
        if self._context is None:
            return self._action(input, context)
        else:
            return self._action(input, self._context)


def basic_dst_func(path: DataPath) -> Path:
    return path.name()


def basic_put_func(src: DataPath, dst: DataPath) -> list[DataPath]:
    data = src.get()
    return [dst.put(data)]


def move_put_func(src: DataPath, dst: DataPath) -> list[DataPath]:
    src._driver.move(src.path(), dst.path())
    return [dst]


def unpack_put_func(src: DataPath, dst: DataPath) -> list[DataPath]:
    unpacked_paths = src.driver().unpack(src.path(), dst.path())
    return [
        DataPath(
            driver = src.driver(),
            cwdir = src.cwdir(),
            path = path,
            name = path.relative_to(dst.path().parent)
        )
        for path in unpacked_paths
    ]


def _prepare_predicate(
    predicate: Any,
    selector: Callable[[Path],Any]|None = None
) -> Callable[[DataPath],bool]|None:
    try:
        if callable(predicate):
            return lambda data_path: predicate(data_path.path())
        if isinstance(predicate, str):
            if predicate == "":
                return lambda path: False
            invert = False
            if predicate[0] == "!":
                invert = True
                predicate = predicate[1:]
            return functools.partial(
                lambda path, regex: invert ^ (regex.fullmatch(str(path.path())) is not None),
                regex = re.compile(predicate.replace(".", "\\.").replace("*", ".*"))
            )
        if selector is not None:
            return functools.partial(
                lambda path, kind, sel: sel(path.path()) == kind,
                kind = predicate,
                sel = selector
            )
    except Exception:
        pass
    return None


def _predicate_any(
    predicates: list[Any],
    selector: Callable[[Path],Any]|None = None
) -> Callable[[DataPath],bool]:
    prepared_predicates = []
    for predicate in predicates:
        prepared_predicate = _prepare_predicate(predicate, selector)
        if prepared_predicate is not None:
            prepared_predicates.append(prepared_predicate)

    return functools.partial(
        lambda path, ps: any([predicate(path) for predicate in ps]),
        ps = prepared_predicates
    )
