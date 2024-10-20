from jfw.validation.rules.rule import Rule


class MinRule(Rule):
    def __init__(self, length: int):
        self.length = length

    def is_valid(self, value) -> bool:
        if isinstance(value, str | bytes | tuple| dict | list | range):
            return len(value) >= self.length

        if isinstance(value, int | float | complex) and not isinstance(value, bool):
            if isinstance(value, complex):
                return value.real >= self.length

            return value >= self.length

        return False

    def message(self, attribute: str, value) -> str:
        if isinstance(value, str | bytes | tuple | dict | list | range):
            return f'{attribute} must be longer than {self.length}'

        return f'{attribute} must be bigger than {self.length}'

    def should_validate(self, value) -> bool:
        return value is not None
