# -*- coding: utf-8 -*-
import scrapy


class HenrySmithCharitySpider(scrapy.Spider):
    name = 'henrysmithcharity'
    start_urls = ['https://www.henrysmithcharity.org.uk/explore-our-grants-and-apply/']

    def parse(self, response):
        for link in response.css('a'):
            if link.css('span::text').extract_first() != "Learn more":
                continue

            fund = {
                "link": link.css('::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "title": response.css("h1::text").extract_first(),
            "description": "",
            "info": response.css('.et_pb_column.et_pb_column_2_3.et_pb_column_1').extract_first()
        })
        yield fund
