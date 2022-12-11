from selenium import webdriver
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent.parent

import time

class Parser:

    def __init__(self):
        self.catalog_url = "https://www.ozon.ru/category/telefony-i-smart-chasy-15501/"

        self.driver = webdriver.Chrome()


    def parse_catalog(self):
        

        self.driver.get(self.catalog_url)
        time.sleep(2)
        with open(str(ROOT_DIR.joinpath('catalog.html')), 'w') as f:
            f.write(self.driver.page_source)
