import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
root_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_folder)
print("✅ Root folder added to sys.path:", root_folder)
from locator_finder.finder import SmartFinder
from locator_finder.finder import SmartFinder
import time

# --------- Test functions ---------
def test_dynamic_login():
    print("Starting test_dynamic_login...")

    # Launch Chrome browser
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    print("🚀 Chrome browser launched successfully!")

    driver.get("https://profile.w3schools.com/login")
    driver.maximize_window()

    # Initialize SmartFinder
    finder = SmartFinder(driver)

    # Directory to save screenshots
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    # Function to take screenshot
    def take_screenshot(name):
        path = os.path.join(screenshot_dir, f"{name}.png")
        driver.save_screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    # Enter username
    try:
        username_elem = finder.find_smart_by_keyword("user")
        username_elem.send_keys("test_username")
        print("👤 Username entered successfully")
    except Exception as e:
        print(f"[WARN] Username field not found: {e}")
        take_screenshot("username_error")

    # Enter email
    try:
        email_elem = finder.find_smart_by_keyword("email")
        email_elem.send_keys("test_user@example.com")
        print("✉️ Email entered successfully")
    except Exception as e:
        print(f"[WARN] Email field not found: {e}")
        take_screenshot("email_error")

    # Enter password
    try:
        password_elem = finder.find_smart_by_keyword("pass")
        password_elem.send_keys("dummy123")
        print("🔑 Password entered successfully")
    except Exception as e:
        print(f"[WARN] Password field not found: {e}")
        take_screenshot("password_error")

    # Click login button
    try:
        login_btn = finder.find_smart_by_keyword("sign", tag="button")
        login_btn.click()
        print("✅ Login button clicked")
    except Exception as e:
        print(f"[WARN] Login button not found: {e}")
        take_screenshot("login_button_error")

    # Wait and close
    time.sleep(2)
    driver.quit()
    print("✅ test_dynamic_login completed!\n")


def test_dummy():
    print("Starting test_dummy...")
    time.sleep(1)
    print("✅ test_dummy completed!\n")


# --------- Run all tests automatically ---------
def run_all_tests():
    tests = [func for func in globals() if func.startswith("test_")]
    for test in tests:
        print(f"\n🧪 Running {test}...")
        globals()[test]()  # call the test function


# --------- Main Entry Point ---------
if __name__ == "__main__":
    run_all_tests()