# -*- coding: utf-8 -*-
import scrapy


class HeritageLotteryFundSpider(scrapy.Spider):
    name = 'heritagelotteryfund'
    start_urls = ['https://www.hlf.org.uk/looking-funding/our-grant-programmes']

    def parse(self, response):
        for f in response.css('.node-programme'):
            fund = {
                "title": f.css('h2 a::text').extract_first(),
                "description": f.css('div.block__summary::text').extract_first(),
                "link": f.css('h2 a::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('.region-content').extract_first()
        })
        yield fund
