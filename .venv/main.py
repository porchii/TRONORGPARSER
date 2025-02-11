import logging
import asyncio
from start_driver import init, authorize
from parser.main import start_cycle
from telegram.main import start_bot_polling
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    # Инициализация драйвера с повторными попытками
    while True:
        try:
            driver = init()
            break
        except Exception as e:
            logging.error(f"Error while initializing driver: {e}")
            await asyncio.sleep(1)
    logging.info("Driver initialized successfully")

    # Загрузка конфигурации
    with open("config.json") as config:
        config_data = json.load(config)
    minimum_balance = config_data["MINIMUM_BALANCE"]

    # Запускаем бота как фоновую задачу, чтобы он не блокировал выполнение:
    bot_task = asyncio.create_task(start_bot_polling())
    logging.info("Bot polling started in background")

    # Если необходимо, можно подождать немного, чтобы бот успел инициализироваться:
    await asyncio.sleep(1)

    # Выполняем авторизацию (после запуска бота)
    await authorize(driver)
    logging.info("Authorization completed")

    # Затем запускаем цикл
    await start_cycle(minimum_balance, driver)

if __name__ == '__main__':
    asyncio.run(main())
