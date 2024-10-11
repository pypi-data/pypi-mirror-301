from __future__ import annotations

import enum
import functools
import itertools
from typing import Callable, Generator, Iterable, Sequence, TypeVar

__all__ = [
    "head",
    "head_or_none",
    "last",
    "last_or_none",
    "tail",
    "init",
    "grouped",
    "deduped",
    "batch_yield",
    "chunk",
    "chunk_between",
    "chunk_with_key",
    "merge_chunks",
    "IntervalRelation",
    "interval_relation",
    "intervals_union",
    "intervals_intersect",
    "intervals_subtract",
]

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


# See Haskell's list operations head, tail, init, and last
# which is also provided in Scala list operations

def head(ms: Sequence[T]) -> T:
    return ms[0]


def head_or_none(ms: Sequence[T]) -> T | None:
    if len(ms) > 0:
        return ms[0]
    return None


def last(ms: Sequence[T]) -> T:
    return ms[-1]


def last_or_none(ms: Sequence[T]) -> T | None:
    if len(ms) > 0:
        return ms[-1]
    return None


def tail(ms: Sequence[T]) -> Sequence[T]:
    return ms[1:]


def init(ms: Sequence[T]) -> Sequence[T]:
    return ms[:-1]


def grouped(
    ms: Sequence[T],
    key_func: Callable[[T], K],
    values_only: bool = False,
) -> list[tuple[K, list[T]]] | list[list[T]]:
    """
    Groups the given list of elements according to key generator function

    :param ms: list of elements
    :param key_func: key generator function
    :param values_only: True if only return elements groups without corresponding keys
    :return: grouped elements, with corresponding keys if `values_only` is set to False
    """
    if ms is None or len(ms) == 0:
        return []
    grouped_ms: dict[K, list[T]] = {}
    for m in ms:
        k = key_func(m)
        grouped_ms.setdefault(k, []).append(m)
    if values_only:
        return [d for _, d in grouped_ms.items()]
    else:
        return [(k, d) for k, d in grouped_ms.items()]


def deduped(ms: Sequence[T], comp_func: Callable[[T, T], bool]) -> list[T]:
    """
    Dedupes the given list of elements

    :param ms: list of elements
    :param comp_func: comparator generator function
    :return: deduped elements
    """
    if ms is None or len(ms) == 0:
        return []
    deduped_ms: list[T] = [head(ms)]
    for m in tail(ms):
        if not comp_func(last(deduped_ms), m):
            deduped_ms.append(m)
    return deduped_ms


def batch_yield(ms: Iterable[T], batch_size: int) -> Generator[list[T]]:
    """
    Splits the given input sequence into batches according to the specific batch size

    :param ms: sequence of elements
    :param batch_size: batch size
    :return: batches of sequences
    """
    if batch_size < 1:
        raise ValueError("illegal batch size")
    batch: list[T] = []
    for m in ms:
        batch.append(m)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch


def chunk(ms: Sequence[T], chunk_func: Callable[[Sequence[T], T], bool], exclusive_end: bool = False) -> list[list[T]]:
    """
    Chops the list of elements into chunks

    :param ms: list of elements
    :param chunk_func: chunk generator function with compares the current chunk and the next element from the list
    :param exclusive_end: set to true to make each chunk (except the last one) carrying the first element of
    the next chunk as an exclusive end
    :return: list of element chunks
    """
    if ms is None or len(ms) == 0:
        return []
    chunks: list[list[T]] = [[head(ms)]]
    for m in tail(ms):
        if chunk_func(last(chunks), m):
            if exclusive_end:
                last(chunks).append(m)
            chunks.append([m])
        else:
            last(chunks).append(m)
    return chunks


def chunk_between(ms: Sequence[T], chunk_func: Callable[[T, T], bool], exclusive_end: bool = False) -> list[list[T]]:
    return chunk(ms, lambda x, y: chunk_func(last(x), y), exclusive_end)


def chunk_with_key(ms: Sequence[T], key_func: Callable[[T], K], exclusive_end: bool = False) -> list[list[T]]:
    return chunk_between(ms, lambda x, y: key_func(x) != key_func(y), exclusive_end)


def merge_chunks(
    chunks: Sequence[Sequence[T]],
    merge_func: Callable[[Sequence[T], Sequence[T]], bool],
    drop_exclusive_end: bool = False,
) -> list[list[T]]:
    """
    Merges chunks according to the given merging criteria

    :param chunks: chunks to be merged into larger ones
    :param merge_func: merged chunk generator function
    :param drop_exclusive_end: set to true if each of the given chunk (except the last one) as an exclusive end element,
    and these exclusive end elements will be dropped while merging their chunks to the corresponding next chunks
    :return: merged chunks
    """
    if chunks is None or len(chunks) == 0:
        return []

    merged_chunks: list[list[T]] = []

    def stateful_reducer(a: Sequence[T], b: Sequence[T]) -> Sequence[T]:
        if merge_func(a, b):
            if drop_exclusive_end:
                return list(itertools.chain(init(a), b))
            return list(itertools.chain(a, b))
        else:
            merged_chunks.append(list(a))
            return b

    last_chunk = functools.reduce(stateful_reducer, chunks)
    merged_chunks.append(list(last_chunk))
    return merged_chunks


