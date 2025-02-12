from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import asyncio
import json
import logging
import asyncio
from parser.main import start_cycle


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Slave():
    def __init__(self):
        # Настраиваем опции для Chrome
        self.current_tasks = []
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # Если нужно запускать без графического интерфейса:
        # user_data_dir = tempfile.mkdtemp()
        # options.add_argument(f"--user-data-dir={user_data_dir}")
        # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # Инициализируем драйвер и сохраняем его в атрибуте экземпляра
        self.driver = webdriver.Chrome(options=options)
        
        # Применяем настройки stealth для обхода детекции
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        logging.info("Драйвер инициализирован и настроен.")
    async def cancel_old_tasks(self):
        for task in self.current_tasks:
            if not task.done():
                task.cancel()  # Отменить задачу
                logging.info("Старая задача отменена.")
        # Очистим список задач
        self.current_tasks = []


    async def confirm(self):
        await self.cancel_old_tasks()
        with open("config.json") as config:
            config_data = json.load(config)
            min_bal = config_data.get("MINIMUM_BALANCE")
        self.driver.get("https://new.p2pbroker.xyz/usdt-payout")
        new_task = asyncio.create_task(start_cycle(min_bal, self.driver))
        self.current_tasks.append(new_task) 

    async def authorize(self):
        await self.cancel_old_tasks()
        """Метод для авторизации на сайте."""
        # Переходим на страницу авторизации
        self.driver.get("https://new.p2pbroker.xyz/sign/in")
        logging.info("Переход на страницу авторизации выполнен.")

        # Загружаем логин и пароль из config.json
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            login = config_data.get("LOGIN")
            password = config_data.get("PASSWD")
            min_bal = config_data.get("MINIMUM_BALANCE")

        # Ждем некоторое время, чтобы страница прогрузилась или чтобы, например, пользователь успел что-то ввести
        await asyncio.sleep(5)

        # Если auth_token обновляется, снова считываем его из файла
        with open("config.json", "r") as config_file:
            config_data = json.load(config_file)
            auth_token = config_data.get("AUTH_TOKEN")

        try:
            # Заполняем форму авторизации
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/main/div/div[2]/form/div[1]/div/input").send_keys(login)
            await asyncio.sleep(1)
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/main/div/div[2]/form/div[2]/div/div[1]/input").send_keys(password)

            await asyncio.sleep(1)
            
            # Заполняем поля с кодом аутентификации (предполагается, что auth_token — строка)
            for pos, c in enumerate(auth_token):
                xpath = f"/html/body/div[1]/div[1]/main/div/div[2]/form/div[3]/div/div[{pos + 1}]/input"
                self.driver.find_element(By.XPATH, xpath).send_keys(c)
                await asyncio.sleep(0.1)
            
            # После авторизации переходим на нужную страницу
            self.driver.get("https://new.p2pbroker.xyz/usdt-payout")
            logging.info("Авторизация выполнена, переход на целевую страницу.")

            # Создаем новую задачу
            new_task = asyncio.create_task(start_cycle(min_bal, self.driver))
            self.current_tasks.append(new_task) 

            
        except Exception as e:
            logging.error(f"Ошибка во время авторизации: {e}")