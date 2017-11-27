import scrapy


class ComicReliefSpider(scrapy.Spider):
    name = "comicrelief"
    start_urls = [
        'https://www.comicrelief.com/apply-for-grants/open-grants-initiatives',
    ]

    def parse(self, response):
        for f in response.css('section.paragraph .cr-body'):
            fund = {
                "title": f.xpath('h3//text()').extract_first(),
                "description": f.xpath('p//text()').extract_first(),
                "link": f.xpath('p/a/@href').extract_first(),
            }
            fund["link"] = response.urljoin(fund["link"])
            request = scrapy.Request(fund["link"], callback=self.parse_fund, meta={'fund': fund})
            yield request
 
    def parse_fund(self, response):
        fund = response.meta.get('fund', {})
        fund.update({
            "info": response.css('main').extract_first()
        })
        yield fund
