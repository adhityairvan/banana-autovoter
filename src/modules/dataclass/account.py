class Account:
    """
    Represents a user account.

    Attributes:
        username (str): The username of the account.
        password (str): The password of the account.
    """

    username: str
    password: str

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return self.username