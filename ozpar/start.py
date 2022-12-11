from scrapy.utils.reactor import install_reactor, is_asyncio_reactor_installed
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from ozpar.spiders.catalog import CatalogSpider
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet import asyncioreactor


if __name__ == '__main__':
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    
    runner = CrawlerRunner(settings=get_project_settings())

    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    print('IS ASYNC REACTOR INSTALLED: ', is_asyncio_reactor_installed())
    from twisted.internet import reactor

    d = runner.crawl(CatalogSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() # the script will block here until the crawling is finished