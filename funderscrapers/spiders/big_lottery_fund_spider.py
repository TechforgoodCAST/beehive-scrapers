import scrapy
import hashlib


class BigLotteryFundSpider(scrapy.Spider):
    name = "biglotteryfund"
    start_urls = [
        'https://www.biglotteryfund.org.uk/funding/funding-finder',
    ]

    def parse(self, response):
        for f in response.css('article.programmeList'):
            fund = {
                "title": f.css('h3 a::text').extract_first(),
                "description": f.css('div.infoDetailsLeft p::text').extract_first(),
                "link": f.css('h3 a::attr(href)').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request

        next_page = response.css(
            'a.pagination-next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
 
    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        info = response.css('article#mainContentContainer').extract_first()
        fund.update({
            "contentHash": hashlib.md5(info.encode()).hexdigest()
        })
        yield fund
