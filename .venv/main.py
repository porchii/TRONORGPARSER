import logging
import asyncio
from start_driver import Slave
from parser.main import start_cycle
from telegram.main import start_bot_polling
from selenium import webdriver
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    logging.info("Starting selenium server")
    driver = Slave()
    logging.info("Started successfully")
    # Загрузка конфигурации
    with open("config.json") as config:
        config_data = json.load(config)
    minimum_balance = config_data["MINIMUM_BALANCE"]

    bot_task = asyncio.create_task(start_bot_polling(driver))

    # Затем запускаем цикл
    await asyncio.gather(bot_task)

if __name__ == '__main__':
    asyncio.run(main())
