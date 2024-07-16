from datetime import datetime

class Message:
    """
    Represents a message in the queue.

    Attributes:
        processName (str): The name of the process.
        createdAt (datetime): The timestamp when the message was created.
    """
    processName: str
    createdAt: datetime
    def __init__(self, processName: str, createdAt: datetime = datetime.now()) -> None:
        """
        Initializes a new instance of the Message class.

        Args:
            processName (str): The name of the process.
            createdAt (datetime, optional): The timestamp when the message was created.
                Defaults to the current datetime.
        """
        self.processName = processName
        self.createdAt = createdAt