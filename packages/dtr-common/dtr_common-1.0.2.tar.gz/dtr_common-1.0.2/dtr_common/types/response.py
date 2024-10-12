from typing import TypedDict, Literal
from .models import TransferPolicyJson, RequestJson


class PoliciesResponseJson(TypedDict):
    page: int
    page_size: int
    total: int
    policies: list[TransferPolicyJson]


class RequestsResponseJson(TypedDict):
    page: int
    page_size: int
    total: int
    requests: list[RequestJson]


class StatusResponseJson(TypedDict):
    id: int
    mode: Literal["online", "offline"]
    updated_at: str
