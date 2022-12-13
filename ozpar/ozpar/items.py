# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class LinkItem(Item):
    url = Field()
    page = Field()
    num = Field()
