from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta, date
import datetime as dt
import time
import os
import csv

from selenium_initializer import save_json, init_driver
from selenium_utils import SeleniumUtils


def site_test_1():
    global driver
    try:
        element = su.get_button_by_label("Click me")
        print(element.accessible_name, element.is_displayed, element.id)
        element.click()
        
        test2 = su.get_button_by_label("Button")
        test2.click()
        
    except Exception as e:
        print(e)


# Main function
def main() -> None:
    global driver
    global su
    driver = init_driver(url="http://127.0.0.1:5500/seleniumplusplus/tests/page/index.html")
    su = SeleniumUtils(driver)
    # Do stuff here
    site_test_1()

    driver.quit()


if __name__ == "__main__":
    main()
