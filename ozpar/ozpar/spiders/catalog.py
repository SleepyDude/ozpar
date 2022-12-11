import scrapy
from ozpar.items import SmartphoneItem
from scrapy.loader import ItemLoader


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    # allowed_domains = ['www.ozon.ru']
    # start_urls = ['http://www.ozon.ru/']
    # custom_settings = {
    #     'PLAYWRIGHT_LAUNCH_OPTIONS': {
    #         'proxy': {
    #             'server': 'socks5://109.237.96.124:62134'
    #         }
    #     }
    # }

    def start_requests(self):
        # GET request
        url = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/'
        # url = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?page=2&sorting=rating'
        # url = 'https://httpbin.org/get'
        # url = 'https://ipinfo.io/json'
        yield scrapy.Request(
            url,
            meta = {
                "playwright": True,
                "playwright_context": "new",
                "timeout": 60 * 1000,  # 60 seconds
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": {
                        "server": "socks5://109.237.96.124:62134"
                    },
                }
            },
        )
        # yield scrapy.Request(url)

    def parse(self, response):
        # 'response' contains the page as seen by the browser
        # loader = ItemLoader(SmartphoneItem())
        with open('catalog.html', 'w') as f:
            f.write(response.text)
        
