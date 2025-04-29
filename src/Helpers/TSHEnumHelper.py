from enum import Enum


class SuperEnum(Enum):
    def __new__(cls, value, _=None):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, _, nested=None):
        self._parent_enum: SuperEnum | None = None
        if nested:
            if not isinstance(nested, type(self)):
                raise TypeError(f"Nested enum must be a SuperEnum, got {type(nested)}.")
            for enm in nested:
                setattr(self, enm.name, enm)
                enm._parent_enum = self

    def is_submember_of(self, parent_enum):
        return self == parent_enum

    def __eq__(self, other):
        return self is other or self._parent_enum == other

    def __hash__(self):
        return hash(self._parent_enum or self)

    @property
    def enum_path(self):
        path = [self]
        current = self._parent_enum
        while current is not None:
            path.append(current)
            current = current._parent_enum
        return path

    @property
    def top(self):
        """Return the topmost parent for this enum member."""
        current = self
        while current._parent_enum is not None:
            current = current._parent_enum
        return current
