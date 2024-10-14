from jfw.validation.rules.required_rule import RequiredRule
from jfw.validation.rules.rule import Rule


class Validator:
    def __init__(self, data: dict | tuple, rules: dict | tuple):
        self.data = data
        self.rules = rules
        self._errors = {}
        self._validate_rules()

    def is_valid(self):
        result = True
        self._errors = {}

        for attribute in self.rules:
            for rule in self.rules[attribute]:
                value = None
                if attribute in self.data:
                    value = self.data[attribute]

                if rule.should_validate(value=value) and not self._validate_attribute_with_value_against_rule(attribute=attribute,
                                                                                                   rule=rule,
                                                                                                   value=value):
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

    def _validate_attribute_with_value_against_rule(self, attribute: str, rule: Rule, value) -> bool:
        if rule.is_valid(value) is False:
            if attribute not in self._errors:
                self._errors[attribute] = []

            self._errors[attribute].append(rule.message(attribute, value))
            return False
        return True

    def _validate_rules(self):
        for key in self.rules:
            if isinstance(self.rules[key], tuple | list) is False:
                raise ValueError('The values in the rules list must be either instances of tuple or lists')

            for rule in self.rules[key]:
                if issubclass(type(rule), Rule) is False:
                    raise ValueError('Validation rules must extend the Rule class')
