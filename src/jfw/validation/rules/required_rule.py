from jfw.validation.rules.rule import Rule


class RequiredRule(Rule):
    def is_valid(self, value) -> bool:
        if value is None:
            return False

        if (
                isinstance(value, str)
                or isinstance(value, tuple)
                or isinstance(value, list)
                or isinstance(value, set)
                or isinstance(value, dict)
        ) and len(value) == 0:
            return False

        return True

    def message(self, attribute: str, value) -> str:
        return f'{attribute} is required'

    def should_validate(self, value) -> bool:
        return True
