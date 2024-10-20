from jfw.validation.rules.rule import Rule


class ListRule(Rule):
    def is_valid(self, value) -> bool:
        return isinstance(value, list)

    def message(self, attribute: str, value) -> str:
        return f'{attribute} must be a list'

    def should_validate(self, value) -> bool:
        return value is not None
