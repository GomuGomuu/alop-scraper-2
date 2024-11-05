from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")

chromedriver_path = r"../drivers/chromedriver.exe"

service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)


def download_editions(url: str, html_path: str) -> None:
    driver.get(url)
    time.sleep(5)
    page_html = driver.page_source

    os.makedirs(os.path.dirname(html_path), exist_ok=True)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(page_html)

    print(f"HTML saved at {html_path}")
