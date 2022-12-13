import scrapy
from ozpar.items import LinkItem
from scrapy.loader import ItemLoader
from scrapy_playwright.page import PageMethod


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    custom_settings = {
        'FEEDS': { 'catalog.json': { 'format': 'json', 'encoding': 'utf-8'}}
    }
    allowed_domains = ['www.ozon.ru', 'www.httpbin.org', 'www.ipinfo.io']
    # start_urls = ['http://www.ozon.ru/']
    # custom_settings = {
    #     'PLAYWRIGHT_LAUNCH_OPTIONS': {
    #         'proxy': {
    #             'server': 'socks5://109.237.96.124:62134'
    #         }
    #     }
    # }
    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.url_pattern = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?page={}&sorting=rating'
        self.phones_link_found = 0
        self.phones_link_need = 2
        self.current_page = 1
        self.current_smartphone = 1

    def start_requests(self):
        # GET request
        url = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating'
        # url = 'https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?page=1&sorting=rating'
        # url = 'https://httpbin.org/get'
        # url = 'https://ipinfo.io/json'
        # while self.phones_link_found < self.phones_link_need:
        # url = self.url_pattern.format(self.current_page)
        # url = 'file:///Users/kolodinevgenij/projects/ozon/ozpar/catalog.html'
        # print('Making request for {}'.format(url), 'and {} page'.format(self.current_page))
        yield scrapy.Request(
            url,
            meta = {
                "playwright": True,
                'playwright_include_page': True,
                'playwright_page_methods': [
                    PageMethod("wait_for_selector", "div.x7k.kx8"),
                    # PageMethod("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
                ],
                "playwright_context": "new",
                # "timeout": 60 * 1000,  # 60 seconds
                "playwright_context_kwargs": {
                    "java_script_enabled": True,
                    "ignore_https_errors": False,
                    "proxy": {
                        "server": "socks4://178.35.177.242:3629"
                    },
                },
                # "playwright_page_goto_kwargs": {
                #     # "wait_until": "networkidle",
                #     "wait_until": "load",
                # },
            },
            callback=self.parse_links,
        )
        self.current_page += 1
        # yield scrapy.Request(url)

    def parse_links(self, response):
        '''
        collect smartphone links
        '''
        blocks = response.css('div.x7k.kx8')
        for block in blocks:
            item_info = block.css('.k9x .he0.eh1.he4.tsBodyM span *::text')
            infolist = item_info.getall()
            # looking for type in info
            print(infolist)
            item_type = 'Unknown'
            try:
                index = infolist.index('Тип: ')
                item_type = infolist[index+1]
                if item_type == 'Смартфон':
                    loader = ItemLoader(LinkItem())
                    item_link = block.css('a.tile-hover-target.uk3').attrib['href']
                    loader.add_value('url', item_link)
                    loader.add_value('page', 1)
                    loader.add_value('num', self.current_smartphone)
                    self.current_smartphone += 1
                    loader.load_item()
            except ValueError:
                pass

        with open('catalog.html', 'w') as f:
            f.write(response.text)
        
