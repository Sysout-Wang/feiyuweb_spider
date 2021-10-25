# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FygameItem(scrapy.Item):

    gId = scrapy.Field()  # 游戏id
    gPreId = scrapy.Field()  # 游戏原id
    gName = scrapy.Field()  # 游戏名
    gAddress = scrapy.Field()  # 原地址
    gPhoto = scrapy.Field()  # 封面图片
    gTime = scrapy.Field()  # 发布时间
    gClass = scrapy.Field()  # 分类
    gImages = scrapy.Field()  # 介绍图片
    gVideo = scrapy.Field()  # 短cg
    gContext = scrapy.Field()  # 游戏介绍
    gBaidu = scrapy.Field()  # 百度云链接
    gCode = scrapy.Field()  # 游戏激活码
    gCheckCode = scrapy.Field()  # 百度云验证码
    gTyyLink = scrapy.Field()  # 天翼云链接
    gIsDelete = scrapy.Field() #是否删除
