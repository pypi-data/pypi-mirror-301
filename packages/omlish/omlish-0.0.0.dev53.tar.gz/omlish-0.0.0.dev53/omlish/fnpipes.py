import abc
import typing as ta


T = ta.TypeVar('T')
U = ta.TypeVar('U')


class Fn(abc.ABC, ta.Generic[T]):
    @abc.abstractmethod
    def __call__(self, *args: ta.Any, **kwargs: ta.Any) -> T:
        raise NotImplementedError

    def pipe(self, fn: ta.Callable[..., U], *args: ta.Any, **kwargs: ta.Any) -> 'Fn[U]':
        return Pipe([self], Bind(fn, *args, **kwargs))

    def __or__(self, fn: ta.Callable[..., U]) -> 'Fn[U]':
        return self.pipe(fn)

    def apply(self, fn: ta.Callable[[T], ta.Any], *args: ta.Any, **kwargs: ta.Any) -> 'Fn[T]':
        return Pipe([self], Apply(Bind(fn, *args, **kwargs)))

    def __and__(self, fn: ta.Callable[[T], ta.Any]) -> 'Fn[T]':
        return self.apply(fn)


class Bind(Fn[T]):
    def __init__(self, fn: ta.Callable[..., T], *args: ta.Any, **kwargs: ta.Any) -> None:
        super().__init__()
        if Ellipsis not in args and Ellipsis not in kwargs:
            args += (Ellipsis,)
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args: ta.Any, **kwargs: ta.Any) -> T:
        fa: list = []
        for a in self._args:
            if a is Ellipsis:
                fa.extend(args)
            else:
                fa.append(a)

        fkw = {}
        for k, v in self._kwargs.items():
            if v is Ellipsis:
                if len(args) != 1:
                    raise ValueError(args)
                fkw[k] = args[0]
            else:
                fkw[k] = v
        fkw.update(kwargs)

        return self._fn(*fa, **fkw)


class Pipe(Fn[T]):
    def __init__(self, lfns: ta.Sequence[ta.Callable], rfn: ta.Callable[..., T]) -> None:
        super().__init__()
        self._lfn, *self._rfns = [*lfns, rfn]

    def __call__(self, *args: ta.Any, **kwargs: ta.Any) -> T:
        o = self._lfn(*args, **kwargs)
        for fn in self._rfns:
            o = fn(o)
        return o


class Apply(Fn[T]):
    def __init__(self, *fns: ta.Callable[[T], ta.Any]) -> None:
        super().__init__()
        self._fns = fns

    def __call__(self, o: T) -> T:  # noqa
        for fn in self._fns:
            fn(o)
        return o


bind = Bind
pipe = Pipe
apply = Apply
