from selenium.webdriver.edge.options import Options
from selenium import webdriver
import time
headless: bool = False

options = Options()

options.add_argument(r"user-data-dir=C:\Users\ACER\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"profile-directory=profile01")


if headless:
    options.add_argument("--headless")

driver = webdriver.Edge(options=options)

driver.get("https://www.amazon.com")
