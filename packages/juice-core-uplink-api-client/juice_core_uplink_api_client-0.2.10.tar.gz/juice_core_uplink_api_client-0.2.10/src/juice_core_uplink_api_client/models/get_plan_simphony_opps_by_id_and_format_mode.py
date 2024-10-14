from enum import Enum


class GetPlanSimphonyOppsByIdAndFormatMode(str, Enum):
    OPEN = "open"
    STRICT = "strict"

    def __str__(self) -> str:
        return str(self.value)
