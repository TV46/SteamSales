from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import shutil
import time

driver = None
temp_dir = tempfile.mkdtemp()
output_file = "steamdb_page.html"  # HTML output file

try:
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )

    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://steamdb.info/app/730/")
    time.sleep(5)

    html = driver.page_source

    # Save HTML to a file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

except Exception as e:
    print("Error occurred:", e)

finally:
    if driver:
        driver.quit()
    shutil.rmtree(temp_dir)
