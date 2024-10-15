#!/usr/bin/env python3
# encoding: utf-8

__author__ = "ChenyangGao <https://chenyanggao.github.io>"
__version__ = (0, 0, 6)
__all__ = [
    "run_async", "as_thread", "ensure_async", "ensure_await", 
    "ensure_coroutine", "ensure_aiter", "async_map", "async_filter", 
    "async_reduce", "async_zip", "async_chain", 
    "async_all", "async_any", "call_as_aiter", "to_list", 
]

from asyncio import get_running_loop, new_event_loop, run, set_event_loop, to_thread
from collections.abc import Awaitable, AsyncIterable, AsyncIterator, Callable, Coroutine, Iterable, Iterator
from inspect import isawaitable, iscoroutine, iscoroutinefunction, isgenerator
from threading import Thread
from typing import cast, Any, ParamSpec, TypeVar

from decotools import decorated
from undefined import undefined


Args = ParamSpec("Args")
T = TypeVar("T")


def run_async(obj, /):
    try:
        get_running_loop()
        has_running_loop = True
    except RuntimeError:
        has_running_loop = False
    if isawaitable(obj):
        if has_running_loop:
            result = None
            def runner():
                nonlocal result
                loop = new_event_loop()
                set_event_loop(loop)
                result = loop.run_until_complete(ensure_coroutine(obj))
            t = Thread(target=runner)
            t.start()
            t.join()
            return result
        else:
            return run(ensure_coroutine(obj))
    else:
        return obj


@decorated
def as_thread(
    func: Callable[Args, T], 
    /, 
    *args: Args.args, 
    **kwds: Args.kwargs, 
) -> Awaitable[T]:
    def wrapfunc(*args, **kwds):
        try:
            return func(*args, **kwds)
        except StopIteration as e:
            raise StopAsyncIteration from e
    return to_thread(wrapfunc, *args, **kwds)


def ensure_async(
    func: Callable[Args, T | Awaitable[T]], 
    /, 
    threaded: bool = False, 
) -> Callable[Args, Awaitable[T]]:
    if iscoroutinefunction(func):
        return func
    func = cast(Callable[Args, T], func)
    if threaded:
        func = as_thread(func)
        async def wrapper(*args, **kwds):
            ret = await func(*args, **kwds)
            if isawaitable(ret):
                try:
                    return await ret
                except StopIteration as e:
                    raise StopAsyncIteration from e
            return ret
    else:
        async def wrapper(*args, **kwds):
            try:
                ret = func(*args, **kwds)
                if isawaitable(ret):
                    return await ret
                return ret
            except StopIteration as e:
                raise StopAsyncIteration from e
    return wrapper


def ensure_await(o, /) -> Awaitable:
    if isawaitable(o):
        return o
    async def wrapper():
        return o
    return wrapper()


def ensure_coroutine(o, /) -> Coroutine:
    if iscoroutine(o):
        return o
    async def wrapper():
        if isawaitable(o):
            return await o
        return o
    return wrapper()


def ensure_aiter(
    it: Iterable[T] | AsyncIterable[T], 
    /, 
    threaded: bool = False, 
) -> AsyncIterator[T]:
    if isinstance(it, AsyncIterable):
        return aiter(it)
    if isgenerator(it):
        if threaded:
            send = as_thread(it.send)
            async def wrapper():
                e: Any = None
                try:
                    while True:
                        e = yield await send(e)
                except StopAsyncIteration:
                    pass
        else:
            send = it.send
            async def wrapper():
                e: Any = None
                try:
                    while True:
                        e = yield send(e)
                except StopIteration:
                    pass
    else:
        if threaded:
            get = as_thread(iter(it).__next__)
            async def wrapper():
                try:
                    while True:
                        yield await get()
                except StopAsyncIteration:
                    pass
        else:
            async def wrapper():
                for e in it:
                    yield e
    return wrapper()


async def async_map(
    func: Callable[..., T], 
    iterable: Iterable | AsyncIterable, 
    /, 
    *iterables: Iterable | AsyncIterable, 
    threaded: bool = False, 
) -> AsyncIterator[T]:
    fn = ensure_async(func, threaded=threaded)
    if iterables:
        async for args in async_zip(iterable, *iterables, threaded=threaded):
            yield await fn(*args)
    else:
        async for arg in ensure_aiter(iterable, threaded=threaded):
            yield await fn(arg)


async def async_filter(
    func: None | Callable[[T], bool], 
    iterable: Iterable[T] | AsyncIterable[T], 
    /, 
    threaded: bool = False, 
) -> AsyncIterator[T]:
    if func is None or func is bool:
        async for arg in ensure_aiter(iterable, threaded=threaded):
            if arg:
                yield arg
    else:
        fn = ensure_async(func, threaded=threaded)
        async for arg in ensure_aiter(iterable, threaded=threaded):
            if await fn(arg):
                yield arg


async def async_reduce(
    func: Callable, 
    iterable, 
    initial=undefined, 
    /, 
    threaded: bool = False, 
) -> AsyncIterator:
    ait = ensure_aiter(iterable, threaded=threaded)
    if initial is undefined:
        try:
            initial = await ait.__anext__()
        except StopAsyncIteration:
            raise TypeError("reduce() of empty iterable with no initial value")
    func = ensure_async(func, threaded=threaded)
    prev = initial
    async for arg in ait:
        prev = await func(prev, arg)
    return prev


async def async_zip(
    iterable, 
    /, 
    *iterables, 
    threaded: bool = False, 
) -> AsyncIterator:
    iterable = ensure_aiter(iterable, threaded=threaded)
    if iterables:
        fs = (iterable.__anext__, *(ensure_aiter(it, threaded=threaded).__anext__ for it in iterables))
        try:
            while True:
                yield tuple([await f() for f in fs])
        except StopAsyncIteration:
            pass
    else:
        async for e in iterable:
            yield e


async def async_chain(
    *iterables, 
    threaded: bool = False, 
) -> AsyncIterator:
    for it in iterables:
        async for e in ensure_aiter(it, threaded=threaded):
            yield e


async def async_chain_from_iterable(
    iterable, 
    /, 
    threaded: bool = False, 
) -> AsyncIterator:
    async for it in ensure_aiter(iterable, threaded=False):
        async for e in ensure_aiter(it, threaded=threaded):
            yield e

setattr(async_chain, "from_iterable", async_chain_from_iterable)


async def async_all(
    iterable, 
    /, 
    threaded: bool = False, 
) -> bool:
    async for e in ensure_aiter(iterable, threaded=threaded):
        if not e:
            return False
    return True


async def async_any(
    iterable, 
    /, 
    threaded: bool = False, 
) -> bool:
    async for e in ensure_aiter(iterable, threaded=threaded):
        if e:
            return True
    return False


async def call_as_aiter(
    func: Callable[[], T] | Callable[[], Awaitable[T]], 
    /, 
    sentinel = undefined, 
    threaded: bool = False, 
) -> AsyncIterator[T]:
    func = ensure_async(func, threaded=threaded)
    try:
        if sentinel is undefined:
            while True:
                yield await func()
        elif callable(sentinel):
            sentinel = ensure_async(sentinel)
            while not (await sentinel(r := await func())):
                yield r
        else:
            check = lambda r, /: r is not sentinel and r != sentinel
            while check(r := await func()):
                yield r
    except (StopIteration, StopAsyncIteration):
        pass


async def to_list(
    it: Iterable[T] | AsyncIterable[T], 
    /, 
    threaded: bool = False, 
) -> list[T]:
    return [e async for e in ensure_aiter(it, threaded=threaded)]

