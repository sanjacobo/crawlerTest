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
    handle_httpstatus_list = [404, 500, 504]
    allowed_domains = ["orbitz.com"]
    start_urls = (
        'https://www.orbitz.com/Chicago-Hotels.d178248.Travel-Guide-Hotels',
        'https://www.orbitz.com/lp/flights/178248/flights-from-chicago'
    )

    regex_page_type = {'Travel-Guide-Hotels': r'Travel-Guide-Hotels',
                       'Flight-Origin-City': r'lp/flights/\d+/\D+',
                       'Flights-OnD': r'lp/flights/\d+/\d+/'
                       }

    page_types = ['Travel-Guide-Hotels',
                  'Flight-Origin-City',
                  'Flights-OnD'
                  ]

    def parse(self, response):
        page_url = response.url
        base_url = get_base_url(response)
        page_status = response.status
        page_name = self.get_page_type(self, page_url)

        if page_status == 200:

            links_on_page = [urlparse.urljoin(base_url, uri) for uri in response.xpath('//a/@href').extract()]
            # h1 page title
            h1 = response.xpath('//h1/text()').extract_first()
            # page meta robot
            robot = response.css('meta[name*=robots]::attr(content)').extract()[0]

            if robot != 'index,follow':
                yield TestcrawlerItem(
                    Url=page_url,
                    Type=page_name,
                    Title=h1,
                    Status=page_status,
                    Robot=robot
                )

            # Feed landing page links to spider
            for link in links_on_page:
                if self.url_is_landing_page(self, link):
                    yield scrapy.Request(link, callback=self.parse)
        else:
            print "Parse error page"
            yield TestcrawlerItem(
                Url=page_url,
                Type=page_name,
                Status=page_status,
                UrlSource=response.request.headers['Referer']
            )

    @staticmethod
    def url_is_landing_page(self, url):
        output = False
        for __page__ in self.page_types:
            if re.compile(self.regex_page_type[__page__]).search(url) is not None:
                output = True
                break
        return output

    @staticmethod
    def get_page_type(self, url):
        output = None
        for __page__ in self.page_types:
            if re.compile(self.regex_page_type[__page__]).search(url) is not None:
                output = __page__
                break
        return output
