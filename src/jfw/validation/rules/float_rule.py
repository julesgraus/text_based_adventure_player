from jfw.validation.rules.rule import Rule


class FloatRule(Rule):
    def is_valid(self, value) -> bool:
        return isinstance(value, float)

    def message(self, attribute: str, value) -> str:
        return f'{attribute} must be a float'
        pass

    def should_validate(self, value) -> bool:
        return value is not None
