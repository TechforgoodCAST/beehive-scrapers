# -*- coding: utf-8 -*-
import scrapy


class ArtsCouncilEnglandSpider(scrapy.Spider):
    name = 'artscouncilengland'
    start_urls = [
        'http://www.artscouncil.org.uk/funding/funding-finder?search_api_views_fulltext=&field_status_of_fund%5B%5D=12']

    def parse(self, response):
        for f in response.css('article'):
            fund = {
                "title": f.css('h3 a::text').extract_first(),
                "description": f.css('.listingDetails').extract_first(),
                "link": f.css('h3 a::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(
                fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

        next_page = response.css(
            'li.pager-next a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('div.main').extract_first()
        })
        yield fund
