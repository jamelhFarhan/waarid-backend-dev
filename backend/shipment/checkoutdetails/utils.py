from enum import IntEnum


class StatusChoice(IntEnum):
    IN_PROGRESS = 1
    APPROVED = 2
    EXPIRED = 3
    PAYED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
