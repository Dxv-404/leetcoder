from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
from daily_fetcher import get_daily_problem_slug, get_question_details
from ai_solver_claude import ask_claude
from extract_code import extract_python_code
from leetcode_submitter import submit_code_to_leetcode
from utils import is_problem_already_solved
from logger import log, send_log_to_discord

load_dotenv()

def main():
    slug = get_daily_problem_slug()
    if is_problem_already_solved(slug):
        log(f"✅ Problem already solved: {slug}")
        return

    question = get_question_details(slug)
    prompt = f"Solve this LeetCode problem in Python 3:\n\nTitle: {question['title']}\n{question['content']}\n\nSample Input: {question['sampleTestCase']}"

    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", False)  # Will auto-close

    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

    reply = ask_claude(prompt, driver)
    if not reply:
        log("⚠️ No reply from Claude.")
        driver.quit()
        return

    code = extract_python_code(reply)
    if not code:
        log("⚠️ No Python code found in Claude's response.")
        driver.quit()
        return

    os.makedirs("solutions", exist_ok=True)
    with open(f"solutions/{slug}.py", "w", encoding="utf-8") as f:
        f.write(code)

    result = submit_code_to_leetcode(slug, code, driver)
    driver.quit()

    if "Accepted" not in result:
        log("🔁 Retrying with new prompt...")
        new_prompt = f"The previous code failed. Please fix this:\n\n{question['title']}\n{question['content']}"
        driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
        new_reply = ask_claude(new_prompt, driver)
        new_code = extract_python_code(new_reply)
        if new_code:
            with open(f"solutions/{slug}_retry.py", "w", encoding="utf-8") as f:
                f.write(new_code)
            submit_code_to_leetcode(slug, new_code, driver)
        driver.quit()

    send_log_to_discord(os.getenv("DISCORD_WEBHOOK"))

if __name__ == "__main__":
    main()
