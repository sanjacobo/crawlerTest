# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestcrawlerItem(scrapy.Item):
    Url = scrapy.Field()
    Type = scrapy.Field()
    Status = scrapy.Field()
    Title = scrapy.Field()
    Robot = scrapy.Field()
    pass
