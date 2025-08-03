import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import time
from logger import log

load_dotenv()

def login_to_leetcode(driver):
    log("Navigating to LeetCode login page...")
    driver.get("https://leetcode.com/accounts/login/")
    time.sleep(10)

    try:
        email_input = driver.find_element(By.ID, "id_login")
        password_input = driver.find_element(By.ID, "id_password")
        remember_checkbox = driver.find_element(By.ID, "id_remember")

        email_input.send_keys(os.getenv("LEETCODE_EMAIL"))
        password_input.send_keys(os.getenv("LEETCODE_PASSWORD"))
        remember_checkbox.click()
        password_input.send_keys(Keys.ENTER)
        log("Submitted login form.")
    except Exception as e:
        log(f"Login error: {e}")
        return False

    time.sleep(10)
    if "leetcode.com" in driver.current_url:
        log("✅ Logged in successfully.")
        return True
    return False
