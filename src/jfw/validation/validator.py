from typing import List

from jfw.validation.rules.required_rule import RequiredRule
from jfw.validation.rules.rule import Rule


class Validator:
    def __init__(self, data: dict | tuple, rules: dict | tuple):
        self._data = data
        self._rules = rules
        self._errors = {}
        self._validate_rules()

    def is_valid(self):
        result = True
        self._errors = {}

        for attribute in self._rules:
            for rule in self._rules[attribute]:
                values = self._resolve_values(attribute)

                for path in values.keys():
                    if rule.should_validate(value=values[path]) and not self._validate_attribute_with_value_against_rule(
                            rule=rule,
                            value=values[path],
                            path=path
                    ):
                        result = False

        return result

    def has_error(self, attribute: str | None = None):
        if attribute is None:
            return len(self._errors) > 0

        return attribute in self._errors

    def get_errors(self, attribute: str = None) -> list:
        if attribute is None:
            errors_list = []
            for attribute in self._errors:
                errors_list.append(', '.join(self._errors.get(attribute)))

            return errors_list
        elif attribute in self._errors:
            return self._errors[attribute]
        else:
            return []

    def _validate_attribute_with_value_against_rule(self, rule: Rule, value, path: str) -> bool:
        if rule.is_valid(value) is False:
            if path not in self._errors:
                self._errors[path] = []

            self._errors[path].append(rule.message(path, value))
            return False
        return True

    def _validate_rules(self):
        for key in self._rules:
            if isinstance(self._rules[key], tuple | list) is False:
                raise ValueError('The values in the rules list must be either instances of tuple or lists')

            for rule in self._rules[key]:
                if issubclass(type(rule), Rule) is False:
                    raise ValueError('Validation rules must extend the Rule class')

    def _resolve_values(self, attribute: str) -> dict:
        parts = attribute.split('.')
        parts.reverse()
        return self._resolve_value(self._data, parts, [])

    def _resolve_value(self, current, attributes: List, path: list) -> dict:
        if len(attributes) == 0:
            return {".".join(path): current}

        attribute = attributes.pop()
        if attribute != '*':
            path.append(attribute)

        if attribute == '*' and self._is_iterable(current):
            values = {}
            for iteration, key_or_value in enumerate(current):
                nested_path = path.copy()

                path_part = str(iteration) if isinstance(current, list) else key_or_value
                value_part = key_or_value if isinstance(current, list) else current[key_or_value]

                nested_path.append(path_part)
                values[".".join(nested_path)] = value_part
            return values

        if (self._is_sequence_type(current)
            and (
                isinstance(attribute, int)
                or (isinstance(attribute, str) and attribute.isdigit())
            )
            and 0 <= int(attribute) < len(current)
        ): return self._resolve_value(current[int(attribute)], attributes, path)

        if (isinstance(attribute, str)
            and isinstance(current, dict)
            and attribute in current
        ): return self._resolve_value(current[attribute], attributes, path)

        return {".".join(path): None}

    def _is_iterable(self, value) -> bool:
        return isinstance(value, dict) or self._is_sequence_type(value)

    def _is_sequence_type(self, value) -> bool:
        return (isinstance(value, list)
                or isinstance(value, tuple)
                or isinstance(value, set)
                )
