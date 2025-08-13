import os
import requests
import time
import telegram
from datetime import datetime

# Variables d'environnement
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
ETHERSCAN_API = os.getenv("ETHERSCAN_API")
WALLETS = os.getenv("WALLETS").split(",")  # adresses séparées par des virgules

# Initialisation du bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_eth_transactions(wallet):
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet}&sort=desc&apikey={ETHERSCAN_API}"
    try:
        r = requests.get(url)
        data = r.json()
        if data["status"] == "1":
            return data["result"]
        else:
            return []
    except Exception as e:
        print(f"Erreur requête : {e}")
        return []

def format_transaction(tx):
    value_eth = int(tx["value"]) / 10**18
    timestamp = datetime.utcfromtimestamp(int(tx["timeStamp"])).strftime('%Y-%m-%d %H:%M:%S')
    return f"💸 Transaction détectée\n\nHash: {tx['hash']}\nMontant: {value_eth:.4f} ETH\nDe: {tx['from']}\nÀ: {tx['to']}\nDate: {timestamp} UTC"

def main():
    print("Bot démarré...")
    last_seen = {wallet: None for wallet in WALLETS}

    while True:
        for wallet in WALLETS:
            txs = get_eth_transactions(wallet)
            if txs:
                latest_tx = txs[0]
                if last_seen[wallet] != latest_tx["hash"]:
                    last_seen[wallet] = latest_tx["hash"]
                    bot.send_message(chat_id=CHAT_ID, text=format_transaction(latest_tx))
        time.sleep(60)  # vérifie toutes les 60 secondes

if __name__ == "__main__":
    main()
