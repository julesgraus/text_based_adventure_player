from jfw.validation.rules.rule import Rule


class IntRule(Rule):
    def is_valid(self, value) -> bool:
        return isinstance(value, int)

    def message(self, attribute: str, value) -> str:
        return f'{attribute} must be an integer'
        pass


