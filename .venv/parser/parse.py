import json
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def get_token_from_json() -> str:
    with open('config.json', 'r') as f:
        data = json.load(f)
        return data['TOKEN']
    return None

async def get_current_usdt(user_agent) -> int:
    headers = {
        'User-Agent': user_agent,
    }
    token = await get_token_from_json()
    url = f"https://apilist.tronscan.org/api/account?address={token}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    tokens = data.get("trc20token_balances", [])

    usdt_balance = 0
    for token in tokens:
        if "tether usd" in token.get("tokenName", "").lower():
            usdt_balance = int(token.get("balance", 0)) / 1_000_000
            break

    return usdt_balance