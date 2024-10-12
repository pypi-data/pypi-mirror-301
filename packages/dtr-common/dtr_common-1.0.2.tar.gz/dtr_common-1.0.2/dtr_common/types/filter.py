from typing import TypedDict, Literal


class FilterPolicyParams(TypedDict, total=False):
    enabled: bool
    type: Literal["periodical", "commanded"]
    dataType: Literal["file", "folder"]
    queues: str
    id: int
    ids: str


class FilterRequestParams(TypedDict, total=False):
    queues: str
    state: Literal["queued", "in_progress", "sucessfull", "failed", "cancelled"]
