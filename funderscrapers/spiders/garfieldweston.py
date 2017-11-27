# -*- coding: utf-8 -*-
import scrapy


class GarfieldWestonSpider(scrapy.Spider):
    name = 'garfieldweston'
    start_urls = ['https://garfieldweston.org/what-we-support/']

    def parse(self, response):
        for f in response.css('.post-link'):
            fund = {
                "title": f.css('h2::text').extract_first().strip(),
                "description": "",
                "link": f.css('a.cta::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            if not fund["link"].startswith(self.start_urls[0]):
                continue
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('section.entry-content').extract_first()
        })
        yield fund
