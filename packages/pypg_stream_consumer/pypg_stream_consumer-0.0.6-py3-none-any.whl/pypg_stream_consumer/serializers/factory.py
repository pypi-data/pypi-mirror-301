import logging  # noqa: D100

from pypg_stream_consumer.serializers.impl.class_serializer import ClassSerializer
from pypg_stream_consumer.serializers.serializer_abc import SerializerABC

logger = logging.getLogger(__name__)


class SerializerFactory:
    """Serialixzer factory class."""

    def __init__(self, name: str) -> None:
        """Init serializer factory.

        Args:
        ----
            name (str): Serializr name

        """
        self.name = name

        self.serializers = {
            "class": ClassSerializer,
        }

        logger.debug("Validate is serializer exists ")
        if name not in self.serializers:
            msg = "Unknown serializer name: '%s'"
            raise ValueError(msg, self.name)

    def get_serializer(self) -> SerializerABC:
        """Get serializer instance.

        Returns
        -------
            Serializer: Serializer instance

        """
        logger.debug("Create '%s' serializer instance", self.name)
        return self.serializers[self.name]()
