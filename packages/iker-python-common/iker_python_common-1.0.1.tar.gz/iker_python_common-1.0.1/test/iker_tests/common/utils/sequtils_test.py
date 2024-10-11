import random
import unittest

import ddt

from iker.common.utils.sequtils import IntervalRelation
from iker.common.utils.sequtils import batch_yield
from iker.common.utils.sequtils import chunk, chunk_between, chunk_with_key, merge_chunks
from iker.common.utils.sequtils import deduped, grouped
from iker.common.utils.sequtils import head, init, last, tail
from iker.common.utils.sequtils import interval_relation, intervals_intersect, intervals_subtract, intervals_union


@ddt.ddt
class SeqUtilsTest(unittest.TestCase):

    @ddt.data(([1], 1), ([1, 2], 1))
    @ddt.unpack
    def test_head(self, data, expect):
        self.assertEqual(expect, head(data))

    def test_head__empty(self):
        self.assertRaises(Exception, head, [])

    def test_head__none(self):
        self.assertRaises(Exception, head, None)

    @ddt.data(([1], 1), ([1, 2], 2))
    @ddt.unpack
    def test_last(self, data, expect):
        self.assertEqual(expect, last(data))

    def test_last__empty(self):
        self.assertRaises(Exception, last, [])

    def test_last__none(self):
        self.assertRaises(Exception, last, None)

    @ddt.data(([1], []), ([1, 2], [1]), ([1, 2, 3], [1, 2]))
    @ddt.unpack
    def test_init(self, data, expect):
        self.assertEqual(expect, init(data))

    def test_init__empty(self):
        self.assertEqual([], init([]))

    def test_init__none(self):
        self.assertRaises(Exception, init, None)

    @ddt.data(([1], []), ([1, 2], [2]), ([1, 2, 3], [2, 3]))
    @ddt.unpack
    def test_tail(self, data, expect):
        self.assertEqual(expect, tail(data))

    def test_tail__empty(self):
        self.assertEqual([], tail([]))

    def test_tail__none(self):
        self.assertRaises(Exception, tail, None)

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: x, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                (0, [0]),
                (1, [1]),
                (2, [2]),
                (3, [3]),
                (4, [4]),
                (5, [5]),
                (6, [6]),
                (7, [7]),
                (8, [8]),
                (9, [9]),
                (10, [10]),
                (11, [11]),
                (12, [12]),
                (13, [13]),
                (14, [14]),
                (15, [15]),
                (16, [16]),
                (17, [17]),
                (18, [18]),
                (19, [19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 5,
            [
                (0, [0, 5, 10, 15]),
                (1, [1, 6, 11, 16]),
                (2, [2, 7, 12, 17]),
                (3, [3, 8, 13, 18]),
                (4, [4, 9, 14, 19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 2,
            [
                (0, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]),
                (1, [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]),
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: None,
            [(None, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])],
        ),
        (
            [[0] * 5, [1] * 5, [2] * 4, [3] * 4, [4] * 3, [5] * 3],
            lambda x: len(x),
            [
                (5, [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]]),
                (4, [[2, 2, 2, 2], [3, 3, 3, 3]]),
                (3, [[4, 4, 4], [5, 5, 5]]),
            ],
        ),
    )
    @ddt.unpack
    def test_grouped(self, data, key_func, expect):
        self.assertEqual(expect, grouped(data, key_func=key_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: x, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 5,
            [
                [0, 5, 10, 15],
                [1, 6, 11, 16],
                [2, 7, 12, 17],
                [3, 8, 13, 18],
                [4, 9, 14, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x % 2,
            [
                [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
                [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: None,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [[0] * 5, [1] * 5, [2] * 4, [3] * 4, [4] * 3, [5] * 3],
            lambda x: len(x),
            [
                [[0, 0, 0, 0, 0], [1, 1, 1, 1, 1]],
                [[2, 2, 2, 2], [3, 3, 3, 3]],
                [[4, 4, 4], [5, 5, 5]],
            ],
        ),
    )
    @ddt.unpack
    def test_grouped__values_only(self, data, key_func, expect):
        self.assertEqual(expect, grouped(data, key_func=key_func, values_only=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: x == y, []),
        ([0, 0, 0, 0, 0], lambda x, y: x == y, [0]),
        ([None, None, None], lambda x, y: x == y, [None]),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x == y,
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        ),
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0],
            lambda x, y: x == y,
            [0, 1, 2, 3, 4, 3, 2, 1, 0],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) < 2,
            [0, 2, 4, 6, 8, 10, 12, 14, 16, 18],
        ),
    )
    @ddt.unpack
    def test_deduped(self, data, comp_func, expect):
        self.assertEqual(expect, deduped(data, comp_func=comp_func))

    @ddt.data(
        ([], 1, []),
        ([1], 1, [[1]]),
        ([1], 2, [[1]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3, 4, 5, 6], 2, [[1, 2], [3, 4], [5, 6]]),
        ([1, 2, 3, 4, 5, 6], 3, [[1, 2, 3], [4, 5, 6]]),
        ([[1, 2, 3], [4, 5, 6]], 1, [[[1, 2, 3]], [[4, 5, 6]]]),
        ([[1, 2, 3], [4, 5, 6]], 2, [[[1, 2, 3], [4, 5, 6]]]),
    )
    @ddt.unpack
    def test_batch_yield(self, data, batch_size, expect):
        self.assertEqual(expect, list(batch_yield(data, batch_size)))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(head(x) - y) > 4,
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(last(x) - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 0,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 1,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk(data, chunk_func=chunk_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(head(x) - y) > 4,
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(last(x) - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 0,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: last(x) % 2 == 1,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk__exclusive_end(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk(data, chunk_func=chunk_func, exclusive_end=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 0,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 1,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_between(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk_between(data, chunk_func=chunk_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: True,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: abs(x - y) > 1,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 0,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x, y: x % 2 == 1,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_between__exclusive_end(self, data, chunk_func, expect):
        self.assertEqual(expect, chunk_between(data, chunk_func=chunk_func, exclusive_end=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: (x + 1) // 2,
            [
                [0],
                [1, 2],
                [3, 4],
                [5, 6],
                [7, 8],
                [9, 10],
                [11, 12],
                [13, 14],
                [15, 16],
                [17, 18],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x // 2,
            [
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9],
                [10, 11],
                [12, 13],
                [14, 15],
                [16, 17],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_with_key(self, data, key_func, expect):
        self.assertEqual(expect, chunk_with_key(data, key_func=key_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x: True, []),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x,
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: (x + 1) // 2,
            [
                [0, 1],
                [1, 2, 3],
                [3, 4, 5],
                [5, 6, 7],
                [7, 8, 9],
                [9, 10, 11],
                [11, 12, 13],
                [13, 14, 15],
                [15, 16, 17],
                [17, 18, 19],
                [19],
            ],
        ),
        (
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            lambda x: x // 2,
            [
                [0, 1, 2],
                [2, 3, 4],
                [4, 5, 6],
                [6, 7, 8],
                [8, 9, 10],
                [10, 11, 12],
                [12, 13, 14],
                [14, 15, 16],
                [16, 17, 18],
                [18, 19],
            ],
        ),
    )
    @ddt.unpack
    def test_chunk_with_key__exclusive_key(self, data, key_func, expect):
        self.assertEqual(expect, chunk_with_key(data, key_func=key_func, exclusive_end=True))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [
                [0],
                [1],
                [2],
                [3],
                [4],
                [5],
                [6],
                [7],
                [8],
                [9],
                [10],
                [11],
                [12],
                [13],
                [14],
                [15],
                [16],
                [17],
                [18],
                [19],
            ],
            lambda x, y: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: abs(head(x) - head(y)) < 10,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4],
                [5, 6, 7, 8, 9],
                [10, 11, 12, 13, 14],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: last(x) % 10 == 4,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
    )
    @ddt.unpack
    def test_merge_chunks(self, data, merge_func, expect):
        self.assertEqual(expect, merge_chunks(data, merge_func=merge_func))

    @ddt.data(
        (None, lambda x: x, []),
        ([], lambda x, y: True, []),
        (
            [
                [0, 1],
                [1, 2],
                [2, 3],
                [3, 4],
                [4, 5],
                [5, 6],
                [6, 7],
                [7, 8],
                [8, 9],
                [9, 10],
                [10, 11],
                [11, 12],
                [12, 13],
                [13, 14],
                [14, 15],
                [15, 16],
                [16, 17],
                [17, 18],
                [18, 19],
                [19],
            ],
            lambda x, y: True,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: abs(head(x) - head(y)) < 10,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
        (
            [
                [0, 1, 2, 3, 4, 5],
                [5, 6, 7, 8, 9, 10],
                [10, 11, 12, 13, 14, 15],
                [15, 16, 17, 18, 19],
            ],
            lambda x, y: last(init(x)) % 10 == 4,
            [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]],
        ),
    )
    @ddt.unpack
    def test_merge_chunks__drop_exclusive_end(self, data, merge_func, expect):
        self.assertEqual(expect, merge_chunks(data, merge_func=merge_func, drop_exclusive_end=True))

    @ddt.data(
        ((-2, 2), (-5, -3), IntervalRelation.LeftDetach),
        ((-2, 2), (-5, -2), IntervalRelation.LeftTouch),
        ((-2, 2), (-5, 0), IntervalRelation.LeftOverlap),
        ((-2, 2), (-2, 0), IntervalRelation.LeftAlignOverlay),
        ((-2, 2), (-2, 3), IntervalRelation.LeftAlignCover),
        ((-2, 2), (-1, 1), IntervalRelation.Overlay),
        ((-2, 2), (-2, 2), IntervalRelation.Identical),
        ((-2, 2), (-3, 3), IntervalRelation.Cover),
        ((-2, 2), (-3, 2), IntervalRelation.RightAlignCover),
        ((-2, 2), (0, 2), IntervalRelation.RightAlignOverlay),
        ((-2, 2), (0, 5), IntervalRelation.RightOverlap),
        ((-2, 2), (2, 5), IntervalRelation.RightTouch),
        ((-2, 2), (3, 5), IntervalRelation.RightDetach),
        ((-2, 2), (-5, -5), IntervalRelation.LeftDetach),
        ((-2, 2), (-2, -2), IntervalRelation.LeftOn),
        ((-2, 2), (0, 0), IntervalRelation.Overlay),
        ((-2, 2), (2, 2), IntervalRelation.RightOn),
        ((-2, 2), (5, 5), IntervalRelation.RightDetach),
        ((0, 0), (-5, -5), IntervalRelation.LeftDetach),
        ((0, 0), (0, 0), IntervalRelation.Identical),
        ((0, 0), (5, 5), IntervalRelation.RightDetach),
        ((0, 0), (-5, -2), IntervalRelation.LeftDetach),
        ((0, 0), (-5, 0), IntervalRelation.RightAlignCover),
        ((0, 0), (-2, 2), IntervalRelation.Cover),
        ((0, 0), (0, 5), IntervalRelation.LeftAlignCover),
        ((0, 0), (2, 5), IntervalRelation.RightDetach),
    )
    @ddt.unpack
    def test_interval_relation(self, b, a, expect):
        self.assertEqual(expect, interval_relation(a, b))

    @ddt.data(
        ([], [], []),
        ([(-2, 2)], [], [(-2, 2)]),
        ([(-2, 2)], [(3, 5)], [(-2, 2), (3, 5)]),
        ([(-2, 2)], [(-5, -3)], [(-5, -3), (-2, 2)]),
        ([(-2, 2)], [(2, 5)], [(-2, 5)]),
        ([(-2, 2)], [(-5, -2)], [(-5, 2)]),
        ([(-2, 2)], [(0, 4)], [(-2, 4)]),
        ([(-2, 2)], [(-4, 0)], [(-4, 2)]),
        ([(-2, 2)], [(-4, 4)], [(-4, 4)]),
        ([(-2, 2)], [(-2, 2)], [(-2, 2)]),
        ([(-2, 2)], [(-1, 1)], [(-2, 2)]),
        ([(-2, 2)], [(0, 2)], [(-2, 2)]),
        ([(-2, 2)], [(-2, 0)], [(-2, 2)]),
        ([(-2, 2)], [(2, 2)], [(-2, 2)]),
        ([(-2, 2)], [(-2, -2)], [(-2, 2)]),
        ([(-2, 2)], [(0, 0)], [(-2, 2)]),
        ([(-10, 10)], [(-8, -4), (-2, 2), (4, 8)], [(-10, 10)]),
        ([(-10, 10)], [(-10, -6), (-2, 2), (6, 10)], [(-10, 10)]),
        ([(-10, 10)], [(-12, -8), (-2, 2), (8, 12)], [(-12, 12)]),
        ([(-10, 10)], [(-12, -10), (-2, 2), (10, 12)], [(-12, 12)]),
        ([(-10, 10)], [(-16, -12), (-2, 2), (12, 16)], [(-16, -12), (-10, 10), (12, 16)]),
        ([(-10, 10)], [(-16, -12), (-11, 11), (12, 16)], [(-16, -12), (-11, 11), (12, 16)]),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-5, -3), (3, 5)],
            [(-10, -6), (-5, -3), (-2, 2), (3, 5), (6, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-6, -2), (2, 6)],
            [(-10, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, -1), (1, 8)],
            [(-10, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 8)],
            [(-10, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(0, 8)],
            [(-10, -6), (-2, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 0)],
            [(-10, 2), (6, 10)],
        ),
    )
    @ddt.unpack
    def test_intervals_union(self, xs, ys, expect):
        self.assertEqual(expect, intervals_union(xs, ys))
        self.assertEqual(expect, intervals_union(ys, xs))
        self.assertEqual(expect, intervals_union(xs, *[[y] for y in ys]))
        self.assertEqual(expect, intervals_union(ys, *[[x] for x in xs]))

    @ddt.data(
        ([], [], []),
        ([(-2, 2)], [], []),
        ([(-2, 2)], [(3, 5)], []),
        ([(-2, 2)], [(-5, -3)], []),
        ([(-2, 2)], [(2, 5)], [(2, 2)]),
        ([(-2, 2)], [(-5, -2)], [(-2, -2)]),
        ([(-2, 2)], [(0, 4)], [(0, 2)]),
        ([(-2, 2)], [(-4, 0)], [(-2, 0)]),
        ([(-2, 2)], [(-4, 4)], [(-2, 2)]),
        ([(-2, 2)], [(-2, 2)], [(-2, 2)]),
        ([(-2, 2)], [(-1, 1)], [(-1, 1)]),
        ([(-2, 2)], [(0, 2)], [(0, 2)]),
        ([(-2, 2)], [(-2, 0)], [(-2, 0)]),
        ([(-2, 2)], [(2, 2)], [(2, 2)]),
        ([(-2, 2)], [(-2, -2)], [(-2, -2)]),
        ([(-2, 2)], [(0, 0)], [(0, 0)]),
        ([(-10, 10)], [(-8, -4), (-2, 2), (4, 8)], [(-8, -4), (-2, 2), (4, 8)]),
        ([(-10, 10)], [(-10, -6), (-2, 2), (6, 10)], [(-10, -6), (-2, 2), (6, 10)]),
        ([(-10, 10)], [(-12, -8), (-2, 2), (8, 12)], [(-10, -8), (-2, 2), (8, 10)]),
        ([(-10, 10)], [(-12, -10), (-2, 2), (10, 12)], [(-10, -10), (-2, 2), (10, 10)]),
        ([(-10, 10)], [(-16, -12), (-2, 2), (12, 16)], [(-2, 2)]),
        ([(-10, 10)], [(-16, -12), (-11, 11), (12, 16)], [(-10, 10)]),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-5, -3), (3, 5)],
            [],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-6, -2), (2, 6)],
            [(-6, -6), (-2, -2), (2, 2), (6, 6)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, -1), (1, 8)],
            [(-8, -6), (-2, -1), (1, 2), (6, 8)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 8)],
            [(-8, -6), (-2, 2), (6, 8)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(0, 8)],
            [(0, 2), (6, 8)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 0)],
            [(-8, -6), (-2, 0)],
        ),
    )
    @ddt.unpack
    def test_intervals_intersect(self, xs, ys, expect):
        self.assertEqual(expect, intervals_intersect(xs, ys))
        self.assertEqual(expect, intervals_intersect(ys, xs))
        self.assertEqual(expect,
                         intervals_union(intervals_intersect(xs, []), *[intervals_intersect(xs, [y]) for y in ys]))
        self.assertEqual(expect,
                         intervals_union(intervals_intersect(ys, []), *[intervals_intersect(ys, [x]) for x in xs]))

    @ddt.data(
        ([], [], []),
        ([(-2, 2)], [], [(-2, 2)]),
        ([(-2, 2)], [(3, 5)], [(-2, 2)]),
        ([(-2, 2)], [(-5, -3)], [(-2, 2)]),
        ([(-2, 2)], [(2, 5)], [(-2, 2)]),
        ([(-2, 2)], [(-5, -2)], [(-2, 2)]),
        ([(-2, 2)], [(0, 4)], [(-2, 0)]),
        ([(-2, 2)], [(-4, 0)], [(0, 2)]),
        ([(-2, 2)], [(-4, 4)], []),
        ([(-2, 2)], [(-2, 2)], []),
        ([(-2, 2)], [(-1, 1)], [(-2, -1), (1, 2)]),
        ([(-2, 2)], [(0, 2)], [(-2, 0)]),
        ([(-2, 2)], [(-2, 0)], [(0, 2)]),
        ([(-2, 2)], [(2, 2)], [(-2, 2)]),
        ([(-2, 2)], [(-2, -2)], [(-2, 2)]),
        ([(-2, 2)], [(0, 0)], [(-2, 0), (0, 2)]),
        ([(-10, 10)], [(-8, -4), (-2, 2), (4, 8)], [(-10, -8), (-4, -2), (2, 4), (8, 10)]),
        ([(-10, 10)], [(-10, -6), (-2, 2), (6, 10)], [(-6, -2), (2, 6)]),
        ([(-10, 10)], [(-12, -8), (-2, 2), (8, 12)], [(-8, -2), (2, 8)]),
        ([(-10, 10)], [(-12, -10), (-2, 2), (10, 12)], [(-10, -2), (2, 10)]),
        ([(-10, 10)], [(-16, -12), (-2, 2), (12, 16)], [(-10, -2), (2, 10)]),
        ([(-10, 10)], [(-16, -12), (-11, 11), (12, 16)], []),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-5, -3), (3, 5)],
            [(-10, -6), (-2, 2), (6, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-6, -2), (2, 6)],
            [(-10, -6), (-2, 2), (6, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, -1), (1, 8)],
            [(-10, -8), (-1, 1), (8, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 8)],
            [(-10, -8), (8, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(0, 8)],
            [(-10, -6), (-2, 0), (8, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 0)],
            [(-10, -8), (0, 2), (6, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-2, 8)],
            [(-10, -6), (8, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 2)],
            [(-10, -8), (6, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-4, 8)],
            [(-10, -6), (8, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 4)],
            [(-10, -8), (6, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-6, 8)],
            [(-10, -6), (8, 10)],
        ),
        (
            [(-10, -6), (-2, 2), (6, 10)],
            [(-8, 6)],
            [(-10, -8), (6, 10)],
        ),
        (
            [(-16, -12), (-10, -6), (-2, 2), (6, 10), (12, 16)],
            [(-4, 8)],
            [(-16, -12), (-10, -6), (8, 10), (12, 16)],
        ),
        (
            [(-16, -12), (-10, -6), (-2, 2), (6, 10), (12, 16)],
            [(-8, 4)],
            [(-16, -12), (-10, -8), (6, 10), (12, 16)],
        ),
        (
            [(-16, -12), (12, 16)],
            [(-10, -6), (-2, 2), (6, 10)],
            [(-16, -12), (12, 16)],
        ),
        (
            [(-16, -12), (12, 16)],
            [(-20, -14), (-10, -6), (-2, 2), (6, 10), (14, 20)],
            [(-14, -12), (12, 14)],
        ),
    )
    @ddt.unpack
    def test_intervals_subtract(self, xs, ys, expect):
        self.assertEqual(expect, intervals_subtract(xs, ys))
        self.assertEqual(expect, intervals_subtract(xs, *[[y] for y in ys]))
        self.assertEqual(expect, intervals_subtract(xs, intervals_intersect(xs, ys)))
        self.assertEqual(expect, intervals_subtract(xs, *[intervals_intersect(xs, [y]) for y in ys]))

    @ddt.idata([(x,) for x in range(100)])
    @ddt.unpack
    def test_intervals_operations_equality(self, x):
        def make_intervals(size, lo, hi):
            vs = [float(random.randrange(lo, hi))]
            for _ in range(size * 2):
                vs.append(last(vs) + float(random.randrange(lo, hi)))
            return [(vs[2 * i], vs[2 * i + 1]) for i in range(size)]

        xs = make_intervals(200, 2, 10)
        ys = make_intervals(200, 2, 10)

        self.assertEqual(intervals_union(xs, ys), intervals_union(ys, xs))
        self.assertEqual(intervals_intersect(xs, ys), intervals_intersect(ys, xs))
        self.assertEqual(intervals_intersect(xs, ys),
                         intervals_union(intervals_intersect(xs, []), *[intervals_intersect(xs, [y]) for y in ys]))
        self.assertEqual([], intervals_subtract(xs, xs))
        self.assertEqual(intervals_subtract(xs, ys),
                         intervals_subtract(xs, *[intervals_intersect(xs, [y]) for y in ys]))
