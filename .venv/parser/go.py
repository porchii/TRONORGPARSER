import asyncio
from selenium.webdriver.common.by import By

async def send_request(driver, amount):
    await asyncio.sleep(1)
    driver.find_element(By.XPATH, f"/html/body/div[1]/div/div/div/main/div/div[1]/div/div[2]/button[2]/span/span").click()
    driver.find_element(By.XPATH, f"/html/body/div[3]/div/div/div[2]/section/div/form/div/div[1]/div/input") \
    .send_keys("1")
    driver.find_element(By.XPATH, f"/html/body/div[3]/div/div/div[2]/section/div/form/div/div[2]/div/input").send_keys(f"{amount}")  # Задержка перед отправкой запроса
    driver.find_element(By.XPATH, f"/html/body/div[3]/div/div/div[2]/section/div/form/div/div[3]/button/span/span").click()
    driver.get("https://new.p2pbroker.xyz/usdt-payout")