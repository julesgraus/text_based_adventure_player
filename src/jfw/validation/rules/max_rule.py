from jfw.validation.rules.rule import Rule


class MaxRule(Rule):
    def __init__(self, length: int):
        self.length = length

    def is_valid(self, value) -> bool:
        if isinstance(value, str | bytes | tuple | list | range):
            return len(value) <= self.length

        if isinstance(value, int | float | complex) and not isinstance(value, bool):
            if isinstance(value, complex):
                return value.real <= self.length

            return value <= self.length

        return False

    def message(self, attribute: str, value) -> str:
        if isinstance(value, str | bytes | tuple | list | range):
            return f'{attribute} must not exceed a length of {self.length}'

        return f'{attribute} must not be bigger than {self.length}'
        pass

    def should_validate(self, value) -> bool:
        return value is not None
