import os
from queue import Queue

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

from src.modules.dataclass.account import Account
from src.modules.dataclass.textMessage import TextMessage
from src.modules.dataclass.votingProcessMessage import VotingProcessMessage
from src.modules.configuration.config import Config
from src.modules.configuration.config import RFBANANA_CPANEL

class AutoVoteApp:
    appConfig: Config
    driver: WebDriver
    queue: Queue
    def __init__(self, queue: Queue) -> None:
        self.appConfig = Config()
        chromeOptions = webdriver.ChromeOptions()
        if self.appConfig.debugMode is False:
            chromeOptions.add_argument('--headless')
        chromeOptions.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(options= chromeOptions)
        self.queue = queue

    def login(self, account: Account):
        usernameInput = self.driver.find_element(By.NAME, 'username')
        usernameInput.clear()
        usernameInput.send_keys(account.username)

        passwordInput = self.driver.find_element(By.NAME, 'password')
        passwordInput.clear()
        passwordInput.send_keys(account.password)

        usernameInput.send_keys(Keys.RETURN)

        try :
            WebDriverWait(self.driver,
                          self.appConfig.timeoutLimit).until(
                              EC.visibility_of_element_located((By.LINK_TEXT, 'Logout')))
        except TimeoutException as exc:
            raise ValueError from exc

    def logout(self):
        logoutButton = self.driver.find_element(By.LINK_TEXT, 'Logout')
        logoutButton.click()
        WebDriverWait(self.driver, 
                      self.appConfig.timeoutLimit).until(
                          EC.visibility_of_element_located((By.LINK_TEXT, 'Login')))

    def tryVoteAllOption(self):
        windowHandle = self.driver.current_window_handle
        self.driver.get(RFBANANA_CPANEL + '/index.php?do=user_vote')
        voteButtons = self.driver.find_elements(By.NAME, 'vote_id')
        for button in voteButtons:
            if not button.is_enabled():
                continue
            button.click()
            self.print("Voted. Cash point added")
            self.driver.switch_to.window(windowHandle)
    def start(self):
        if len(self.appConfig.accounts) == 0:
            self.print('No account inputted. Please input account first')
            self.queue.put(VotingProcessMessage("voting", 1, 1, list()))
            return
        numProcessed: int = 0
        for account in self.appConfig.accounts:
            try:
                self.driver.delete_all_cookies()
                self.driver.get(self.appConfig.cpanelUrl)
                self.login(account)
                self.tryVoteAllOption()
                self.logout()
                self.print('RF Banana voting for account: ' + account.username + ' is complete')
            except ValueError:
                self.print('Failed to login' + account.username + ' or account not exists')
            except (NoSuchElementException , TimeoutException):
                self.print('Error Auto voting for username: ' + account.username)
                self.print('Error happen when searching for things to click. Probably from slow connection to website. Please re run if needed')
            numProcessed += 1
            self.queue.put(
                VotingProcessMessage("voting", len(self.appConfig.accounts), numProcessed, list()))
        self.print('Finish voting for all account inputted. Enjoy -NightKnight')
        if self.appConfig.debugMode:
            os.system("pause")
    def print(self, input: str):
        self.queue.put(TextMessage("voting", input))
        