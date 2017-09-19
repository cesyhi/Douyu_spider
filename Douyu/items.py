# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuItem(scrapy.Item):
    # 主播昵称
    name = scrapy.Field()
    # uid
    uid = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 路径
    image_path = scrapy.Field()
    # 个人签名
    root_name = scrapy.Field()

