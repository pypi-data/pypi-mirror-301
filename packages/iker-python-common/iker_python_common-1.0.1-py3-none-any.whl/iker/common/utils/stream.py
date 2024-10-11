from typing import Any, Callable, Self, TypeVar, Union

from iker.common.utils.sequtils import grouped
from iker.common.utils.sequtils import head, init, last, tail

__all__ = [
    "Streaming",
    "stream",
]

T = TypeVar("T")
K = TypeVar("K")
U = TypeVar("U")
V = TypeVar("V")


class Streaming(object):
    def __init__(self, data: Union[list[Any], dict[Any, Any], Self]):
        if isinstance(data, Streaming):
            self.data = data.get()
        else:
            self.data = data
        if not self.is_list() and not self.is_dict():
            raise ValueError("unsupported type")

    def get(self):
        return self.data

    def count(self) -> int:
        return len(self.data)

    def is_list(self) -> bool:
        return isinstance(self.data, list)

    def is_dict(self) -> bool:
        return isinstance(self.data, dict)

    def to_list(self) -> Self:
        if self.is_list():
            return self
        else:
            return Streaming(list(self.data.items()))

    def to_dict(self) -> Self:
        if self.is_dict():
            return self
        else:
            return Streaming(dict(self.data))

    def map(self, func: Callable[[T], U]) -> Self:
        if self.is_list():
            return Streaming(list(map(func, self.data)))
        else:
            return self.to_list().map(func)

    def reduce(self, func: Callable[[T, T], T]) -> Self:
        if self.is_list():
            if len(self.data) <= 1:
                return self
            r = head(self.data)
            for x in tail(self.data):
                r = func(r, x)
            return Streaming([r])
        else:
            return self.to_list().reduce(func)

    def group(self, func: Callable[[T], K]) -> Self:
        if self.is_list():
            return Streaming(grouped(self.data, key_func=func))
        else:
            return self.to_list().group(func)

    def keys(self) -> Self:
        if self.is_dict():
            return Streaming(list(self.data.keys()))
        else:
            return self.to_dict().keys()

    def values(self) -> Self:
        if self.is_dict():
            return Streaming(list(self.data.values()))
        else:
            return self.to_dict().values()

    def map_values(self, func: Callable[[T], U]) -> Self:
        if self.is_dict():
            return Streaming(dict([(key, func(value)) for key, value in self.data.items()]))
        else:
            return self.to_dict().map_values(func)

    def flatten(self) -> Self:
        if self.is_dict():
            raise ValueError("unsupported method")
        data = []
        for d in self.data:
            data.extend(Streaming(d).to_list().get())
        return Streaming(data)

    def flat_map(self, func: Callable[[T], Union[list[U], dict[K, V], Self]]) -> Self:
        if self.is_list():
            data = []
            for d in self.data:
                data.extend(Streaming(func(d)).to_list().get())
            return Streaming(data)
        else:
            return self.to_list().flat_map(func)

    def group_map(self, group_func: Callable[[T], K], map_func: Callable[[T], U]) -> Self:
        if self.is_list():
            return Streaming(
                [
                    (key, list(map(map_func, values)))
                    for key, values in grouped(self.data, key_func=group_func)
                ]
            )
        else:
            return self.to_list().group_map(group_func, map_func)

    def filter(self, func: Callable[[T], bool]) -> Self:
        if self.is_list():
            return Streaming(list(filter(func, self.data)))
        else:
            return self.to_list().filter(func)

    def sort(self, func: Callable[[T], K]) -> Self:
        if self.is_list():
            return Streaming(list(sorted(self.data, key=func)))
        else:
            return self.to_list().filter(func)

    def head(self) -> Self:
        if self.is_list():
            return Streaming([head(self.data)])
        else:
            return self.to_list().head()

    def last(self) -> Self:
        if self.is_list():
            return Streaming([last(self.data)])
        else:
            return self.to_list().last()

    def init(self) -> Self:
        if self.is_list():
            return Streaming(init(self.data))
        else:
            return self.to_list().init()

    def tail(self) -> Self:
        if self.is_list():
            return Streaming(tail(self.data))
        else:
            return self.to_list().tail()

    def foreach(self, func: Callable[[T], None]) -> Self:
        if self.is_list():
            for x in self.data:
                func(x)
        else:
            self.to_list().foreach(func)
        return self

    def exists(self, func: Callable[[T], bool]) -> bool:
        if self.is_list():
            return any(map(func, self.data))
        else:
            return self.to_list().exists(func)

    def forall(self, func: Callable[[T], bool]) -> bool:
        if self.is_list():
            return all(map(func, self.data))
        else:
            return self.to_list().exists(func)

    def union(self, other: Self) -> Self:
        if self.is_list():
            return Streaming(list(set(self.to_list().get()).union(set(other.to_list().get()))))
        else:
            return self.to_list().union(other)

    def intersect(self, other: Self) -> Self:
        if self.is_list():
            return Streaming(list(set(self.to_list().get()).intersection(set(other.to_list().get()))))
        else:
            return self.to_list().intersect(other)


stream = Streaming
