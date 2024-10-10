import functools
import importlib
import time
import inspect

from typing import *
from enum import Enum
from collections import OrderedDict


__all__ = [
    'Stopwatch',
    'stopwatch',
    'enable_global_watch',
    'disable_global_watch',
    'watch_for',
    'GlobalWatch',
]


class TimeUnit(str, Enum):
    ns = 'ns'
    us = 'us'
    ms = 'ms'
    s = 's'
    m = 'm'
    h = 'h'


def emphasize(text: str):
    return f'\x1b[38;5;201;1m{text}\x1b[0m'


class Stopwatch:
    """计时器

    Args:
        unit: 计时单位
        sink: 耗时信息的输出函数，默认为 ``print``

    >>> watch = Stopwatch(unit='s', sink=print, msg_on_enter=False)
    >>> import time
    >>> with watch('[task - sleep]'):
    ...    time.sleep(0)
    [task - sleep] takes: 0.00s
    """
    __slots__ = (
        'runtimes', 'start_stack', 'rec_count', 'name',
        '_unit_repr', '_unit', '_sink', '_msg_on_enter',
        '_emphasize_threshold'
    )

    TIME_MAP = {
        'ns': 1,
        'us': 1_000,
        'ms': 1_000_000,
        's': 1_000_000_000,
        'm': 60_000_000_000,
        'h': 3_600_000_000_000,
    }

    def __init__(
        self,
        unit: str = 'ms',
        sink=print,
        msg_on_enter: bool = True,
        emphasize_threshold: Optional[float] = None  # in millseconds
    ):
        self.runtimes = OrderedDict()
        self.start_stack = []
        self.rec_count = 0
        self.name = []
        self._unit_repr = _unit = TimeUnit[unit].value
        self._unit = self.TIME_MAP[_unit]
        self._sink = sink
        self._msg_on_enter = msg_on_enter
        self._emphasize_threshold = emphasize_threshold

    def _write(self, content: str):
        try:
            self._sink(content)
        except:  # noqa
            print(content)

    def __call__(self, name=None):
        self.name.append(name)
        return self

    def __enter__(self):
        self.rec_count += 1
        if self._msg_on_enter:
            prefix, task_name = self.get_current_task_name(pop=False)
            self._write(f'{prefix}entering: {task_name}')

        self.start_stack.append(time.perf_counter_ns())

    def __exit__(self, exc_type, exc_val, exc_tb):
        time_gap = time.perf_counter_ns() - self.start_stack.pop(-1)
        key = ''.join(self.get_current_task_name())
        output = f"{key} takes: {time_gap / self._unit :.2f}{self._unit_repr}"
        if (
            self._emphasize_threshold is not None
            and time_gap / self.TIME_MAP['ms'] > self._emphasize_threshold
        ):
            output = emphasize(output)
        self._write(output)
        self.runtimes[key] = time_gap

    def get_current_task_name(self, pop=True):
        stack_len = len(self.start_stack)
        prefix = '\t' * stack_len

        if self.name and self.name[-1] is not None:
            if pop:
                name = self.name.pop(-1)
            else:
                name = self.name[-1]
        else:
            name = f"task{self.rec_count}"

        return prefix, name

    def get_all_runtime(self):
        return list(self.runtimes.values())

    def clear(self):
        self.runtimes.clear()
        self.rec_count = 0

    def __repr__(self):
        return ', '.join(
            f"{name}:{t / self._unit :.2f}{self._unit_repr}"
            for name, t in self.runtimes.items()
        )


def stopwatch(
    func: Callable = None,
    unit: TimeUnit = 'ms',
    name: Optional[str] = None,
    use_global: bool = True,
    is_coro: bool = False
):
    if func is None:
        return functools.partial(
            stopwatch, unit=unit, name=name, use_global=use_global, is_coro=is_coro)

    if use_global:
        watch = GlobalWatch
    else:
        watch = Stopwatch(unit)
    func_name = name or func.__qualname__

    if not (inspect.iscoroutinefunction(func) or is_coro):
        def wrap(*args, **kwargs):
            with watch(func_name):
                rtn = func(*args, **kwargs)
            return rtn
    else:
        async def wrap(*args, **kwargs):
            with watch(func_name):
                rtn = await func(*args, **kwargs)
            return rtn

    return functools.wraps(func)(wrap)


_CurrentWatch = _Watch = Stopwatch(unit='ms')


def disable_global_watch():
    global _CurrentWatch
    _CurrentWatch = None


def enable_global_watch(watch: Optional[Stopwatch] = None):
    global _CurrentWatch
    _CurrentWatch = watch or _Watch


class _StopWatchProxy:
    @staticmethod
    def set_sink(sink):
        _Watch._sink = sink

    @staticmethod
    def set_emphasize_threshold(thres: int):
        _Watch._emphasize_threshold = thres

    def __enter__(self):
        if _CurrentWatch is None:
            return
        return _CurrentWatch.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if _CurrentWatch is None:
            return
        return _CurrentWatch.__exit__(exc_type, exc_val, exc_tb)

    def __call__(self, name=None):
        if _CurrentWatch is not None:
            _CurrentWatch.__call__(name)
        return self


GlobalWatch = _StopWatchProxy()
_Watched = set()


def _set_watch_single(
    target,
    function: str,
    name_fn: Optional[Union[Callable[..., str], str]] = None
):
    if function not in target.__dict__:
        print(f"::WARN:: {target}.{function} not found.")
        return

    fn = target.__dict__[function]

    if isinstance(fn, (classmethod, staticmethod)):
        wrapper = type(fn)
        fn = fn.__func__
    else:
        wrapper = lambda x: x

    if fn in _Watched:
        return

    def resolve_fname(*args, **kwargs):
        if name_fn is None:
            name = fn.__qualname__
        elif isinstance(name_fn, str):
            name = name_fn.format(name=fn.__qualname__, args=args, kwargs=kwargs)
        else:
            name = name_fn(*args, **kwargs)
        return name

    if inspect.iscoroutinefunction(fn):
        async def new_fn(*args, **kwargs):
            name = resolve_fname(*args, **kwargs)
            with GlobalWatch(name):
                return await fn(*args, **kwargs)

    else:
        def new_fn(*args, **kwargs):
            name = resolve_fname(*args, **kwargs)
            with GlobalWatch(name):
                return fn(*args, **kwargs)

    new_fn = wrapper(new_fn)
    _Watched.update((fn, new_fn))
    setattr(target, function, new_fn)


def watch_for(
    function,
    name_fn: Optional[Union[Callable[..., str], str]] = None
):
    """指定需要计时的函数

    可以在不修改源代码的前提下为特定的函数增加计时。
    支持fuction, method, classmethod, staticmethod。
    """
    qualname = function.__qualname__.split('.', maxsplit=1)

    if len(qualname) == 2:
        clsname, funcname = qualname
        owner = function.__globals__[clsname]
    else:
        funcname = qualname[0]
        if not hasattr(function, '__globals__'):
            import builtins as owner
        else:
            owner = importlib.import_module(function.__globals__['__name__'])

    _set_watch_single(owner, funcname, name_fn)

