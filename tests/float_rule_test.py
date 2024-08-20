import unittest

from jfw.validation.rules.float_rule import FloatRule


class MaxRuleTestCase(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(FloatRule().is_valid(1.0))
        self.assertFalse(FloatRule().is_valid(1))
        self.assertFalse(FloatRule().is_valid({}))
        self.assertFalse(FloatRule().is_valid([]))
        self.assertFalse(FloatRule().is_valid(''))
        self.assertFalse(FloatRule().is_valid('1'))

    def test_message(self):
        self.assertEqual('some attribute must be a float', FloatRule().message('some attribute', 0.1))


if __name__ == '__main__':
    unittest.main()
