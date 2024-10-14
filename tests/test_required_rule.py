import unittest

from jfw.validation.rules.required_rule import RequiredRule


class RequiredRuleTestCase(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(RequiredRule().is_valid(' '))
        self.assertTrue(RequiredRule().is_valid(('value', 9)))
        self.assertTrue(RequiredRule().is_valid([1, 1]))
        self.assertTrue(RequiredRule().is_valid({1, 2}))
        self.assertTrue(RequiredRule().is_valid({1: 2}))

        self.assertFalse(RequiredRule().is_valid(None))

        self.assertFalse(RequiredRule().is_valid(''))
        self.assertFalse(RequiredRule().is_valid(()))
        self.assertFalse(RequiredRule().is_valid([]))
        self.assertFalse(RequiredRule().is_valid({}))

    def test_message(self):
        self.assertEqual('some attribute is required', RequiredRule().message('some attribute', None))

    def test_should_validate(self):
        self.assertEqual(True, RequiredRule().should_validate(None))

if __name__ == '__main__':
    unittest.main()
