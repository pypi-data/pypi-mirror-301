from typing import TypedDict, Literal
from .models import TransferPolicyJson


class CreateRequestJson(TypedDict):
    policy: int
    files: list[str]


class UpdateRequestJson(TypedDict, total=False):
    request_id: int
    status: Literal["queued", "in_progress", "sucessful", "failed", "cancelled"]
    sub_status: Literal["check", "validation", "destination_copy", "notify", "stopped", "source_copy"]
    nb_retry: int
    next_retry_min_time: str
    failure_reason: str

class UpdateParamsJson(TypedDict, total=False):
    param_id: int
    next_polling_min_time: str

class CreatePoliciesJson(TypedDict):
    policies: list[TransferPolicyJson]
