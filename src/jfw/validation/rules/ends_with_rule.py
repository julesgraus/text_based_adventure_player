from jfw.validation.rules.rule import Rule


class EndsWithRule(Rule):
    def __init__(self, ends_with: str):
        self.ends_with = ends_with

    def is_valid(self, value) -> bool:
        if isinstance(value, str):
            return value.endswith(self.ends_with)

        return False

    def message(self, attribute: str, value) -> str:
        return f'{attribute} must end with {self.ends_with}'

    def should_validate(self, value) -> bool:
        return value is not None
