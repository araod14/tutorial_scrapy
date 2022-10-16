import scrapy

"""
text = '//div[@class="quote"]/span[@itemprop="text"]/text()'
author = '//div[@class="quote"]/span/small[@class="author"]/text()'
tags = '//div[@class="tags"]/a[@class="tag"]/text()'
boton = '//ul[@class="pager"]/li[@class="next"]/a/@href'
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
                'text': quote.xpath('./span[@itemprop="text"]/text()').get(),
                'author': quote.xpath('./span/small[@class="author"]/text()').get(),
                'tags' : quote.xpath('/div[@class="tags"]/a[@class="tag"]/text()').getall()
            }

        next_page = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
