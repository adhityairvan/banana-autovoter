from typing import List
from datetime import datetime
from src.modules.dataclass.message import Message

class VotingProcessMessage(Message):
    totalAccount: int
    numProcessed: int
    processedAccount: List[str]
    def __init__(self,
                 proceessName: str,
                 totalAccount: int,
                 numProcessed: int,
                 processedAccount: List[str],
                 createdAt: datetime = datetime.now()) -> None:
        super().__init__(proceessName, createdAt)
        self.totalAccount = totalAccount
        self.numProcessed = numProcessed
        self.processedAccount = processedAccount
    def __str__(self) -> str:
        return self.processedAccount.__str__()
