from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import shutil
import time

driver = None  # Initialize driver variable

# Create a truly temporary user-data-dir
temp_dir = tempfile.mkdtemp()

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

    # Point to Chromium binary on GitHub Actions
    options.binary_location = "/usr/bin/chromium-browser"

    # Use a unique user-data-dir
    options.add_argument(f"--user-data-dir={temp_dir}")

    # Create driver
    driver = webdriver.Chrome(options=options)

    driver.get("https://steamdb.info/app/730/")
    time.sleep(5)
    html = driver.page_source
    print(html[:1000])

except Exception as e:
    print("Error occurred:", e)

finally:
    # Quit driver only if it exists
    if driver:
        driver.quit()
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