class IntervalRelation(enum.IntEnum):
    LeftIn = 0x1
    RightIn = 0x2
    LeftLeftOut = 0x10
    LeftLeftOn = 0x20
    LeftRightOn = 0x40
    LeftRightOut = 0x80
    RightLeftOut = 0x100
    RightLeftOn = 0x200
    RightRightOn = 0x400
    RightRightOut = 0x800

    LeftDetach = LeftLeftOut | RightLeftOut
    LeftTouch = LeftLeftOut | RightLeftOn
    LeftOverlap = LeftLeftOut | RightIn
    LeftOn = LeftLeftOn | RightLeftOn
    LeftAlignOverlay = LeftLeftOn | RightIn
    LeftAlignCover = LeftLeftOn | RightRightOut
    Overlay = LeftIn | RightIn
    Cover = LeftLeftOut | RightRightOut
    Identical = LeftLeftOn | RightRightOn
    RightAlignOverlay = LeftIn | RightRightOn
    RightAlignCover = LeftLeftOut | RightRightOn
    RightOn = LeftRightOn | RightRightOn
    RightOverlap = LeftIn | RightRightOut
    RightTouch = LeftRightOn | RightRightOut
    RightDetach = LeftRightOut | RightRightOut


def interval_relation(a: tuple[float, float], b: tuple[float, float]) -> int:
    (a0, a1), (b0, b1) = a, b
    rel = 0
    if a0 < b0:
        rel |= IntervalRelation.LeftLeftOut
    elif a0 == b0:
        rel |= IntervalRelation.LeftLeftOn
    elif b0 < a0 < b1:
        rel |= IntervalRelation.LeftIn
    elif a0 == b1:
        rel |= IntervalRelation.LeftRightOn
    elif a0 > b1:
        rel |= IntervalRelation.LeftRightOut
    if a1 > b1:
        rel |= IntervalRelation.RightRightOut
    elif a1 == b1:
        rel |= IntervalRelation.RightRightOn
    elif b0 < a1 < b1:
        rel |= IntervalRelation.RightIn
    elif a1 == b0:
        rel |= IntervalRelation.RightLeftOn
    elif a1 < b0:
        rel |= IntervalRelation.RightLeftOut
    return rel


def intervals_union(a: Sequence[tuple[T, T]], *bs: Sequence[tuple[T, T]]) -> list[tuple[T, T]]:
    """
    Computes the union of the given interval lists. The intervals in each of the lists must be sorted and do not
    mutually overlap

    :param a: the first interval list
    :param bs: the remaining interval lists
    :return: union of the interval lists whose intervals are sorted
    """

    def union(xs: Sequence[tuple[T, T]], ys: Sequence[tuple[T, T]]) -> list[tuple[T, T]]:
        if not xs or not ys:
            return list(itertools.chain(xs, ys))

        result: list[tuple[T, T]] = []

        i, j = 0, 0
        x0_lo, _ = xs[i]
        y0_lo, _ = ys[j]
        lo = hi = min(x0_lo, y0_lo)
        while i < len(xs) or j < len(ys):
            if i < len(xs) and j < len(ys):
                x_lo, _ = xs[i]
                y_lo, _ = ys[j]
                if x_lo < y_lo:
                    curr = xs[i]
                    i += 1
                else:
                    curr = ys[j]
                    j += 1
            elif i == len(xs):
                curr = ys[j]
                j += 1
            else:
                curr = xs[i]
                i += 1

            curr_lo, curr_hi = curr

            if hi < curr_lo:
                result.append((lo, hi))
                lo, hi = curr
            else:
                hi = max(hi, curr_hi)

        result.append((lo, hi))

        return result

    for b in bs:
        a = union(a, b)
    return a


def intervals_intersect(a: Sequence[tuple[T, T]], *bs: Sequence[tuple[T, T]]) -> list[tuple[T, T]]:
    """
    Computes the intersection of the given interval lists. The intervals in each of the lists must be sorted and do not
    mutually overlap

    :param a: the first interval list
    :param bs: the remaining interval lists
    :return: intersection of the interval lists whose intervals are sorted
    """

    def intersect(xs: Sequence[tuple[T, T]], ys: Sequence[tuple[T, T]]) -> list[tuple[T, T]]:
        if not xs or not ys:
            return []

        result: list[tuple[T, T]] = []

        i, j = 0, 0
        while i < len(xs) and j < len(ys):
            x_lo, x_hi = xs[i]
            y_lo, y_hi = ys[j]
            lo = max(x_lo, y_lo)
            hi = min(x_hi, y_hi)

            if not hi < lo:
                result.append((lo, hi))

            if x_hi < y_hi:
                i += 1
            else:
                j += 1

        return result

    for b in bs:
        a = intersect(a, b)
    return a


def intervals_subtract(a: Sequence[tuple[T, T]], *bs: Sequence[tuple[T, T]]) -> list[tuple[T, T]]:
    """
    Computes the subtraction on the first interval list by the remaining interval lists. The intervals in each of the
    lists must be sorted and do not mutually overlap

    :param a: the first interval list
    :param bs: the remaining interval lists
    :return: subtraction on the first interval list by the remaining interval lists whose intervals are sorted
    """

    def subtract(xs: Sequence[tuple[T, T]], ys: Sequence[tuple[T, T]]) -> list[tuple[T, T]]:
        if not xs or not ys:
            return list(xs)

        result: list[tuple[T, T]] = []

        i, j = 0, 0
        curr = xs[i]
        while j < len(ys):
            curr_lo, curr_hi = curr
            y_lo, y_hi = ys[j]
            lo = max(curr_lo, y_lo)
            hi = min(curr_hi, y_hi)

            if not lo > hi:
                if curr_lo < lo:
                    result.append((curr_lo, lo))
                if hi < curr_hi:
                    curr = hi, curr_hi
                else:
                    curr = None
            elif curr_hi < y_lo:
                result.append(curr)
                curr = None

            if curr is None:
                i += 1
                if i < len(xs):
                    curr = xs[i]
                else:
                    break
            else:
                j += 1

        if curr is not None:
            result.append(curr)

        i += 1
        while i < len(xs):
            result.append(xs[i])
            i += 1

        return result

    for b in bs:
        a = subtract(a, b)
    return a
