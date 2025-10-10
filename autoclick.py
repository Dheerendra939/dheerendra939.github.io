from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Configuration ---
page_url = "https://dheerendra939.github.io"  # Replace with your HTML page URL
click_interval = 5  # seconds (replace with desired frequency)

# --- Chrome options for headless GitHub run ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

# --- Launch browser ---
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(page_url)

# Wait for page and iframe to load
time.sleep(3)

try:
    while True:
        try:
            # Find all iframes on the page
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                iframe.click()  # Click the iframe area
                print(f"Iframe clicked at {time.strftime('%H:%M:%S')}")

        except Exception as e:
            print("Click failed:", e)

        time.sleep(click_interval)

except KeyboardInterrupt:
    print("Stopping auto-click.")
    driver.quit()
