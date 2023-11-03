"""Handle the opening website, downloading the HTML, and parsing it"""


import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


SLEEP_TIME = 3


class Scraper:
    """Scraper utility to fetch web pages"""
    def __init__(self, config):
        self.config = config
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/70.0.3538.77 Safari/537.36")

        self.driver = webdriver.Chrome(options=options)

    def get_data(self):
        """Use Selenium to collect the entire html page"""
        self.driver.get(self.config['url'])

        # If there is a cookie button, press it
        if 'allow_cookies_button' in self.config:
            try:
                wait = WebDriverWait(self.driver, SLEEP_TIME)
                cookie_button = wait.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, self.config['allow_cookies_button'])))
                cookie_button.click()
            except TimeoutException:
                print("Timed out waiting for the cookie button to be clickable.")
            except NoSuchElementException:
                print("Cookie button not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        try:
            wait = WebDriverWait(self.driver, SLEEP_TIME)
            wait.until(lambda driver: driver.execute_script("return document.body.scrollHeight") > 0)
        except TimeoutException:
            print("Timed out waiting for the initial scroll height to be available.")

        # Initial scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        # Scroll to the bottom of the page
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SLEEP_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break
            last_height = new_height

        html = self.driver.page_source
        self.driver.quit()
        return html
