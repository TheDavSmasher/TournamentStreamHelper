from enum import Enum, EnumMeta
from typing import Iterator, Type


class SuperEnumMeta(EnumMeta):
    def __iter__(cls) -> Iterator['SuperEnum']:
        member: SuperEnum
        for member in super().__iter__():
            yield member
            if member._nested is not None:
                yield from member._nested


class SuperEnum(Enum, metaclass=SuperEnumMeta):
    def __new__(cls, value, _=None):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, _, nested: Type['SuperEnum'] = None):
        self._parent: SuperEnum | None = None
        self._nested = nested
        if nested:
            if not issubclass(nested, SuperEnum):
                raise TypeError(f"Nested enum must be a SuperEnum, got {type(nested)}.")
            for enm in nested:
                setattr(self, enm.name, enm)
                enm._parent = self

    def is_submember_of(self, parent_enum):
        return self == parent_enum

    def __eq__(self, other):
        return self is other or self._parent == other

    def __hash__(self):
        return hash(self._parent or self)

    @property
    def enum_path(self):
        path = [self]
        current = self._parent
        while current is not None:
            path.append(current)
            current = current._parent
        return path

    @property
    def top(self):
        """Return the topmost parent for this enum member."""
        return self.enum_path[-1]
