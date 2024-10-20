import unittest

from jfw.validation.rules.bool_rule import BoolRule
from jfw.validation.rules.int_rule import IntRule
from jfw.validation.rules.list_rule import ListRule
from jfw.validation.rules.max_rule import MaxRule
from jfw.validation.rules.min_rule import MinRule
from jfw.validation.rules.required_rule import RequiredRule
from jfw.validation.rules.str_rule import StrRule
from jfw.validation.validator import Validator


class TestValidator(unittest.TestCase):
    def test_it_raises_a_value_error_when_the_rules_are_not_wrapped_in_tuple_or_list(self) -> None:
        with self.assertRaises(ValueError) as context:
            Validator({
            }, {
                'name': MinRule(1),
            })

    def test_it_validates_invalid_data(self) -> None:
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

    def test_it_validates_valid_data(self) -> None:
        validator = Validator({
            'name': 'Jules',
        }, {
            'name': [MinRule(1), StrRule()],
        })

        self.assertTrue(validator.is_valid())
        self.assertFalse(validator.has_error())
        self.assertFalse(validator.has_error('name'))
        self.assertListEqual([], validator.get_errors('name'))

    def test_it_validates_when_there_is_a_rule_that_should_not_validate_when_there_is_no_value(self) -> None:
        validator = Validator({
        }, {
            'name': [StrRule()],
        })

        self.assertTrue(validator.is_valid())

    def test_it_validates_when_there_is_a_rule_that_should_validate_when_there_is_no_value(self) -> None:
        validator = Validator({
        }, {
            'name': [RequiredRule()],
        })

        self.assertFalse(validator.is_valid())

    def test_it_invalidates_when_there_is_at_least_one_rule_false(self) -> None:
        validator = Validator({
            'name': '123'
        }, {
            'name': [MaxRule(1), MinRule(2)],
        })

        self.assertFalse(validator.is_valid())

    def test_it_validates_nested_list_value(self) -> None:
        validator = Validator({
            'data': [1]
        }, {
            'data.0': [StrRule()],
        })

        self.assertFalse(validator.is_valid())
        self.assertListEqual(validator.get_errors(), ['data.0 must be a string'])

    def test_it_tries_to_validate_a_nested_list_value_that_does_not_exist(self) -> None:
        validator = Validator({
            'data': [1]
        }, {
            'data.1': [StrRule()],
        })

        self.assertTrue(validator.is_valid())

    def test_it_validates_nested_list_values_using_asterisk_rule(self) -> None:
        validator = Validator({
            'data': [1, '', 2]
        }, {
            'data.*': [StrRule()],
        })

        self.assertFalse(validator.is_valid())
        self.assertListEqual(validator.get_errors(), ['data.0 must be a string', 'data.2 must be a string'])

    def test_it_validates_deeply_nested_list_values_using_asterisk_rule(self) -> None:
        validator = Validator({
            'data': [[1, '']]
        }, {
            'data.*.0': [StrRule()],
            'data.*.1': [IntRule()],
        })

        self.assertFalse(validator.is_valid())
        self.assertListEqual(validator.get_errors(), ['data.0.0 must be a string', 'data.0.1 must be an integer'])

    def test_it_validates_nested_dict_values_using_asterisk_rule(self) -> None:
        validator = Validator({
            'data': {'one': 1, 'two': '', 'three': 2}
        }, {
            'data.*': [StrRule()],
        })

        self.assertFalse(validator.is_valid())
        self.assertListEqual(validator.get_errors(), ['data.one must be a string', 'data.three must be a string'])

    def test_it_validates_deeply_nested_dict_values_using_asterisk_rule(self) -> None:
        validator = Validator({
            'data': {
                'one': {
                    'two': ['', 1]
                },
            }
        }, {
            'data.*.*.*': [StrRule()],
        })

        self.assertFalse(validator.is_valid())
        self.assertListEqual(validator.get_errors(), ['data.one.two.1 must be a string'])

    def test_it_validates_deeply_nested_dict_values(self) -> None:
        validator = Validator({
            'data': {
                'one': {
                    'two': ['', 1]
                },
            }
        }, {
            'data.one.two.0': [IntRule()],
            'data.one.two.1': [StrRule()],
        })

        self.assertFalse(validator.is_valid())
        self.assertListEqual(validator.get_errors(),
                             ['data.one.two.0 must be an integer', 'data.one.two.1 must be a string'])

    def test_it_validates_complex_data_with_multiple_rules(self) -> None:
        validator = Validator({
            'data': {
                'one': {
                    'two': ['', 1]
                },
                'two': [1, 2]
            },
            'meta': True
        }, {
            'meta': [BoolRule()],
            'data.one.two.0': [StrRule()],
            'data.one.two.1': [IntRule()],
            'data.two': [ListRule(), MaxRule(2)],
            'data.two.*': [IntRule()],
        })

        self.assertTrue(validator.is_valid())

if __name__ == '__main__':
    unittest.main()
