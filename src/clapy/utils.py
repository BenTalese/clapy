from typing import Generic, Type, TypeVar

__all__ = ["AttributeChangeTracker"]

TAttribute = TypeVar('TAttribute')

class AttributeChangeTracker(Generic[TAttribute]):
    __origin__ = Type['AttributeChangeTracker']

    def __init__(self, value: TAttribute):
        self._value = value
        self._has_been_set = True if value else False

    def __setattr__(self, name, value):
        if name == '_value':
            super().__setattr__(name, value)
            self._has_been_set = True
        else:
            super().__setattr__(name, value)

    @property
    def value(self) -> TAttribute:
        return self._value

    @property
    def has_been_set(self) -> bool:
        return self._has_been_set

    def __repr__(self) -> str:
        return repr(self._value)

    def __class__(self):
        return type(self._value)
