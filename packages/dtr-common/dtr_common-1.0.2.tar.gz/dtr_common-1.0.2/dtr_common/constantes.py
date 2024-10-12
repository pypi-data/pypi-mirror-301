from enum import Enum


class State(Enum):
    QUEUED = "queued"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    CANCELLED = "cancelled"
    IN_PROGRESS = "in_progress"
    NOTIFY = "notify"

class SubState(Enum):
    CHECK = "check"
    VALIDATION = "validation"
    DESTINATION_COPY = "destination_copy"
    NOTIFY = "notify"
    STOPPED = "stopped"
    SOURCE_COPY = "source_copy"

class Mode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"

class Type(Enum):
    PERIODICAL = "periodical"
    COMMANDED = "commanded"
