from __future__ import annotations  # noqa: D100


class MetaFilter(type):
    """Filter meta class."""

    action_identifier: str = ""

    def __str__(cls) -> str:
        """Class string representation."""
        return cls.action_identifier


class InsertFilter(metaclass=MetaFilter):
    """Insert filter class."""

    action_identifier = "I"


class DeleteFilter(metaclass=MetaFilter):
    """Delete filter class."""

    action_identifier = "D"


class UpdateFilter(metaclass=MetaFilter):
    """Update filter class."""

    action_identifier = "U"


class BeginFilter(metaclass=MetaFilter):
    """Begin filter class."""

    action_identifier = "B"


class CommitFilter(metaclass=MetaFilter):
    """Commit filter class."""

    action_identifier = "C"
