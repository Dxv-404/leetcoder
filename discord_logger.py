# discord_logger.py
from discord_webhook import DiscordWebhook
from datetime import datetime
import os

LOG_FILE = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
os.makedirs("logs", exist_ok=True)

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def log(msg):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    full_msg = f"{timestamp} {msg}"
    print(full_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(full_msg + "\n")
    
    if DISCORD_WEBHOOK:
        try:
            webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=full_msg)
            webhook.execute()
        except Exception as e:
            print("[Discord Error]", e)

# Use in any module:
# from discord_logger import log
# log("🔐 Logging into Google...")
