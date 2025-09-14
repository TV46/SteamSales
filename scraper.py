from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import shutil

driver = None
output_file = os.path.join(os.getcwd(), "steamdb_page.html")
temp_dir = f"/tmp/chrome-profile-{int(time.time())}"

try:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.binary_location = "/usr/bin/chromium"  # change if needed

    driver = webdriver.Chrome(options=options)
    driver.get("https://steamdb.info/app/730/")
    time.sleep(5)

    print("Page title:", driver.title)  # debug

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    print(f"Saved HTML to {output_file}")

finally:
    if driver:
        driver.quit()
    shutil.rmtree(temp_dir, ignore_errors=True)
