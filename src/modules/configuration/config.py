import json
from typing import List
import jsons

from src.modules.dataclass.account import Account
from src.modules.configuration import CONFIG_FILE, RFBANANA_CPANEL


class Config:
    accounts: List[Account] = []
    cpanelUrl: str = RFBANANA_CPANEL
    timeoutLimit: int = 15
    debugMode: bool = False
    def __init__(self) -> None:
        with open(CONFIG_FILE, encoding="UTF", mode="a+") as configRaw:
            configRaw.seek(0)
            if configRaw.read() == "":
                stringDumps = jsons.dumps(obj=self, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
                configRaw.write(stringDumps)
            configRaw.seek(0)
            config = json.load(configRaw)
            for jsonAccount in config.get('accounts'):
                self.accounts.append(Account(jsonAccount.get('username'), 
                                             jsonAccount.get('password')))
            self.cpanelUrl = config.get('cpanel_host', RFBANANA_CPANEL)
            self.timeoutLimit = config.get('timeout_limit')
            self.debugMode = config.get('debug_mode', False)
    def addAccount(self, username: str, password: str) -> None:
        self.accounts.append(Account(username, password))
    def deleteAccount(self, username: str) -> None:
        for account in self.accounts:
            if account.username == username:
                self.accounts.remove(account)
                return
    def saveChangesToJson(self):
        with open(CONFIG_FILE, mode="w+", encoding='utf-8') as configRaw:
            stringDumps = jsons.dumps(obj=self, key_transformer=jsons.KEY_TRANSFORMER_SNAKECASE)
            configRaw.write(stringDumps)
