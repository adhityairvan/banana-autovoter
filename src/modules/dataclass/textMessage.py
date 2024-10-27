from datetime import datetime
from src.modules.dataclass.message import Message

class TextMessage(Message):
    textMessage: str
    def __init__(self,
                 proceessName: str,
                 textMessage: str,
                 createdAt: datetime = datetime.now()) -> None:
        super().__init__(proceessName, createdAt)
        self.textMessage = textMessage
    def __str__(self) -> str:
        return self.textMessage.__str__()
