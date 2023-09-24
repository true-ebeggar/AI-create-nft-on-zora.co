import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeDriverService
from selenium.webdriver.chrome.options import Options


def start_ads(profile_id, idx):
    result = {"driver": None, "error": None}

    try:
        open_url = f"http://local.adspower.net:50325/api/v1" \
                   f"/browser/start?user_id={profile_id}"

        resp = requests.get(open_url).json()
        if resp["code"] != 0:
            result["error"] = resp["msg"]
            return result

        chrome_driver = resp["data"]["webdriver"]
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress",
                                               resp["data"]["ws"]["selenium"])
        if idx == 0:
            driver = webdriver.Chrome(service=chrome_driver, options=chrome_options)
        else:
            driver = webdriver.Chrome(service=ChromeDriverService(chrome_driver), options=chrome_options)

        initial_window_handle = driver.current_window_handle
        for tab in driver.window_handles:
            if tab != initial_window_handle:
                driver.switch_to.window(tab)
                driver.close()
        driver.switch_to.window(initial_window_handle)

        result["driver"] = driver

    except Exception as e:
        result["error"] = str(e)

    return result
def start_dolphin(profile_id):
    result = {"driver": None, "error": None}

    try:
        req_url = f'http://localhost:3001/v1.0/' \
                  f'browser_profiles/{profile_id}/start?automation=1'
        response = requests.get(req_url)
        response_json = response.json()

        port = str(response_json['automation']['port'])
        options = webdriver.ChromeOptions()
        options.debugger_address = f'127.0.0.1:{port}'
        driver = webdriver.Chrome(options=options)

        initial_window_handle = driver.current_window_handle
        for tab in driver.window_handles:
            if tab != initial_window_handle:
                driver.switch_to.window(tab)
                driver.close()
        driver.switch_to.window(initial_window_handle)

        result["driver"] = driver

    except Exception as e:
        result["error"] = str(e)

    return result