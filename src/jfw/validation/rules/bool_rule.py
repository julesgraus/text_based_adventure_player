from jfw.validation.rules.rule import Rule


class BoolRule(Rule):
    def is_valid(self, value) -> bool:
        return isinstance(value, bool)

    def message(self, attribute: str, value) -> str:
        return f'{attribute} must be a boolean'

    def should_validate(self, value) -> bool:
        return value is not None
