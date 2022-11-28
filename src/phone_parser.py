from selenium import webdriver

import time

class Parser:

    def __init__(self):
        self.driver = webdriver.Chrome()

        self.driver.get('https://google.com')
        time.sleep(5)