from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

import json
import os

RFBANANA_CPANEL = "https://cp.rfbanana.ru"

class Account:
    username: str
    password: str
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        pass
    def __str__(self) -> str:
        return self.username

class Config:
    accounts: list[Account] = []
    cpanelUrl: str = RFBANANA_CPANEL
    timeoutLimit: int = 15
    debugMode: bool = False
    def __init__(self, config: dict) -> None:
        for jsonAccount in config.get('accounts'):
            self.accounts.append(Account(jsonAccount.get('username'), jsonAccount.get('password')))
        self.cpanelUrl = config.get('cpanel_host', RFBANANA_CPANEL)
        self.timeoutLimit = config.get('timeout_limit')
        self.debugMode = config.get('debug_mode', False)
        pass

class AutoVoteApp:
    appConfig: Config
    driver: WebDriver
    def __init__(self) -> None:
        with open('config.json') as configRaw:
            config = json.load(configRaw)
            self.appConfig = Config(config)
        chrome_options = webdriver.ChromeOptions()
        if self.appConfig.debugMode is False:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(options= chrome_options)
        pass
    def login(self, account: Account):
        usernameInput = self.driver.find_element(By.NAME, 'username')
        usernameInput.clear()
        usernameInput.send_keys(account.username)

        passwordInput = self.driver.find_element(By.NAME, 'password')
        passwordInput.clear()
        passwordInput.send_keys(account.password)

        usernameInput.send_keys(Keys.RETURN)

        try :
            WebDriverWait(self.driver, self.appConfig.timeoutLimit).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Logout')))
        except TimeoutException:
            raise ValueError

    def logout(self):
        logoutButton = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logoutButton.click()
        WebDriverWait(self.driver, self.appConfig.timeoutLimit).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Login')))

    def tryVoteAllOption(self):
        windowHandle = self.driver.current_window_handle
        self.driver.get(RFBANANA_CPANEL + '/index.php?do=user_vote')
        voteButtons = self.driver.find_elements(By.NAME, 'vote_id')
        for button in voteButtons:
            if(not button.is_enabled()):
                continue
            button.click()
            print("Voted. Cash point added")
            self.driver.switch_to.window(windowHandle)
    def start(self):
        for account in self.appConfig.accounts:
            print(account.__str__(), end=" | ")
        print()
        for account in self.appConfig.accounts:
            try:
                self.driver.delete_all_cookies()
                self.driver.get(self.appConfig.cpanelUrl)
                self.login(account)
                self.tryVoteAllOption()
                self.logout()
                print('RF Banana voting for account: ' + account.username + ' is complete')
            except ValueError:
                print('Failed to login' + account.username + ' or account not exists')
            except (NoSuchElementException , TimeoutException) as ex:
                print('Error Auto voting for username: ' + account.username)
                print('Error happen when searching for things to click. Probably from slow connection to website. Please re run if needed')
        print('Finish voting for all account inputted. Enjoy -NightKnight')
        if self.appConfig.debugMode:
            os.system("pause")

if __name__ == "__main__" :
    autoVoteApp: AutoVoteApp = AutoVoteApp()
    autoVoteApp.start()