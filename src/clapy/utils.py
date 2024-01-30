from typing import Generic, Optional, Type, TypeVar

__all__ = ["AttributeChangeTracker"]

TAttributeValue = TypeVar('TAttributeValue')

class AttributeChangeTracker(Generic[TAttributeValue]):
    __origin__ = Type['AttributeChangeTracker']

    def __init__(self, value: Optional[TAttributeValue] = None, has_been_set: Optional[bool] = False):
        self._value = value
        self._has_been_set = has_been_set

    def __setattr__(self, name, value):
        if name == '_value':
            super().__setattr__(name, value)
            self._has_been_set = True
        else:
            super().__setattr__(name, value)

    @property
    def value(self) -> TAttributeValue:
        return self._value # type: ignore

    @property
    def has_been_set(self) -> bool:
        return self._has_been_set # type: ignore

    def __repr__(self) -> str:
        return repr(self._value)

    def __class__(self):
        return type(self._value)
