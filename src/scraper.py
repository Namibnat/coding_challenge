"""Handle the opening website, downloading the HTML, and parsing it"""

import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

# Constants used for page load increments.
SLEEP_TIME_LONG = 3
SLEEP_TIME_SHORT = 1
SCROLLER_INCREMENTS = 200


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

    def _close_cookies_message(self):
        """Routine to close a cookies pop-up"""
        try:
            wait = WebDriverWait(self.driver, SLEEP_TIME_LONG)
            cookie_button = wait.until(expected_conditions.element_to_be_clickable(
                (By.CLASS_NAME, self.config['allow_cookies_button'])))
            cookie_button.click()
        except TimeoutException:
            print("Timed out waiting for the cookie button to be clickable.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _html_page_scroll(self):
        """Scroll to the bottom of the page in steps to allow page loading"""
        scroller = 0
        new_height = SCROLLER_INCREMENTS
        while scroller < new_height:
            self.driver.execute_script(f"window.scrollTo(0, {scroller});")
            time.sleep(SLEEP_TIME_SHORT)
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            scroller += SCROLLER_INCREMENTS

        time.sleep(SLEEP_TIME_LONG)
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_data(self):
        """Use Selenium to collect the entire html page"""
        self.driver.get(self.config['url'])

        # If there is a cookie button, press it.
        if 'allow_cookies_button' in self.config:
            self._close_cookies_message()

        # Scroll the page to collect it all.
        self._html_page_scroll()

        html = self.driver.page_source
        self.driver.quit()
        return html
