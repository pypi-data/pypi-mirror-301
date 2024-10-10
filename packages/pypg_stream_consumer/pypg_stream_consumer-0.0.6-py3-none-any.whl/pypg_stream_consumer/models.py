from __future__ import annotations  # noqa: D100

from dataclasses import dataclass


@dataclass
class ReplicationMessagePayload:
    """PG replication message payload."""

    action: str
    schema: str | None = None
    table: str | None = None
    columns: list[str] | None = None
    identity: str | None = None


@dataclass
class ReplicationMessage:
    """PG replication message."""

    data_start: str
    wal_end: str
    send_time: int
    data_size: int
    payload: ReplicationMessagePayload
