"""Exceptions raised by the Kenya Data SDK."""


class KenyaDataError(Exception):
    """Base class for all kenya-data SDK errors."""


class EntityNotFoundError(KenyaDataError):
    """Raised when a lookup does not match any entity."""

    def __init__(self, entity_type: str, identifier: str) -> None:
        self.entity_type = entity_type
        self.identifier = identifier
        super().__init__(f"No {entity_type} found matching {identifier!r}")
