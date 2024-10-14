import unittest

from jfw.validation.rules.max_rule import MaxRule


class MaxRuleTestCase(unittest.TestCase):
    def test_validity(self):
        self.assertTrue(MaxRule(1).is_valid(''))
        self.assertTrue(MaxRule(1).is_valid(' '))
        self.assertFalse(MaxRule(1).is_valid('  '))

        self.assertTrue(MaxRule(1).is_valid(bytes('', 'utf8')))
        self.assertTrue(MaxRule(1).is_valid(bytes(' ', 'utf8')))
        self.assertFalse(MaxRule(1).is_valid(bytes('  ', 'utf8')))

        self.assertTrue(MaxRule(1).is_valid(()))
        self.assertTrue(MaxRule(1).is_valid((' ')))
        self.assertFalse(MaxRule(1).is_valid((' ', ' ')))

        self.assertTrue(MaxRule(1).is_valid([]))
        self.assertTrue(MaxRule(1).is_valid(['']))
        self.assertFalse(MaxRule(1).is_valid(['', '']))

        self.assertTrue(MaxRule(1).is_valid(range(0)))
        self.assertTrue(MaxRule(1).is_valid(range(1)))
        self.assertFalse(MaxRule(1).is_valid(range(2)))

        self.assertTrue(MaxRule(1).is_valid(0))
        self.assertTrue(MaxRule(1).is_valid(1))
        self.assertFalse(MaxRule(1).is_valid(2))

        self.assertTrue(MaxRule(1).is_valid(0.0))
        self.assertTrue(MaxRule(1).is_valid(1.0))
        self.assertFalse(MaxRule(1).is_valid(2.0))

        self.assertTrue(MaxRule(1).is_valid(complex('+0.13')))
        self.assertFalse(MaxRule(1).is_valid(complex('+2.13')))

    def test_message(self):
        self.assertEqual('some attribute must not exceed a length of 1', MaxRule(1).message('some attribute', ''))
        self.assertEqual('some attribute must not be bigger than 1', MaxRule(1).message('some attribute', 2))

    def test_should_validate_when_value_is_none(self):
        self.assertEqual(False, MaxRule(1).should_validate(None))

    def test_should_validate_when_value_is_not_none(self):
        self.assertEqual(True, MaxRule(1).should_validate(''))

if __name__ == '__main__':
    unittest.main()
