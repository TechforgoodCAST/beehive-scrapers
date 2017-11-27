# -*- coding: utf-8 -*-
import scrapy


class JosephRowntreeCharitableTrustSpider(scrapy.Spider):
    name = 'josephrowntreecharitabletrust'
    start_urls = ['https://www.jrct.org.uk/funding-priorities']

    def parse(self, response):
        for f in response.css('.flcbT.colCanPage .qA ul')[0].css('li'):
            fund = {
                "title": f.css('a::text').extract_first(),
                "description": "",
                "link": f.css('a::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('.qA').extract_first()
        })
        yield fund
