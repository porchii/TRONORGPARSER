Чтобы использовать, нужно установить необходимые библиотеки:
```
pip install selenium selenium-stealth logging asyncio json aiogram random_user_agent
```
Также требуется установить chromedriver и chromium browser
На Linux(Ubuntu):
https://skolo.online/documents/webscrapping/

На Windows:
https://medium.com/@patrick.yoho11/installing-selenium-and-chromedriver-on-windows-e02202ac2b08

Как пользоваться?

Для начала нужно создать ```config.json``` с основной информацией о вашем аккаунте:

config.json (Example):
```yaml
{
"TOKEN": "1",
 "BOT_TOKEN": "ТОКЕН", // ПОЛУЧАЕТСЯ У BOT_FATHER
 "MINIMUM_BALANCE": 1000000, // МИНИМАЛЬНЫЙ БАЛАНС ДЛЯ ПАРСИНГА
 "LOGIN": "ЛОГИН ОТ АККАУНТА", // ЛОГИН ОТ АККАУНТА
 "PASSWD": "ПАРОЛЬ", // ПАРОЛЬ ОТ АККАУНТА
 "AUTH_TOKEN": "1" // ОСТАВИТЬ ТАК ПО УМОЛЧАНИЮ
}
```

После запуская с помощью ```python3 main.py```, вы должны открыть телграм с ботом, токен которого указали в ```config.json```, далее вам доступны следующие команды:

/auth - Ввести код из GOOGLE AUTHETICATOR, чтобы зарегистрировать бота

/confirm - Подтвердить указанные данные, которые вы меняли в боте (Обязательно после указания значений в Телеграм Боте) !!!Можно использовать только тогда, когда выполнена авторизация!!!


После ```/auth``` бот начинает мониторинг баланса. Когда баланс >= нужного, происходит отправка заявки 




