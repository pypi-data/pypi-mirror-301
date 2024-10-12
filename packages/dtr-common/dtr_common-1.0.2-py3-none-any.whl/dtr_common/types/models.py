from __future__ import annotations
from typing import TypedDict, Literal


class CredentialsJson(TypedDict, total=False):
    login: str
    password: str
    type: str | None
    token: str | None


class NotificationServerJson(TypedDict, total=False):
    name: str
    type: str
    host: str
    port: int
    timeout: str
    credentials: CredentialsJson | None


class TargetJson(TypedDict, total=False):
    name: str
    protocol: Literal["FTPS", "SFTP", "S3"]
    host: str
    port: int
    credentials: CredentialsJson | None


class KafkaServerParametersJson(TypedDict, total=False):
    server: NotificationServerJson
    topic: str
    replica: int
    partitions: int


class QueueJson(TypedDict, total=False):
    name: str
    priority: int
    uid: str


class SrcPolicyJson(TypedDict, total=False):
    target: TargetJson
    path: str | None
    purge: bool
    pattern: str


class DestPolicyJson(TypedDict, total=False):
    target: TargetJson
    path: str | None


class PeriodicalParametersJson(TypedDict, total=False):
    polling_interval: int


class TransferPolicyParametersJson(TypedDict):
    compress: bool
    compress_type: str | None
    data_type: Literal["file", "folder"]
    max_retry: int
    periodical: PeriodicalParametersJson
    retention_delay: int
    retry_delay: int
    only_new_data: bool


class StateJson(TypedDict, total=False):
    date: str
    state: Literal["queued", "failed", "cancelled", "notify", "in_progress"]

class SubStateJson(TypedDict, total=False):
    date: str
    sub_state: Literal["check", "validation", "destination_copy", "notify", "stopped", "source_copy"]

class TransferPolicyJson(TypedDict, total=False):
    id: int
    name: str
    type: Literal["periodical", "commanded"]
    enabled: bool
    queue: QueueJson
    data_type: Literal["file", "directory"]
    kafka: list[KafkaServerParametersJson] | None
    notifications: list[KafkaServerParametersJson] | None
    parameters: TransferPolicyParametersJson
    src: SrcPolicyJson
    dest: DestPolicyJson
    transfers: list[RequestJson]
    created_at: str


class RequestJson(TypedDict, total=False):
    id: int
    date: str
    filename: str
    nb_retry: int
    size: int | None
    uid: str
    states: list[StateJson]
    sub_states: list[SubStateJson]
    policy: TransferPolicyJson
