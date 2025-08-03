from logger import log
import time
from selenium.webdriver.common.by import By
from leetcode_login import login_to_leetcode

def submit_code_to_leetcode(slug, code, driver):
    log(f"Navigating to problem page: {slug}")
    driver.get(f"https://leetcode.com/problems/{slug}/")
    time.sleep(10)

    if "login" in driver.current_url:
        log("⚠️ Not logged in, attempting auto-login...")
        login_to_leetcode(driver)

    try:
        log("Injecting code into LeetCode editor...")
        editor = driver.find_element(By.CLASS_NAME, "view-lines")
        editor.click()

        driver.execute_script("""
            document.querySelector('.monaco-editor textarea').value = arguments[0];
        """, code)

        run_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
        run_btn.click()

        log("Clicked Submit. Waiting for result...")
        time.sleep(20)

        result = driver.find_element(By.CLASS_NAME, "success__3Ai7").text
        log(f"Submission result: {result}")
        return result
    except Exception as e:
        log(f"❌ Submission error: {e}")
        return None
