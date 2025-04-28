from enum import Enum, EnumMeta


class SuperEnum(Enum):
    def __init__(self, value, nested=None):
        self.value = value
        if nested:
            if isinstance(nested, EnumMeta):
                self._nested_enum = nested
                for enm in nested:
                    setattr(self, enm.name, enm)
                    self._set_parent(enm)

    def is_submember_of(self, parent_enum):
        current = getattr(self, "_parent_enum", None)
        while current is not None:
            if current is parent_enum:
                return True
            current = getattr(current, "_parent_enum", None)
        return False

    def enum_path(self):
        path = [self]
        current = getattr(self, "_parent_enum", None)
        while current is not None:
            path.append(current)
            current = getattr(current, "_parent_enum", None)
        return path

    def _set_parent(self, enm):
        """Recursively set parent references and modify equality/hash."""
        enm._parent_enum = self

        # Define dynamic __eq__ and __hash__
        def _eq(self_, other):
            return (
                self_ is other or
                getattr(self_, "_parent_enum", None) == other
            )

        def _hash(self_):
            return hash(getattr(self_, "_parent_enum", self_))

        enm.__eq__ = _eq.__get__(enm, type(enm))
        enm.__hash__ = _hash.__get__(enm, type(enm))

        if hasattr(enm, '_nested_enum'):
            for sub_enm in enm._nested_enum:
                setattr(enm, sub_enm.name, sub_enm)
                enm._set_parent(sub_enm)

    @property
    def top(self):
        """Return the topmost parent for this enum member."""
        current = self
        while hasattr(current, '_parent_enum'):
            current = current._parent_enum
        return current
