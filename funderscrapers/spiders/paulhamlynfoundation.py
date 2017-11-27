# -*- coding: utf-8 -*-
import scrapy


class PaulHamlynFoundationSpider(scrapy.Spider):
    name = 'paulhamlynfoundation'
    start_urls = ['http://www.phf.org.uk/our-work-in-the-uk/']

    def parse(self, response):
        for f in response.css('article'):
            request = scrapy.Request(
                f.css("a.read-more::attr(href)").extract_first(),
                callback=self.parse_fund_page
            )
            yield request

    def parse_fund_page(self, response):
        for f in response.css('.box-rollup'):
            fund = {
                "title": f.css('h3::text').extract_first(),
                "description": f.css('div.excerpt p::text').extract_first(),
                "link": f.css('a.read-more::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('section#fund-content div.single-content').extract_first()
        })
        yield fund
