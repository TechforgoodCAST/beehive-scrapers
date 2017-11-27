import scrapy
import hashlib


class CityBridgeTrustSpider(scrapy.Spider):
    name = "citybridgetrust"
    start_urls = [
        'https://www.citybridgetrust.org.uk/what-we-do/grant-making/what-we-fund/',
    ]

    def parse(self, response):
        for f in response.css(".u-container.u-container--smaller.u-container--nopadd p")[1].css("a"):
            fund = {
                "title": f.css('::text').extract_first(),
                "description": "",
                "link": f.css('::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request
 
    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('.u-container.u-container--smaller.u-container--nopadd .c-Copy').extract_first()
        })
        yield fund
