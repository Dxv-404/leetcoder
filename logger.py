from datetime import datetime
import os
from discord_webhook import DiscordWebhook

LOG_FILE = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
os.makedirs("logs", exist_ok=True)

def log(msg):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    full_msg = f"{timestamp} {msg}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")

def send_log_to_discord(webhook_url):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        webhook = DiscordWebhook(url=webhook_url, content=f"```\n{f.read()}\n```")
        webhook.execute()
