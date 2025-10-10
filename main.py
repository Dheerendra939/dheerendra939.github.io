import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Setup Chrome headless options
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    return driver

# Visit URL and click the first link/button
def visit_and_click(url):
    print(f"🌐 Opening: {url}")
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(5)  # wait for page to load

        clickable = None
        try:
            clickable = driver.find_element(By.TAG_NAME, "a")
        except:
            try:
                clickable = driver.find_element(By.TAG_NAME, "button")
            except:
                pass

        if clickable:
            driver.execute_script("arguments[0].click();", clickable)
            print(f"🖱 Clicked first element on: {url}")
        else:
            print(f"⚠ No clickable elements found on: {url}")

        time.sleep(3)
    except Exception as e:
        print(f"❌ Error with {url}: {e}")
    finally:
        driver.quit()

# Main
if __name__ == "__main__":
    with open("urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    # Repeat the process 5 times
    for round_num in range(1, 6):
        print(f"\n🔁 Run {round_num}/5 started...\n")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(visit_and_click, urls)
        print(f"✅ Run {round_num}/5 completed.\n")
        time.sleep(1)  # wait before next round
