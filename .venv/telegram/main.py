from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from start_driver import Slave
import logging
import json

driver = Slave()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Form(StatesGroup):
    wallet_token = State()
    minimum_balance = State()

    get_login = State()
    get_password = State()
    get_auth_token = State()

with open("config.json") as config:
    config_data = json.load(config)
    token = config_data["BOT_TOKEN"]

bot = Bot(token)
dp = Dispatcher()

@dp.message(F.text=='/start')
async def start_command(message: Message):

    keyboard = [
        [
            KeyboardButton(text="Ввести новый токен кошелька")
        ],
        [
            KeyboardButton(text="Минимальный баланс для создания заявки")
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

    await message.answer("Привет! Вот доступные действия:", reply_markup=reply_markup)

@dp.message(F.text=='Ввести новый токен кошелька')
async def wallet_token_command(message: Message, state: FSMContext):
    await message.answer(f"Введите новый токен.")
    await state.set_state(Form.wallet_token)

@dp.message(Form.wallet_token)
async def wallet_token_handler(message: Message, state: FSMContext):
    wallet_token = message.text

    with open("config.json") as config:
        config_data = json.load(config)
        config_data["TOKEN"] = wallet_token
        with open("config.json", "w") as config:
            json.dump(config_data, config)
    await message.answer(f"Токен кошелька успешно изменен.")
    await state.clear()

@dp.message(F.text=='Минимальный баланс для создания заявки')
async def minimum_balance_command(message: Message, state: FSMContext):
    await message.answer(f"Введите минимальный баланс для создания заявки.")
    await state.set_state(Form.minimum_balance)


@dp.message(Form.minimum_balance)
async def minimum_balance_handler(message: Message, state: FSMContext):
    try:
        minimum_balance = int(message.text)
    except ValueError:
        await message.answer("Необходимо ввести числовое значение.")
        return
    with open("config.json") as config:
        config_data = json.load(config)
        config_data["MINIMUM_BALANCE"] = minimum_balance
        with open("config.json", "w") as config:
            json.dump(config_data, config)

    await message.answer("Минимальный баланс успешно определен.")
    await state.clear()
@dp.message(Command("auth"))
async def get_auth_token_handler(message: Message):
    try:
        auth_token = message.text.split()[1]
        message.answer("auth_token: {auth_token}")
    except IndexError:
        await message.answer("Необходимо ввести код аутентификации.")
        return
    with open("config.json") as config:
        config_data = json.load(config)
        config_data["AUTH_TOKEN"] = auth_token
        with open("config.json", "w") as config:
            json.dump(config_data, config)
    await message.answer("Код аутентификации успешно введен.")
    
    try:
        await driver.authorize()
    except Exception as e:
        await message.answer(f"Ошибка авторизации: {e}")
    
@dp.message(Command("confirm"))
async def confirm_handler(message: Message):
    try:
        await driver.confirm()
        await message.answer("Данные для парсера обновлены")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def start_bot_polling(Driver: Slave):
    global driver
    driver = Driver
    await dp.start_polling(bot)