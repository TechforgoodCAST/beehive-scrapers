# -*- coding: utf-8 -*-
import scrapy
from slugify import slugify


class EsmeefairburnSpider(scrapy.Spider):
    name = 'esmeefairburn'
    start_urls = [
        'https://esmeefairbairn.org.uk/arts',
        'https://esmeefairbairn.org.uk/children-and-young-people',
        'https://esmeefairbairn.org.uk/environment',
        'https://esmeefairbairn.org.uk/food',
        'https://esmeefairbairn.org.uk/social-change',
    ]

    def parse(self, response):
        for f in response.css('article'):
            fund = {
                "title": f.css('h3::text').extract_first(),
                "description": "",
                "info": f.css('.b-article__main').extract_first(),
                "link": "",
            }
            fund["link"] = response.urljoin("#{}".format(slugify(fund["title"])))
            yield fund
