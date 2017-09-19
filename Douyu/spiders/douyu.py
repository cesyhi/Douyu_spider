# -*- coding: utf-8 -*-
import json

import scrapy

from Douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn']
    # start_urls = ['http://capi.douyucdn.cn/']
    host = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=100&offset='
    offset = 0
    start_urls = [host]

    def parse(self, response):
        print(response.body)
        # 将源码转换成字典
        data_list = json.loads(response.body.decode())['data']
        # 遍历数据列表
        for data in data_list:
            item = DouyuItem()

            item['name'] = data['nickname']
            item['uid'] = data['owner_uid']
            item['image_path'] = data['vertical_src']
            item['city'] = data['anchor_city']
            item['root_name'] = data['room_name']
            print(item)
            yield item

        # 翻页
        if (len(data_list)) != 0:
            self.offset += 100
            next_url = self.host + str(self.offset)
            yield scrapy.Request(next_url, callback=self.parse)
