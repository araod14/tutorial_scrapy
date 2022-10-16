import scrapy

"""
text = /html/body/div/div[2]/div[1]/div[1]/span[1]/text()
author = /html/body/div/div[2]/div[1]/div[1]/span[2]/small/text()
tags = 
"""


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['https://quotes.toscrape.com/']
    custom_settings = {
        'FEED_URI' : 'quotes.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    }

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('/html/body/div/div[2]/div[1]/div[1]/span[1]/text()').get(),
                'author': quote.xpath('/html/body/div/div[2]/div[1]/div[1]/span[2]/small/text()').get()
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
