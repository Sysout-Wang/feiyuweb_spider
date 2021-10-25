import scrapy


class FeiyuSpider(scrapy.Spider):
    name = 'feiyu'
    allowed_domains = ['www.key173.com']
    start_urls = ['http://www.key173.com/']

    def parse(self, response):
        pass
