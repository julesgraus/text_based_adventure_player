import unittest

from jfw.validation.rules.min_rule import MinRule


class TestMinRule(unittest.TestCase):
    def test_validity(self):
        self.assertFalse(MinRule(2).is_valid(''))
        self.assertFalse(MinRule(2).is_valid(' '))
        self.assertTrue(MinRule(2).is_valid('  '))

        self.assertFalse(MinRule(2).is_valid(bytes('', 'utf8')))
        self.assertFalse(MinRule(2).is_valid(bytes(' ', 'utf8')))
        self.assertTrue(MinRule(2).is_valid(bytes('  ', 'utf8')))

        self.assertFalse(MinRule(2).is_valid(()))
        self.assertFalse(MinRule(2).is_valid((' ')))
        self.assertTrue(MinRule(2).is_valid((' ', ' ')))

        self.assertFalse(MinRule(2).is_valid([]))
        self.assertFalse(MinRule(2).is_valid(['']))
        self.assertTrue(MinRule(2).is_valid(['', '']))

        self.assertFalse(MinRule(2).is_valid(range(0)))
        self.assertFalse(MinRule(2).is_valid(range(1)))
        self.assertTrue(MinRule(2).is_valid(range(2)))

        self.assertFalse(MinRule(2).is_valid(0))
        self.assertFalse(MinRule(2).is_valid(1))
        self.assertTrue(MinRule(2).is_valid(2))

        self.assertFalse(MinRule(2).is_valid(0.0))
        self.assertFalse(MinRule(2).is_valid(1.0))
        self.assertTrue(MinRule(2).is_valid(2.0))

        self.assertFalse(MinRule(2).is_valid(complex('+1.23')))
        self.assertTrue(MinRule(2).is_valid(complex('+2.23')))

    def test_message(self):
        self.assertEqual('some attribute must be longer than 1', MinRule(1).message('some attribute', ''))
        self.assertEqual('some attribute must be bigger than 1', MinRule(1).message('some attribute', 2))

    def test_should_validate_when_value_is_none(self):
        self.assertEqual(False, MinRule(1).should_validate(None))

    def test_should_validate_when_value_is_not_none(self):
        self.assertEqual(True, MinRule(1).should_validate(''))

if __name__ == '__main__':
    unittest.main()
