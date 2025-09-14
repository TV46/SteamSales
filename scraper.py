from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configure Chrome
options = Options()
options.headless = True  # Set False if you want to see the browser
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/117.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

try:
    url = "https://steamdb.info/app/730/"  # Replace with the page you want
    driver.get(url)

    # Wait a few seconds for the page to fully load
    time.sleep(5)

    html = driver.page_source
    print(html[:1000])  # Print first 1000 chars

finally:
    driver.quit()
