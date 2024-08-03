from typing import List
from src.modules.dataclass.message import Message
from datetime import datetime

class VotingProcessMessage(Message):
    totalAccount: int
    numProcessed: int
    processedAccount: List[str]
    def __init__(self, proceessName: str, totalAccount: int, numProcessed: int, processedAccount: List[str], createdAt: datetime = datetime.now()) -> None:
        super().__init__(proceessName, createdAt)
        self.totalAccount = totalAccount
        self.numProcessed = numProcessed
        self.processedAccount = processedAccount
        pass
    def __str__(self) -> str:
        return self.processedAccount.__str__()