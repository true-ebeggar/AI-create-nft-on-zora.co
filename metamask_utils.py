import random
import string
import threading
import time
import pandas as pd
from selenium.common import NoSuchElementException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_utils import click_fast, _input, click_slow, _input_slow


lock = threading.Lock()
DATA_PATH = "Data.xlsx"
df = pd.read_excel(DATA_PATH)


def confirm_transaction(driver, logger, zora=False):
    metamask_window_handle = find_metamask_notification(driver, logger)

    if metamask_window_handle:
        if zora == 1:
            logger.info("Setting gas values for zora...")
            time.sleep(3)
            click_slow(driver, '//*[@id="app-content"]/div/div[2]/div/div[5]/div[2]/div/div/div/div[1]/button')
            click_slow(driver, '//*[@id="popover-content"]/div/div/section/div[2]/div/div[2]/div[1]/button')
            gas = str(f"{random.uniform(0.05, 0.06):.5f}")
            _input_slow(driver,
                   '//*[@id="popover-content"]/div/div/section/div[2]/div/div[2]/div[1]/div[3]/div[2]/label/div[2]/input',
                   gas)
            _input_slow(driver,
                   '//*[@id="popover-content"]/div/div/section/div[2]/div/div[2]/div[1]/div[3]/div[3]/label/div[2]/input',
                   gas)
            click_slow(driver, '//*[@id="popover-content"]/div/div/section/div[3]/button')
            logger.info("Gas values set successfully.")

        find_confirm_button_js = '''
        function findConfirmButton() {
          return document.querySelector('[data-testid="page-container-footer-next"]');
        }
        return findConfirmButton();
        '''
        confirm_button = driver.execute_script(find_confirm_button_js)

        if confirm_button:
            for i in range(5):
                if metamask_window_handle not in driver.window_handles:
                    logger.info("Transaction approved successfully!")
                    return True
                logger.info(f"Attempting to click the confirm button ({i + 1}/5)...")
                driver.execute_script("arguments[0].click();", confirm_button)
                time.sleep(3)
            return True
        else:
            logger.warning("Unable to find the 'Confirm' button in MetaMask.")
            return False
    else:
        logger.warning(f"MetaMask Notification window not found")
        return False
def swich_to_base(driver, logger, IDENTIFICATOR):
    driver.get(f"chrome-extension://{IDENTIFICATOR}/home.html#")
    click_slow(driver, '//*[@id="app-content"]/div/div[1]/div/div[2]/div/div')
    time.sleep(5)

    try:
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'Base')]")
        click_slow(driver, "//*[contains(text(), 'Base')]")
        logger.info("Switched to the Base network...")
    except NoSuchElementException:
        click_slow(driver, "//*[contains(text(), 'Ethereum Mainnet')]")
        logger.info("Base network isn't added. Setting it up now...")
        driver.get(f"chrome-extension://{IDENTIFICATOR}/home.html#settings/networks/add-network")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input',
               "Base")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/label/input',
               "https://developer-access-mainnet.base.org")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/label/input',
               "8453")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/label/input',
               "ETH")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/label/input',
               "https://basescan.org")
        time.sleep(2)
        click_slow(driver, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]')
def swich_to_zora(driver, logger, IDENTIFICATOR):
    driver.get(f"chrome-extension://{IDENTIFICATOR}/home.html#")
    click_slow(driver, '//*[@id="app-content"]/div/div[1]/div/div[2]/div/div')
    time.sleep(3)

    try:
        element = driver.find_element(By.XPATH, "//*[contains(text(), 'Zora')]")
        click_slow(driver, "//*[contains(text(), 'Zora')]")
        logger.info("Switched to the Zora network...")
    except NoSuchElementException:
        click_slow(driver, "//*[contains(text(), 'Ethereum Mainnet')]")
        logger.info("Zora network isn't added. Setting it up now...")
        driver.get(f"chrome-extension://{IDENTIFICATOR}/home.html#settings/networks/add-network")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input',
               "Zora")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/label/input',
               "https://rpc.zora.energy/")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/label/input',
               "7777777")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/label/input',
               "ETH")
        _input(driver, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/label/input',
               "https://explorer.zora.energy/")
        time.sleep(2)
        click_slow(driver, '/html/body/div[1]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]')
def generate_password(length):
    if length < 8:
        print("Password length should be at least 8")
        return None

    all_characters = string.ascii_letters + string.digits + string.punctuation

    password = []
    password.append(random.choice(string.ascii_lowercase))
    password.append(random.choice(string.ascii_uppercase))
    password.append(random.choice(string.digits))
    password.append(random.choice(string.punctuation))

    for i in range(length - 4):
        password.append(random.choice(all_characters))

    random.shuffle(password)

    password_string = "".join(password)
    return password_string
def create_wallet(idx, driver, seed):
    try:
        click_fast(driver, '//*[@id="app-content"]/div/div[2]/div/div/div/button')
        click_fast(driver, '//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]')
        click_fast(driver, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button')
        seed_words = seed.split()
        for i, word in enumerate(seed_words):
            seed_word_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="import-srp__srp-word-{i}"]')))
            seed_word_input.send_keys(word)

        password = str(generate_password(32))
        _input(driver, '//*[@id="password"]', password)
        _input(driver, '//*[@id="confirm-password"]', password)
        with lock:
            df.loc[df.index[idx], 'Password'] = password
            df.to_excel(DATA_PATH, index=False)
        click_fast(driver, '//*[@id="create-new-vault__terms-checkbox"]')
        click_fast(driver, '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button')
        click_fast(driver, '//*[@id="app-content"]/div/div[2]/div/div/button')

        click_fast(driver, '//*[@id="tippy-tooltip-2"]/div/div[2]/div/div[1]/button')
        driver.refresh()
        click_fast(driver, '//*[@id="popover-content"]/div/div/section/div[1]/div/button')
        driver.refresh()
        click_fast(driver, '//*[@id="popover-content"]/div/div/section/div[1]/div/button')
        click_fast(driver, '//*[@id="popover-content"]/div/div/section/div[2]/div/div[2]/div/button')
        return True
    except Exception as e:
        print(f"{e}")
        return False
def find_metamask_notification(driver, logger):
    metamask_window_handle = None

    for attempt in range(30):

        time.sleep(1)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if 'MetaMask Notification' in driver.title:
                metamask_window_handle = handle
                logger.info("Found MM notification window!")
                break

        if metamask_window_handle:
            break

    return metamask_window_handle