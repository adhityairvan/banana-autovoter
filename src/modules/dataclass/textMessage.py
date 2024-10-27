from typing import List
from src.modules.dataclass.message import Message
from datetime import datetime

class TextMessage(Message):
    textMessage: str
    def __init__(self, proceessName: str, textMessage: str, createdAt: datetime = datetime.now()) -> None:
        super().__init__(proceessName, createdAt)
        self.textMessage = textMessage
        pass
    def __str__(self) -> str:
        return self.textMessage.__str__()