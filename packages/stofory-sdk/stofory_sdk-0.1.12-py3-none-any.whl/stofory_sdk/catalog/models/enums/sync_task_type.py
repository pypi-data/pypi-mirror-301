import enum


class SyncTaskType(enum.Enum):
    CREATE = enum.auto()
    UPDATE = enum.auto()
    DELETE = enum.auto()
