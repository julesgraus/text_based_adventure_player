from typing import LiteralString

from jfw.Helpers import value as value_resolver


class Container:
    def __init__(self):
        self.__simple_bindings = {}

    def bind(self, key: LiteralString, value: LiteralString | int | float | object | bool):
        self.__simple_bindings[key] = value

    def resolve(self, key: LiteralString):
        if key in self.__simple_bindings:
            return self.__resolve_simple_binding(key)

    def __resolve_simple_binding(self, key: LiteralString) -> None | LiteralString | int | float | object | bool:
        if key in self.__simple_bindings:
            return value_resolver(self.__simple_bindings[key])

        return None
