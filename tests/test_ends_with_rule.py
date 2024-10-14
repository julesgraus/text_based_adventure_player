import unittest

from jfw.validation.rules.ends_with_rule import EndsWithRule


class TestEndsWithRule(unittest.TestCase):
    def test_validity(self):
        self.assertFalse(EndsWithRule('.txt').is_valid(''))
        self.assertFalse(EndsWithRule('.txt').is_valid('something.test'))
        self.assertTrue(EndsWithRule('.txt').is_valid('something.txt'))

    def test_message(self):
        self.assertEqual(f'some attribute must end with .txt', EndsWithRule('.txt').message('some attribute', ''))

    def test_should_validate_when_value_is_none(self):
        self.assertEqual(False, EndsWithRule(1).should_validate(None))

    def test_should_validate_when_value_is_not_none(self):
        self.assertEqual(True, EndsWithRule(1).should_validate(''))

if __name__ == '__main__':
    unittest.main()
