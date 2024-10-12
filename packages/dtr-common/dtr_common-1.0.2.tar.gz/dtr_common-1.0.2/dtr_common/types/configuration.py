from typing import TypedDict, Literal
from .models import NotificationServerJson, QueueJson, PeriodicalParametersJson, TargetJson


class KafkaConf(TypedDict):
    server: str
    topics: list[str]


class SrcConf(TypedDict):
    target: str
    path: str
    purge: bool
    pattern: str

class DestConf(TypedDict):
    target: str
    path: str
    tmp_prefix_dest: str
    final_prefix_dest: str


class TransferPolicyConf(TypedDict, total=False):
    name: str
    type: Literal["periodical", "commanded"]
    queue: str
    data_type: Literal["file", "folder"]
    notifications: list[KafkaConf]
    periodical: PeriodicalParametersJson
    src: SrcConf
    dest: DestConf


class ConfigurationJson(TypedDict):
    notification_servers: list[NotificationServerJson]
    queues: list[QueueJson]
    targets: list[TargetJson]
    transfer_policies: list[str]
