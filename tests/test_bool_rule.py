import unittest

from jfw.validation.rules.bool_rule import BoolRule


class TestBoolRule(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(BoolRule().is_valid(True))
        self.assertFalse(BoolRule().is_valid(1.0))
        self.assertFalse(BoolRule().is_valid({}))
        self.assertFalse(BoolRule().is_valid([]))
        self.assertFalse(BoolRule().is_valid(''))
        self.assertFalse(BoolRule().is_valid('1'))

    def test_message(self):
        self.assertEqual('some attribute must be a boolean', BoolRule().message('some attribute', 0.1))

    def test_should_validate_when_value_is_none(self):
        self.assertEqual(False, BoolRule().should_validate(None))

    def test_should_validate_when_value_is_not_none(self):
        self.assertEqual(True, BoolRule().should_validate(''))

if __name__ == '__main__':
    unittest.main()
