# -*- coding: utf-8 -*-
import scrapy
from testCrawler.items import TestcrawlerItem
from scrapy.utils.response import get_base_url
import urlparse
from testCrawler.spiders.DataProvider import Data


class LpSpider(scrapy.Spider):
    name = "lp"
    custom_settings = {
        'DEPTH_LIMIT': 1,
    }
    handle_httpstatus_list = [404, 500, 504]

    #run with: scrapy crawl lp -a pos=ORB

    def __init__(self, pos='ORB', *args, **kwargs):
        super(LpSpider, self).__init__(*args, **kwargs)
        # set pages data
        data = Data()
        self.page_types = data.page_types
        self.regex_page_type = data.regex_page_type
        self.find_page_type = data.find_page_type
        # set domains
        self.allowed_domains = [data.domains[pos]]
        # set start urls
        f = open("start_urls_" + pos + ".csv")
        self.start_urls = [url.strip() for url in f.readlines()]
        f.close()

    def parse(self, response):
        page_url = response.url
        base_url = get_base_url(response)
        page_status = response.status
        page_name = self.find_page_type(self, page_url)

        if page_status == 200:

            links_on_page = [urlparse.urljoin(base_url, uri) for uri in response.xpath('//a/@href').extract()]
            # h1 page title
            h1 = response.xpath('//h1/text()').extract_first()
            # page meta robot
            robot = response.css('meta[name*=robots]::attr(content)').extract()[0]

            if str(robot).lower().replace(" ", "") != 'index,follow':
                yield TestcrawlerItem(
                    Url=page_url,
                    Type=page_name,
                    Title=h1,
                    Status=page_status,
                    Robot=robot
                )

            # Feed landing page links to spider
            for link in links_on_page:
                if self.find_page_type(self, link) is not None:
                    yield scrapy.Request(link, callback=self.parse)
        else:
            url_source = response.request.headers['Referer']

            yield TestcrawlerItem(
                Url=page_url,
                Type=page_name,
                Status=page_status,
                UrlSource=url_source
            )
