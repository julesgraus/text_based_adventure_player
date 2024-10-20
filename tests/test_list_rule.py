import unittest

from jfw.validation.rules.list_rule import ListRule


class TestListRule(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(ListRule().is_valid([]))
        self.assertFalse(ListRule().is_valid({}))

    def test_message(self):
        self.assertEqual('some attribute must be a list', ListRule().message('some attribute', 0.1))

    def test_should_validate_when_value_is_none(self):
        self.assertEqual(False, ListRule().should_validate(None))

    def test_should_validate_when_value_is_not_none(self):
        self.assertEqual(True, ListRule().should_validate(0.1))

if __name__ == '__main__':
    unittest.main()
