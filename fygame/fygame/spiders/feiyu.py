import requests
from scrapy import Spider, Request
from lxml import etree

import re

from ..items import FygameItem
from ..settings import DEFAULT_REQUEST_HEADERS

class FeiyuSpider(Spider):
    name = 'feiyu'
    allowed_domains = ['www.key173.com']
    start_urls = 'http://www.key173.com/index.php?type=product&id=0&page={0}'
    game_id = 1001

    def start_requests(self):
        for i in range(1, 153):
            url = self.start_urls.format(i)
            yield Request(url, callback=self.parse_outer_page, meta={'url': url})

    def parse_outer_page(self, response):
        urls_game = response.xpath('//div[@class="placeholder"]/a[1]/@href').extract()
        g_photos = response.xpath('//div[@class="placeholder"]/a[1]/img/@data-src').extract()
        for url, photo in zip(urls_game, g_photos):
            url_game = 'http://'+self.allowed_domains[0]+'/'+url
            yield Request(url_game, callback=self.parse_inner_page, meta={'url': url_game, 'gphoto': photo})

    def parse_inner_page(self, response):

        item = FygameItem()
        item['gId'] = self.game_id
        item['gPreId'] = response.meta['url'].split('=')[-1]
        item['gName'] = response.xpath('//h1[@class="entry-title"]/text()').get().strip()
        item['gAddress'] = response.meta['url']
        item['gPhoto'] = 'http://'+self.allowed_domains[0]+'/'+response.meta['gphoto']
        item['gTime'] = response.xpath('//span[@class="meta-date"]//time/text()').get().strip()
        item['gClass'] = response.xpath('//div[@class="breadcrumbs"]/a[2]/text()').get().strip()
        item['gImages'] = response.xpath('//div[@class="entry-content u-text-format u-clearfix"]//img/@src').extract()
        if response.xpath('//video/source[2]/@src').get():
            item['gVideo'] = response.xpath('//video/source[2]/@src').get().strip()
        else:
            item['gVideo'] = response.xpath('//video/source[2]/@src').get()
        item['gContext'] = response.xpath('//div[@class="entry-content u-text-format u-clearfix"]//p//text()').extract()

        url_tmp = 'http://'+self.allowed_domains[0]+'/'+response.xpath('//div[@class="pay-box"]/a/@href').get().strip()
        item['gCardSecret'] = self.parse_link(url_tmp)
        item['gIsDelete'] = 0
        self.game_id += 1

        yield item

    def parse_link(self, url):
        post_tmp = requests.post(url, headers=DEFAULT_REQUEST_HEADERS).text
        pattern = re.compile("href='(.*?)&.*?</script>")
        genkey = pattern.findall(post_tmp)[0].strip()
        all_url = 'http://'+self.allowed_domains[0]+'/' + genkey + '&' + url.split('?')[-1]
        post_html_fahuo = requests.get(all_url, headers=DEFAULT_REQUEST_HEADERS).text
        parse_page = etree.HTML(post_html_fahuo)
        result = parse_page.xpath('//textarea[@class="form-control"]/text()')[0].strip()

        return result

