from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from time import sleep
from random import randint
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import platform
import os
import traceback
from utils.logger import setup_logger
from utils.mail_handler import send_mail
import sys
from utils.exceptions import VerifyApiException
from utils.call_handler import make_phone_call
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


"""
For Voting
"""

__author__ = "PYT4ONGIG"
__VERSION__ = 0.4


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


voting_logger = setup_logger("voting_logger", 'voting.log')
alert_logger = setup_logger("alert_logger", "alerts.log")

print(bcolors.OKGREEN + """
                                          _                 _            _       
 _____  _   _  _____  _   _  _____  _    _  ______  _   _____ 
|       ||  | |  ||       || | |   ||       ||  |  | ||       ||   | |       |
|    _  ||  |_|  ||_     _|| |_|   ||   _   ||   |_| ||    ___||   | |    ___|
|   |_| ||       |  |   |  |       ||  | |  ||       ||   | _ |   | |   | _ 
|    __||     |  |   |  |__    ||  |_|  ||  _    ||   ||  ||   | |   ||  |
|   |      |   |    |   |      |   ||       || | |   ||   |_| ||   | |   |_| |
|___|      |___|    |___|      |___||_______||_|  |__||_______||___| |_______|
       
""" + bcolors.ENDC)


# Turning off default loggers
selenium_logger = logging.getLogger(
    'selenium.webdriver.remote.remote_connection')
selenium_logger.setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

# logger = logging.basicConfig(filename="logger.log", level=logging.DEBUG,
#                     format='%(asctime)s  - %(levelname)s - %(message)s')

voting_logger.debug("Initilize: Voting Bot")


def get_driver(browser_name, driver_path=None, options=None):
    # Configure Drivers based on os
    # You can pass driver Path manually
    # Supports only chrome and firefox
    driver = None
    browser = browser_name.lower()
    assert browser in (
        "firefox", "chrome"), f"software doesn't support given browser: name: {browser_name}"
    if 'win' in platform.system().lower():
        if driver_path is not None:
            if browser == "firefox":
                driver = webdriver.Firefox(
                    executable_path=driver_path, options=options)
            elif browser == "chrome":
                driver = webdriver.Chrome(
                    executable_path=driver_path, options=options)
        elif not driver_path:
            driver = webdriver.Firefox(
                options=options) if browser == "firefox" else webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(
            executable_path=driver_path if driver_path else './chromedriver', options=options) if browser == "chrome" else webdriver.Firefox(
            executable_path=driver_path if driver_path else './geckodriver', options=options)
    print(f"{browser} is launching")
    return driver


def init_browser(browser_name):
    # if browser_name == "firefox":
    #     from selenium.webdriver.chrome.options import Options as chrome_options
    #     options = chrome_options()
    # elif browser_name == "chrome":
    #     from selenium.webdriver.firefox.options import Options as firefox_options
    #     options = firefox_options()
    # #options.headless = True
    driver = get_driver(browser_name)
    driver.maximize_window()
    voting_logger.debug(f"Browser {browser_name} initialization")
    return driver


cfg = {
    "subject": "Voting",
    "sender": "flaskapp90@gmail.com",
    "password": os.getenv("password"),
    "smtp_server": "smtp.gmail.com",
    "port": 465
}

read_from_cache = False
run = True


class VotingBot(object):
    ELEMENT_LOAD_TIMEOUT = 30  # Timeout for element Loading

    def __init__(self):
        self.s = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.set_page_load_timeout(self.ELEMENT_LOAD_TIMEOUT)
        self.voting_url = "https://voting.pancakeswap.finance"

        # Cache
        self.voting_cache = self.read_from_cache_file(read=read_from_cache)
        print(
            f"Reading From Cache = {read_from_cache}, Cache=:<{self.voting_cache}>")

    def refresh_tab(self, delay=.5):
        sleep(delay)
        voting_logger.debug(f"Tab with url: {self.voting_url} Refreshed")
        self.driver.refresh()

    def open_target_page(self):
        try:
            self.driver.get(self.voting_url)
        except Exception:
            voting_logger.critical(
                f"Can't Connect To {self.voting_url} Check The Network")
    # IO Procesess

    def write_to_cache_file(self, data, filename="cache.txt"):
        if data:
            with open(filename, 'w') as e:
                print(f"Writting {data} to cache file")
                e.write(str(data))

    def read_from_cache_file(self, read=True, filename="cache.txt"):
        if read:
            with open(filename, 'r') as e:
                voting_logger.debug(f"reading Data From cache")
                print("Reading data from cache file.")
                data = e.read()
                if data:
                    return data
                #     try:
                #         return eval(data)
                #     except:
                #         return "No proposals found"
                # else:
                #     return None
        return None
    # ------------

    def get_voting_names(self):
        no_prop_text = "//*[contains(text(), 'No proposals found')]"
        voting_selector = '//a[contains(@href, "/voting/proposal/")]//div[@color="text"]'

        try:
            no_prop = WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH,
                                                no_prop_text))
            )
            if no_prop:
                return "No proposals found"
        except:
            pass

        try:
            loading_finished = WebDriverWait(self.driver, self.ELEMENT_LOAD_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH,
                                                voting_selector))
            )

            if loading_finished:
                # print("Element Found")
                try:
                    element = self.driver.find_element(
                        By.XPATH, voting_selector)

                    voting_logger.debug(f"Current Voting LIST {element.text}")
                    return element.text if element else False
                except NoSuchElementException:
                    voting_logger.critical(
                        f"Cant Find Element With Selector {voting_selector}")
        except TimeoutException:
            voting_logger.critical(
                f"TimeOutError: Can't load Element. Locator= {voting_selector}")
        except Exception as e:
            voting_logger.critical(f"Error In Voting: {e}")
            traceback.print_exc()

    def create_alert_msg(self, cache, current):
        message = f'Voting Alert \n{cache} changed with {current}'
        return message

    def main(self):
        self.open_target_page()

        while True:
            self.refresh_tab()
            assert self.driver.current_url == "https://pancakeswap.finance/voting"
            print(print(f"Starting cache {self.voting_cache}"))
            print("Time for changes")
            # sleep(10)

            names = self.get_voting_names()
            print(f"Voting Names = {names}")
            if self.voting_cache is None:
                print("Voting Cache is Empty")

            if self.voting_cache is not None and self.voting_cache != names and names != "No proposals found" and names != None:
                msg = self.create_alert_msg(self.voting_cache, names)
                make_phone_call(alert_logger, from_="", to="")
                make_phone_call(alert_logger, from_="", to="")

                send_mail(alert_logger, msg, "receiver@gmail.com", **cfg)

                # 45 SECOND Dealy for other users
                sleep(45)
                make_phone_call(alert_logger, from_="", to="")
                send_mail(alert_logger, msg, "receiver@protonmail.com", **cfg)

            self.voting_cache = names
            print(f"Cache List {self.voting_cache}")
            voting_logger.debug(f"Cache List {self.voting_cache}")
            print(datetime.now())
            sleep(randint(5, 13))


if __name__ == "__main__":
    while run:
        try:
            bot = VotingBot()
            bot.main()
        except Exception:
            traceback.print_exc()
            voting_logger.critical(
                "Critical Alert in Main Loop", exc_info=sys.exc_info())
            read_from_cache = True
            print(f"Writing to cache")
            bot.write_to_cache_file(bot.voting_cache)
            bot.driver.quit()
            continue
