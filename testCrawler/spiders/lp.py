# -*- coding: utf-8 -*-
import scrapy
from testCrawler.items import TestcrawlerItem
import re


class LpSpider(scrapy.Spider):
    name = "lp"
    custom_settings = {
        'DEPTH_LIMIT': 1,
    }
    allowed_domains = ["orbitz.com"]
    handle_httpstatus_all = True
    start_urls = (
        'https://www.orbitz.com/Chicago-Hotels.d178248.Travel-Guide-Hotels',
    )

    def parse(self, response):
        yield TestcrawlerItem(lpUrl=response.url)
        yield TestcrawlerItem(lpStatus=response.status)

        for h1 in response.xpath('//h1').extract():
            yield TestcrawlerItem(lpTitle=h1)

        for url in response.xpath('//a/@href').extract():
            regexp = re.compile(r'lp/flights')
            if regexp.search(url) is not None:
                yield scrapy.Request('https://www.orbitz.com' + url, callback=self.parse)
