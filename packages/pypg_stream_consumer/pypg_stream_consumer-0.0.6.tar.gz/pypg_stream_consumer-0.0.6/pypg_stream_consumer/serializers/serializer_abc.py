from abc import ABCMeta, abstractmethod  # noqa: D100


class SerializerABC:
    """replication messages serializer."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def serialize(self, msg: any) -> any:
        """Message serialize function.

        Args:
        ----
            msg (any): Source replication message

        Returns:
        -------
            any: Serialized replication message

        """
