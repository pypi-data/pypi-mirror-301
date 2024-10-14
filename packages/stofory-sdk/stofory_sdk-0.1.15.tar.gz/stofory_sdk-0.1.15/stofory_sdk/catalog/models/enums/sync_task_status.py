import enum


class SyncTaskStatus(enum.Enum):
    PENDING = enum.auto()
    PROCESSING = enum.auto()
    COMPLETED = enum.auto()
    FAILED = enum.auto()
