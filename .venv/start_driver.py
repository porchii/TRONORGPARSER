from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import asyncio
import json
from telegram.main import ask_auth_token
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def init():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    return driver

async def authorize(driver: webdriver):
    driver.get("https://new.p2pbroker.xyz/sign/in")

    with open("config.json") as config:
        config_data = json.load(config)
        login = config_data["LOGIN"]
        password = config_data["PASSWD"]
    
    await ask_auth_token()

    await asyncio.sleep(10)
    with open("config.json") as config:
        config_data = json.load(config)
        auth_token = config_data["AUTH_TOKEN"]
        with open("config.json", "w") as config:
            json.dump(config_data, config)
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/main/div/div[2]/form/div[1]/div/input").send_keys(login)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/main/div/div[2]/form/div[2]/div/div[1]/input").send_keys(password)
        for (pos, c) in enumerate(auth_token):
                driver.find_element(By.XPATH, f"/html/body/div[1]/div[1]/main/div/div[2]/form/div[3]/div/div[{pos + 1}]/input").send_keys(c)
        driver.get("https://new.p2pbroker.xyz/usdt-payout")
        
    except Exception as e:
        logging.error(f"Error while authorizing: {e}")
        