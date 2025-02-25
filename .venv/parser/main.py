from parser.parse import get_current_usdt
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import asyncio
import logging
from parser.go import send_request
from telegram.notify import send_notifty

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def start_cycle(min_bal: int, driver) -> None:
    
    while True:
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.LINUX.value]   
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        try:    
                balance = await get_current_usdt(user_agent)
                logging.info(f"UST Balance is {balance})")
                if driver.current_url != "https://new.p2pbroker.xyz/usdt-payout":
                     send_notifty("Бота редиректнуло, нужно авторизироваться заново")
                     break
                if balance >= min_bal:
                    logging.info("Sending request...")
                    try: 
                        await send_request(driver, min_bal)
                        logging.info("Request sent successfully")
                        send_notifty('Заявка "создана". Чтобы снова начать мониторинг введите /confir для подтверждения данных мониторинга')
                        break
                    except Exception as e:
                          logging.error(f"Error while sending request: {e}")
                          continue
        except Exception as e:
                logging.error(f"Error while fetching balance: {e}")
                continue
        await asyncio.sleep(0.2)
