import unittest

import ddt

from iker.common.core.exceptions import BaseTraceableException


@ddt.ddt
class BaseTraceableExceptionTest(unittest.TestCase):

    @ddt.data(
        ("A plain message", [], "A plain message"),
        ("A formatted message, %s!", ["Holy smoke"], "A formatted message, Holy smoke!"),
        ("A formatted message, %s %s!", ["Holy", "smoke"], "A formatted message, Holy smoke!"),
        ("%d formatted message, %s %s!", [1, "Holy", "smoke"], "1 formatted message, Holy smoke!"),
    )
    @ddt.unpack
    def test_builtin_init(self, format_string, args, expect):
        error = BaseTraceableException(format_string, *args)
        self.assertEqual(expect, str(error))
