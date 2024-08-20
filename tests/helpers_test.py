import unittest

from jfw.Helpers import value


class HelpersTestCase(unittest.TestCase):
    def test_value_helper_without_callable_as_argument_returns_argument(self):
        self.assertEqual('test', value('test'))

    def test_value_helper_with_callable_returns_value_from_callable(self):
        self.assertEqual('test', value(lambda: 'test'))
