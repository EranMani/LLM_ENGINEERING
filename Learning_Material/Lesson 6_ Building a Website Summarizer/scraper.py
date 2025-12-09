from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_selenium_content(url):
    # setup chrome options
    chrome_options = Options()

    # Add headless as an argument, which is faster and cleaner for background tasks
    chrome_options.add_argument("--headless")

    # Avoid protection and crashes
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)
        # Get the content found in the body tag
        body = driver.find_element(By.TAG_NAME, "body")
        body_text = body.text
        return body_text
    finally:
        # quit the driver to free up ram
        driver.quit()