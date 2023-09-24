# Standard library imports
import string
import time
import random
import os

# Third-party imports
import pandas as pd
import nltk
from nltk.corpus import words
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException


from selenium_utils import click_slow, _input_slow, _input
from metamask_utils import confirm_transaction, create_wallet, swich_to_zora, find_metamask_notification
from browser_calls import start_ads
from logger import SetupGayLogger
from AI_staff import get_image_content, get_image_description

MIN_DELAY = 2500
MAX_DELAY = 3500
ASTICA_API = '966F6BF4-9EAF-49DC-9DDC-47BF3C2A212AC39F730E-8F40-48CE-87DC-264557EA8E12'
OPENAI_API = "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"
IDENTIFICATOR = 'fmbaealjlbbeacofdgmbipcmolohbhhn'
METAMASK_URL = f"chrome-extension://{IDENTIFICATOR}/home.html#"
DATA_PATH = "Data.xlsx"

df = pd.read_excel(DATA_PATH)
profiles = df['Profile ID'].tolist()
passwords = df['Password'].tolist()
seeds = df['Seed'].tolist()

def check_max_trx_reached(df, target):
    for value in df['Value']:
        if value < target:
            return False
    return True


def process_profile(idx, nugger):
    profile_id = profiles[idx]
    password = passwords[idx]
    seed = seeds[idx]

    response = start_ads(profile_id, idx)

    if response["error"]:
        nugger.error(f"Failed to start browser for profile ID {profile_id}. Error Details: {response['error']}")
        return 0

    driver = response["driver"]
    time.sleep(5)

    try:
        initial_window_handle = driver.current_window_handle
        for tab in driver.window_handles:
            if tab != initial_window_handle:
                driver.switch_to.window(tab)
                nugger.info("Closing any extra browser tabs that are open...")
                driver.close()

        driver.switch_to.window(initial_window_handle)

        driver.get(METAMASK_URL)
        time.sleep(3)

        if driver.current_url == f'chrome-extension://{IDENTIFICATOR}/home.html#unlock':
            _input(driver, '//*[@id="password"]', password)
            click_slow(driver, '//*[@id="app-content"]/div/div[3]/div/div/button')
            nugger.info("Unlocking the Metamask wallet...")
        elif driver.current_url == f'chrome-extension://{IDENTIFICATOR}/home.html#initialize/welcome':
            nugger.info("No Metamask wallet found. Attempting to create a new wallet...")
            if create_wallet(idx, driver, seed):
                nugger.info("Successfully created a new Metamask wallet.")
            else:
                nugger.error("Failed to create a new Metamask wallet.")

        swich_to_zora(driver, nugger, IDENTIFICATOR)
        driver.get("https://zora.co/")
        time.sleep(5)
        try:
            element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[1]/div/nav/div[3]/button/div')
            click_slow(driver, '//*[@id="__next"]/div/div[3]/div[1]/div/nav/div[3]/button')
            click_slow(driver, '/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div[2]/div[2]/div[1]/button')

            metamask_notification = find_metamask_notification(driver, nugger)
            if metamask_notification:
                click_slow(driver, '//*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]')
                click_slow(driver, '//*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]')
                driver.switch_to.window(initial_window_handle)
        except NoSuchElementException:
            math = 3+3

        driver.get("https://zora.co/create/single-edition?prev=%2Fcreate%2Fsingle-edition")

        with open("prompt.txt", 'r') as file:
            lines = file.readlines()
        my_line = lines.pop(0).strip()
        if my_line is None:
            nugger.critical("The prompt file is empty!")
            exit(1)
        with open("prompt.txt", 'w') as file:
            file.writelines(lines)

        nugger.info("Generating image content using OpenAI...")
        filename = "path_to_save_image.png"
        absolute_path = os.path.abspath(filename)

        image_path, image_url = get_image_content(my_line, OPENAI_API, absolute_path)
        if image_path and image_url is not None:
            nugger.info("Successfully generated image content.")
            image_input = driver.find_element(By.XPATH,
                                              '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[4]/div/div[2]/div/input')
            image_input.send_keys(image_path)
            time.sleep(10)
            if os.path.exists(image_path):
                os.remove(image_path)
        else:
            nugger.error("Failed to generate image content.")
            return 0

        nugger.info("Generating description for the image content. This may take a while. Please be patient...")

        try:
            description = get_image_description(ASTICA_API, image_url, nugger)
            nugger.info("Obtained image description. Starting input to page.")
            _input_slow(driver, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[3]/textarea',
                        description)
        except Exception:
            nugger.error("Unable to obtain a description for image.")
            return 0

        random_string = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
        _input_slow(driver, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[2]/input', random_string)

        english_words = words.words()
        collection_name = random.choice(english_words).capitalize()

        _input_slow(driver, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[1]/div[1]/div/input',
                    collection_name)
        _input_slow(driver, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[6]/div[2]/div/input', "0")

        nugger.info("Configuring switches to make this shit look legit...")

        button = random.randint(1, 2)
        click_slow(driver, f'//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[7]/div[1]/div/button[{button}]')
        button2 = random.randint(1, 2)
        click_slow(driver, f'//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/div[8]/div[2]/div[1]/div/button[{button2}]')

        click_slow(driver, '//*[@id="__next"]/div/div[3]/div[2]/div/div[2]/div/form/div/button')

        confirm_transaction(driver, nugger, True)
        driver.switch_to.window(initial_window_handle)

        time.sleep(30)
        driver.get('https://zora.co/manage')

        time.sleep(5)

        element = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[3]/div[2]/div/div/div[3]/div[2]/div[1]/a')
        link = element.get_attribute('href')
        if link:
            new_url = link.replace("manage", "collect")
            driver.get(new_url)
        else:
            nugger.error("The 'href' attribute is empty or not found")

        click_slow(driver, '//*[@id="__next"]/div/div[3]/div[4]/main/div[3]/div/div/div[1]/button')
        click_slow(driver, '//*[@id="sidebar"]/footer/div/div[1]/button')
        click_slow(driver, '//*[@id="idle-state-mint"]/div[1]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/button')
        confirm_transaction(driver, nugger, True)
        driver.switch_to.window(initial_window_handle)

        driver.get('https://zora.co/manage')

        click_slow(driver, '//*[@id="__next"]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[1]/div[2]/div/button')
        confirm_transaction(driver, nugger, True)
        driver.switch_to.window(initial_window_handle)
        driver.close()
        return 1

    except Exception as e:
        print(f"An unexpected error occurred - {e}")
        return 0


# Input the range of indices for accounts.
start_idx = 5
end_idx = 99


# Validate the provided indices.
if start_idx > end_idx:
    print("Invalid input!")
    exit(1)

# Infinite loop to continuously mint for eligible accounts.
while True:
    indices = list(range(start_idx, end_idx))
    random.shuffle(indices)

    for idx in indices:
        nugger = SetupGayLogger(f'Account {idx + 1}', False)
        total_trx = df.at[idx, 'Value']

        # Check if the account has already minted 7 times.
        if total_trx >= 1:
            nugger.info(f"Account {idx + 1} already Done. Skipping...")
            time.sleep(0.1)
            continue

        # Check if all accounts have reached the max transaction limit.
        if check_max_trx_reached(df, 1):
            nugger.error("Action is done for all seed. Stopping process...")
            exit(1)

        try:
            result = process_profile(idx, nugger)  # Adjusting for zero-based indexing
        except Exception as e:
            print(e)
            time.sleep(5)
            continue

        if result == 1:
            df.at[idx, 'Value'] = 1
            df.to_excel(DATA_PATH, index=False)
            S = round(random.uniform(MIN_DELAY, MAX_DELAY))
            nugger.info(f"Sleep for {S} second before next operation")
            time.sleep(S)
            break

