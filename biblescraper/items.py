# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiblescraperItem(scrapy.Item):
    language = scrapy.Field()
    version = scrapy.Field()
    testament = scrapy.Field()
    book_order = scrapy.Field()
    book = scrapy.Field()
    type = scrapy.Field()
    chapter = scrapy.Field()
    verse = scrapy.Field()
    position = scrapy.Field()
    scripture = scrapy.Field()
    words = scrapy.Field()

