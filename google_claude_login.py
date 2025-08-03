import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from discord_logger import log
from gmail_verification_handler import extract_verification_code_from_email
import os


def login_to_claude_with_google(driver):
    log("🔐 Claude login required. Attempting automated login via Google...")

    try:
        driver.get("https://claude.ai/login")
        time.sleep(3)
        log("🌐 Navigating to Claude.ai login page...")

        # Click "Continue with Google"
        try:
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Sign in')]"))
            )
            sign_in_button.click()
        except:
            log("⚠️ 'Sign in' button not found. Maybe already logged in.")
            return True

        time.sleep(2)
        google_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue with Google')]"))
        )
        google_button.click()
        log("🖱 Clicking 'Continue with Google' button...")
        time.sleep(5)

        # Try to click saved Gmail account (if shown)
        try:
            log("📧 Checking if account chooser appears...")
            saved_account = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-identifier]"))
            )
            saved_account.click()
            log("✅ Selected saved Google account.")
        except:
            # Fallback to entering email manually
            log("⌨️ Entering email manually...")
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            email_field.send_keys(os.environ.get("GMAIL_EMAIL"))
            driver.find_element(By.XPATH, "//span[contains(., 'Next')]").click()
            time.sleep(3)

        # Enter password if prompted
        try:
            log("🔐 Entering password...")
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.send_keys(os.environ.get("GMAIL_PASSWORD"))
            driver.find_element(By.XPATH, "//span[contains(., 'Next')]").click()
            time.sleep(6)
        except Exception as e:
            log("❌ Password input not found.")
            raise e

        # Handle verification code
        try:
            otp_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @aria-label='Enter code']"))
            )
            log("📨 Fetching verification code from Gmail...")
            verification_code = extract_verification_code_from_email(driver)
            if verification_code:
                otp_input.send_keys(verification_code)
                driver.find_element(By.XPATH, "//span[contains(., 'Next') or contains(., 'Verify')]").click()
                log(f"✅ Verification code entered successfully: `{verification_code}`")
            else:
                log("❌ Could not fetch verification code from Gmail.")
                return False
        except Exception as otp_err:
            log("❌ Error handling verification code.")
            print(otp_err)
            return False

        time.sleep(5)
        log("✅ Google login flow complete.")
        return True

    except Exception as e:
        log(f"❌ Automated login failed: `{e}`")
        return False
