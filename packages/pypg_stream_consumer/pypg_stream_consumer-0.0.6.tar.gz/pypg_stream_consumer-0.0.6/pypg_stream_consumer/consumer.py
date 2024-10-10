from __future__ import annotations  # noqa: D100

import logging

import psycopg2
import psycopg2.extras

from pypg_stream_consumer.models import ReplicationMessagePayload  # noqa: TCH001
from pypg_stream_consumer.serializers.factory import SerializerFactory
from pypg_stream_consumer.serializers.serializer_abc import SerializerABC  # noqa: TCH001

logger = logging.getLogger(__name__)


class PGStreamConsumer:
    """Postgres logical replication stream consumer."""

    def __init__(  # noqa: PLR0913
        self,
        db_uri: str,
        name: str,
        serializer: SerializerABC | None = None,
        callback: callable | None = None,
        filters: list[callable] | None = None,
    ) -> None:
        """Init Stream Consumer.

        Args:
        ----
            db_uri (str): DB URI string
            name (str): Consumer name
            serializer (Serialize, optional): Replication messages serializer. Defaults to None.
            callback (callable, optional): Callback function. Defaults to None.
            filters (list[callable], optional): Relication message filters list. Defaults to None.

        """
        self.db_uri = db_uri
        self.name = name
        self.serializer = serializer
        self.callback = callback
        self.filters = filters
        self.__inner_serializer = SerializerFactory(name="class").get_serializer()
        self.__conn = None

    def run(self) -> None:
        """Configure consumer and start consuming messages."""
        logger.debug("Create postgres connection with URI: %s", self.db_uri)
        self.__conn = psycopg2.connect(
            self.db_uri,
            connection_factory=psycopg2.extras.LogicalReplicationConnection,
        )
        cur = self.__conn.cursor()

        logger.debug("Create replication slot with name: %s", self.name)
        try:
            cur.create_replication_slot(self.name, output_plugin="wal2json")  # "pgoutput"
        except psycopg2.errors.DuplicateObject:
            logger.warning("Replication slot '%s' already exists", self.name)

        logger.debug("Start replication")
        cur.start_replication(slot_name=self.name, options={"format-version": 2}, decode=True)
        cur.consume_stream(self.__message_handler)

    def stop(self) -> None:
        """Stop consuming."""
        logger.debug("Stopping replication")
        self.__conn.close()

    def __message_handler(self, msg: psycopg2.extras.ReplicationMessage) -> None:
        """Process received replication message.

        Args:
        ----
            msg (psycopg2.extras.LogicalReplicationMessage): Logical replication message

        """
        logger.debug("Received new message:")
        logger.debug("LSN: %s", msg.data_start)
        logger.debug("Data: %s", msg.payload)

        serialized_msg = self.__inner_serializer.serialize(msg)
        if self.filters and not self.__apply_filters(serialized_msg.payload):
            logger.debug("Message filtered")
            msg.cursor.send_feedback(flush_lsn=msg.data_start)
            return

        if self.callback:
            if self.serializer:
                self.callback(self.serializer.serialize(msg))
            else:
                self.callback(msg)

        logger.debug("Commit LSN: %s", msg.data_start)
        msg.cursor.send_feedback(flush_lsn=msg.data_start)

    def __apply_filters(self, payload: ReplicationMessagePayload) -> bool:
        """Apply filters to message.

        Args:
        ----
            payload (ReplicationMessagePayload): Replication message

        Returns:
        -------
            bool: Filter result

        """
        return any(payload.action == str(filter_) for filter_ in self.filters)
