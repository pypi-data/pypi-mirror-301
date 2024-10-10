import json  # noqa: D100

import psycopg2.extras

from pypg_stream_consumer.models import ReplicationMessage, ReplicationMessagePayload
from pypg_stream_consumer.serializers.serializer_abc import SerializerABC


class ClassSerializer(SerializerABC):
    """JSON formatted replication message to dict serializer."""

    def serialize(self, msg: psycopg2.extras.ReplicationMessage) -> ReplicationMessage:
        """Serialize message function.

        Args:
        ----
            msg (str): JSON string

        Returns:
        -------
            ReplicationMessage: Serialize message

        """
        return ReplicationMessage(
            data_start=msg.data_start,
            wal_end=msg.wal_end,
            send_time=msg.send_time,
            data_size=msg.data_size,
            payload=ReplicationMessagePayload(**json.loads(msg.payload)),
        )
