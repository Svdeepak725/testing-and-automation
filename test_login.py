"""
Full Selenium automation script for login:
- Positive test (valid credentials)
- Negative tests (empty fields, wrong credentials)
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ---------- CONFIG ----------
TARGET_URL = "https://profile.w3schools.com/login?redirect_url=https%3A%2F%2Fspaces.w3schools.com%2Fspace%2F"  # <-- Replace with your login page URL
TIMEOUT = 15
SCREENSHOT_ON_FAIL = "login_fail.png"

# ---------- CREDENTIALS ----------
VALID_EMAIL = "testuser@example.com"      # Replace with valid email
VALID_PASSWORD = "MySecurePass123"        # Replace with valid password

# Negative test cases
negative_cases = [
    {"email": "", "password": VALID_PASSWORD, "desc": "Empty email"},
    {"email": VALID_EMAIL, "password": "", "desc": "Empty password"},
    {"email": "wronguser@example.com", "password": "wrongpass", "desc": "Wrong email and password"},
]

# ---------- FUNCTIONS ----------
def create_driver(headless=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def run_login_test(driver, wait, email_input, password_input, description="Test"):
    """Run a single login attempt"""
    print(f"\nRunning test: {description}")
    driver.get(TARGET_URL)

    # Locate elements
    form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.LoginForm_login_form__NDkUT")))
    email = form.find_element(By.NAME, "email")
    password = form.find_element(By.NAME, "password")
    submit = form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    error_div = form.find_element(By.CSS_SELECTOR, "div.LoginForm_error_text__4fzmN")

    # Fill form
    email.clear()
    email.send_keys(email_input)
    password.clear()
    password.send_keys(password_input)
    time.sleep(0.3)

    # Submit
    submit.click()

    # Wait/check error message
    try:
        wait.until(lambda d: error_div.text.strip() != "")
        print(f"Result: {error_div.text.strip()}")
    except:
        print("No error message appeared — check if login succeeded")
        driver.save_screenshot(SCREENSHOT_ON_FAIL)
        print("Screenshot saved:", SCREENSHOT_ON_FAIL)

    time.sleep(1)

def test_full_login_suite():
    driver = create_driver(headless=False)
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # -------- Positive test ----------
        run_login_test(driver, wait, VALID_EMAIL, VALID_PASSWORD, "Positive test (valid credentials)")

        # -------- Negative tests ----------
        for case in negative_cases:
            run_login_test(driver, wait, case["email"], case["password"], f"Negative test: {case['desc']}")

    except Exception as e:
        print("Error during login suite:", e)
    finally:
        driver.quit()
        print("\nBrowser closed. All tests finished.")

# ---------- RUN ----------
if __name__ == "__main__":
    print("Starting full login test suite...")
    test_full_login_suite()
