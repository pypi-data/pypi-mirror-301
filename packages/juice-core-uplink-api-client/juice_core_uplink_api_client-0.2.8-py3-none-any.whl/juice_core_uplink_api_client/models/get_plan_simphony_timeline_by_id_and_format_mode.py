from enum import Enum


class GetPlanSimphonyTimelineByIdAndFormatMode(str, Enum):
    OPEN = "open"
    STRICT = "strict"

    def __str__(self) -> str:
        return str(self.value)
