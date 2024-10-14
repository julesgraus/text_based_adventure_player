import unittest

from jfw.validation.rules.str_rule import StrRule


class MaxRuleTestCase(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(StrRule().is_valid(''))
        self.assertFalse(StrRule().is_valid(1.0))
        self.assertFalse(StrRule().is_valid({}))
        self.assertFalse(StrRule().is_valid([]))

    def test_message(self):
        self.assertEqual('some attribute must be a string', StrRule().message('some attribute', 0.1))

    def test_should_validate(self):
        self.assertEqual(False, StrRule().should_validate(None))

if __name__ == '__main__':
    unittest.main()
