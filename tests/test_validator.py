import unittest

from jfw.validation.rules.int_rule import IntRule
from jfw.validation.rules.max_rule import MaxRule
from jfw.validation.rules.min_rule import MinRule
from jfw.validation.rules.required_rule import RequiredRule
from jfw.validation.rules.str_rule import StrRule
from jfw.validation.validator import Validator


class TestValidator(unittest.TestCase):
    def test_it_raises_a_value_error_when_the_rules_are_not_wrapped_in_tuple_or_list(self):
        with self.assertRaises(ValueError) as context:
            Validator({
            }, {
                'name': MinRule(1),
            })

    def test_it_validates_invalid_data(self):
        validator = Validator({
            'name': '',
        }, {
            'name': [MinRule(1), IntRule()],
        })

        self.assertFalse(validator.has_error())

        self.assertFalse(validator.is_valid())

        self.assertTrue(validator.has_error())
        self.assertTrue(validator.has_error('name'))
        self.assertFalse(validator.has_error('other'))

        self.assertListEqual(['name must be longer than 1', 'name must be an integer'], validator.get_errors('name'))
        self.assertListEqual([], validator.get_errors('other'))

    def test_it_validates_valid_data(self):
        validator = Validator({
            'name': 'Jules',
        }, {
            'name': [MinRule(1), StrRule()],
        })

        self.assertTrue(validator.is_valid())
        self.assertFalse(validator.has_error())
        self.assertFalse(validator.has_error('name'))
        self.assertListEqual([], validator.get_errors('name'))

    def test_it_validates_when_there_is_a_rule_that_should_not_validate_when_there_is_no_value(self):
        validator = Validator({
        }, {
            'name': [StrRule()],
        })

        self.assertTrue(validator.is_valid())

    def test_it_validates_when_there_is_a_rule_that_should_validate_when_there_is_no_value(self):
        validator = Validator({
        }, {
            'name': [RequiredRule()],
        })

        self.assertFalse(validator.is_valid())

    def test_it_invalidates_when_there_is_at_least_one_rule_false(self):
        validator = Validator({
            'name': '123'
        }, {
            'name': [MaxRule(1), MinRule(2)],
        })

        self.assertFalse(validator.is_valid())



if __name__ == '__main__':
    unittest.main()
