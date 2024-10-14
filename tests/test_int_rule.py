import unittest

from jfw.validation.rules.int_rule import IntRule


class TestIntRule(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(IntRule().is_valid(1))
        self.assertFalse(IntRule().is_valid(1.0))
        self.assertFalse(IntRule().is_valid({}))
        self.assertFalse(IntRule().is_valid([]))
        self.assertFalse(IntRule().is_valid(''))
        self.assertFalse(IntRule().is_valid('1'))

    def test_message(self):
        self.assertEqual('some attribute must be an integer', IntRule().message('some attribute', 0.1))

    def test_should_validate_when_value_is_none(self):
        self.assertEqual(False, IntRule().should_validate(None))

    def test_should_validate_when_value_is_not_none(self):
        self.assertEqual(True, IntRule().should_validate(''))

if __name__ == '__main__':
    unittest.main()
