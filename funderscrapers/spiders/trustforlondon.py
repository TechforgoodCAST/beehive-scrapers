# -*- coding: utf-8 -*-
import scrapy


class TrustForLondonSpider(scrapy.Spider):
    name = 'trustforlondon'
    start_urls = ['https://www.trustforlondon.org.uk/funding/']

    def parse(self, response):
        for f in response.css('.grid-image-rounded a'):
            fund = {
                "title": f.css('h3::text').extract_first(),
                "description": f.css('p.grid-image-rounded__description__summary::text').extract_first(),
                "link": f.css('::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('section.section--body').extract_first()
        })
        yield fund
