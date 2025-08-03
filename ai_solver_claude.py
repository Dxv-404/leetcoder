# ai_solver_claude.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from discord_logger import log
from google_claude_login import login_to_claude_with_google

def wait_for_claude_ready(driver):
    for _ in range(90):
        try:
            textarea = driver.find_element(By.TAG_NAME, "textarea")
            if textarea.is_displayed() and textarea.is_enabled():
                return textarea
        except:
            pass
        time.sleep(1)
    return None

def ask_claude(prompt, driver):
    log("🌐 Opening Claude.ai...")
    driver.get("https://claude.ai/chats")
    time.sleep(5)

    if "login" in driver.current_url:
        log("🔐 Claude login required. Attempting automated login via Google...")
        success = login_to_claude_with_google(driver)
        if not success:
            log("❌ Automated login failed. Aborting Claude interaction.")
            return None

    textarea = wait_for_claude_ready(driver)
    if not textarea:
        log("❌ Claude textarea not available. Aborting.")
        return None

    log("⌨️ Typing prompt into Claude...")
    textarea.send_keys(prompt)
    textarea.send_keys(Keys.ENTER)

    log("⏳ Waiting for Claude's response...")
    time.sleep(35)

    try:
        messages = driver.find_elements(By.CLASS_NAME, "prose")
        reply_text = messages[-1].text if messages else None
        log("✅ Claude reply received.")
        return reply_text
    except Exception as e:
        log(f"❌ Claude reply read failed: {e}")
        return None
