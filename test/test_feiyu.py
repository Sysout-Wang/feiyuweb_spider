import requests
from lxml import etree

import random
import re

from ua_info import ua_list

class FySpider(object):
    def __init__(self):
        self.url_site = "http://www.key173.com/"
        self.url_pro = "http://www.key173.com/?type=productinfo&id=1978"
        self.headers = {
            'user-agent': random.choice(ua_list),
            'cookie': 'PHPSESSID=j3q9fq78uag25fku83akfbpkl3'
        }

    def parse_page(self):
        post_html = requests.get(self.url_pro, headers=self.headers).text
        parse_page = etree.HTML(post_html)
        item = dict()
        item['gPreId'] = self.url_pro.split('=')[-1]
        item['gName'] = parse_page.xpath('//h1[@class="entry-title"]/text()')[0].strip()
        item['gAddress'] = self.url_pro
        # item['gPhoto'] =
        item['gTime'] = parse_page.xpath('//span[@class="meta-date"]//time/text()')[0].strip()
        item['gClass'] = parse_page.xpath('//div[@class="breadcrumbs"]/a[2]/text()')[0].strip()
        # item['gImages'] =
        item['gVideo'] = parse_page.xpath('//video/source[2]/@src')[0].strip()
        # item['gContext'] =

        url_tmp = self.url_site+parse_page.xpath('//div[@class="pay-box"]/a/@href')[0].strip()
        item['gCode'], item['gTyyLink'], item['gBaidu'], item['gCheckCode'] = self.parse_link(url_tmp)
        item['gIsDelete'] = 0

        print(item)

    def parse_link(self, url):
        post_tmp = requests.post(url, headers=self.headers).text
        pattern = re.compile("href='(.*?)&.*?</script>")
        genkey = pattern.findall(post_tmp)[0].strip()
        all_url = self.url_site+genkey+'&'+url.split('?')[-1]
        post_html_fahuo = requests.get(all_url, headers=self.headers).text
        pattern_link = re.compile("解压码(.*?)天翼：(.*?)百度：(.*?)提取码：(.*?)</textarea", re.S)
        result = [i.strip() for i in pattern_link.findall(post_html_fahuo)[0]]

        return result

    def run(self):
        self.parse_page()

if __name__ == '__main__':
    test = FySpider()
    test.run()