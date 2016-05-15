# -*- coding: utf-8 -*-
import scrapy
from testCrawler.items import TestcrawlerItem
import re
from scrapy.utils.response import get_base_url
import urlparse


class LpSpider(scrapy.Spider):
    name = "lp"
    custom_settings = {
        'DEPTH_LIMIT': 1,
    }
    allowed_domains = ["orbitz.com"]
    # handle_httpstatus_all = True
    start_urls = (
        'https://www.orbitz.com/Chicago-Hotels.d178248.Travel-Guide-Hotels',
    )

    def parse(self, response):
        # get data form page
        h1 = response.xpath('//h1/text()').extract_first()
        robot = response.css('meta[name*=robots]::attr(content)').extract()[0]
        yield TestcrawlerItem(Url=response.url, Title=h1, Status=response.status, Robot=robot)

        # get more urls to crawl
        base_url = get_base_url(response)
        urls_on_page = [urlparse.urljoin(base_url, uri) for uri in response.xpath('//a/@href').extract()]

        for url in urls_on_page:
            if LpSpider.url_is_landing_page(self, url):
                yield scrapy.Request(url, callback=self.parse)

    @staticmethod
    def url_is_landing_page(self, url):
        # ToDo: regex of landing pages list
        regex = [re.compile(r'lp/flights'), re.compile(r'Travel-Guide-Hotels')]
        output = False
        for reg in regex:
            if reg.search(url) is not None:
                output = True
                break
        return output
