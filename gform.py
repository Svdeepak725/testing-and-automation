from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
from datetime import datetime
import time
import os
import random

# --- Excel setup ---
excel_file = "data.xlsx"
sheet_name = "Sheet1"

wb = openpyxl.load_workbook(excel_file)
sheet = wb[sheet_name]

# --- Chrome setup ---
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# --- Folder to save screenshots ---
screenshot_folder = "screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# --- Loop through Excel rows ---
for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
    print(f"\n Filling form for row {idx}...")
    driver.get("https://forms.gle/WT68aV5UnPajeoSc8")
    code_span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.M7eMe b")))
    code_text = code_span.text
    text_inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text'], textarea")))

   
    form_data = [
        row[0],         
        str(row[1]),     
        row[2],          
        row[3],          
        str(row[4]),     
        row[6],          
        code_text        
    ]
    for i, value in enumerate(form_data):
        try:
            element = text_inputs[i]
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(random.uniform(0.5, 1.0))
            element.click()
            element.clear()
            element.send_keys(value)
            print(f"✅ Filled field {i+1}: {value}")
            time.sleep(random.uniform(0.3, 0.7))
        except IndexError:
            print(f"⚠️ Skipped: No input found for '{value}' (index {i})")

    try:
        date_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='date']")))
        time.sleep(1)
        dob_excel = row[5]
        dob_iso = datetime.strptime(dob_excel, "%d-%m-%Y").strftime("%Y-%m-%d")

        driver.execute_script("""
            const el = arguments[0];
            const value = arguments[1];
            el.value = value;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, date_input, dob_iso)

        print(f" Date of Birth filled successfully ({dob_excel} -> {dob_iso})!")
        time.sleep(random.uniform(0.5, 1.0))
    except Exception as e:
        print(" Date input not found or failed:", e)

    try:
        submit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[role='button']")))
        submit_btn.click()
        print("Form submitted successfully!")

        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Your response has been recorded')]")))
        print("Confirmation page loaded!")

        screenshot_path = os.path.join(screenshot_folder, f"row_{idx}.png")
        driver.save_screenshot(screenshot_path)
        print(f" Screenshot saved: {screenshot_path}")
    except Exception as e:
        print("Failed to submit form or take screenshot:", e)

    time.sleep(random.uniform(2, 4))

print("\n All rows processed successfully!")
driver.quit()
