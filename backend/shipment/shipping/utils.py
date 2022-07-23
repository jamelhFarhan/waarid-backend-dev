from enum import IntEnum


class StatusChoice(IntEnum):
    IN_PROGRESS = 1
    SHIPPED = 2
    DELIVERED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

