# gmail_verification_handler.py
import os
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
from discord_logger import log

load_dotenv()

GMAIL_EMAIL = os.getenv("GMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def extract_verification_code_from_email(driver):
    log("📨 Opening Gmail tab...")
    driver.execute_script("window.open('https://mail.google.com', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)

    try:
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_input.send_keys(GMAIL_EMAIL)
        email_input.send_keys(Keys.ENTER)
        log("📧 Entered Gmail email.")
    except TimeoutException:
        log("⚠️ Gmail email input not found (might already be logged in).")

    time.sleep(3)
    try:
        password_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(GMAIL_PASSWORD)
        password_input.send_keys(Keys.ENTER)
        log("🔐 Entered Gmail password.")
    except TimeoutException:
        log("⚠️ Gmail password input not found (might already be logged in).")

    time.sleep(10)
    log("🔎 Looking for Claude verification email...")

    for attempt in range(6):
        try:
            search_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail']"))
            )
            search_box.clear()
            search_box.send_keys("from:no-reply@claude.ai")
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)

            top_email = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//tr[@jscontroller][1]"))
            )
            top_email.click()
            log("📨 Opened top Claude email.")
            break
        except Exception:
            log(f"🔁 Email not found yet, retrying ({attempt+1}/6)...")
            time.sleep(10)
    else:
        log("❌ Claude verification email not found after retries.")
        return None

    time.sleep(5)
    try:
        body = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='listitem' or @dir='ltr']"))
        )
        text = body.text
        code_match = re.search(r"\\b(\\d{6})\\b", text)
        if code_match:
            code = code_match.group(1)
            log(f"✅ Extracted verification code: {code}")
        else:
            log("❌ Code not found in email body.")
            code = None
    except TimeoutException:
        log("❌ Could not read email body for code.")
        code = None

    driver.switch_to.window(driver.window_handles[0])
    log("↩️ Switched back to Claude tab.")
    return code