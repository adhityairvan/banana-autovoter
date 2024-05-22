from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import json

RFBANANA_CPANEL = "https://cp.rfbanana.ru"

def loadConfigAndSettings():
    with open('config.json') as configRaw:
        config = json.load(configRaw)
        usernames = config['usernames']
        cpanelUrl = config.get('cpanel_host', RFBANANA_CPANEL)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    return cpanelUrl, usernames, chrome_options

def login(driver, username):
    usernameInput = driver.find_element(By.NAME, 'username')
    usernameInput.clear()
    usernameInput.send_keys(username)
    usernameInput.send_keys(Keys.RETURN)

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Logout')))

def logout(driver):
    logoutButton = driver.find_element(By.LINK_TEXT, 'Logout')
    logoutButton.click()
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Login')))

def tryVoteAllOption(driver):
    windowHandle = driver.current_window_handle;
    driver.get(RFBANANA_CPANEL + '/index.php?do=user_vote')
    voteButtons = driver.find_elements(By.NAME, 'vote_id')
    for button in voteButtons:
        if(not button.is_enabled()):
            continue
        button.click()
        print("Voted. Cash point added")
        driver.switch_to.window(windowHandle)

usernames = []
cpanelHost, usernames, chrome_options = loadConfigAndSettings()

with webdriver.Chrome(options= chrome_options) as driver:
    print(usernames)
    for username in usernames:
        try:
            driver.delete_all_cookies()
            driver.get(cpanelHost)
            login(driver, username)
            tryVoteAllOption(driver)
            logout(driver)
            print('RF Banana voting for account: ' + username + ' is complete')
        except NoSuchElementException as ex:
            print('Error Auto voting for username: ' + username)
            print('Error happen when searching for things to click. Probably from slow connection to website. Please re run if needed')
    print('Finish voting for all account inputted. Enjoy -NightKnight')