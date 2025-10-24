from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SmartFinder:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout  # seconds

    def find_smart_by_keyword(self, keyword, tag=None):
        # Friendly keyword mapping
        mapping = {
            "user": "modalusername",
            "email": "modalusername",
            "pass": "current-password",
            "password": "current-password",
            "login": "Log in",
            "sign": "Log in"
        }

        if keyword in mapping:
            keyword = mapping[keyword]

        strategies = [
            (By.ID, keyword),
            (By.NAME, keyword),
            (By.CLASS_NAME, keyword),
            (By.XPATH, f"//{tag}[contains(text(), '{keyword}')]" if tag else f"//*[contains(text(), '{keyword}') or contains(@id,'{keyword}') or contains(@name,'{keyword}')]"),
            (By.CSS_SELECTOR, f"{tag}[name*='{keyword}']" if tag else f"[name*='{keyword}']"),
        ]

        for by, value in strategies:
            try:
                elem = WebDriverWait(self.driver, self.timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                return elem
            except:
                continue

        raise Exception(f"[ERROR] Cannot find any element for keyword: '{keyword}' with tag='{tag}'")
