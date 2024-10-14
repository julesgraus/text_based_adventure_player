from jfw.validation.rules.rule import Rule


class StrRule(Rule):
    def is_valid(self, value) -> bool:
        return isinstance(value, str)

    def message(self, attribute: str, value) -> str:
        return f'{attribute} must be a string'

    def should_validate(self, value) -> bool:
        return value is not None
