# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from scrapy.conf import settings
import scrapy
import os
from pymongo import MongoClient


class DouyuPipeline(object):
    def process_item(self, item, spider):
        return item


class Images(ImagesPipeline):
    # 从ｓｅｔｔｉｎｇ获取图片的路径
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        """
        发起下载的请求
        :return:
        """
        print(item['image_path'])
        yield scrapy.Request(item['image_path'])

    def item_completed(self, results, item, info):
        """
        获取下载的信息
        :param results:
        :param item:
        :param info:
        :return:
        """
        images = [data['path'] for ok, data in results]
        # 构建图片名
        old_name = self.IMAGES_STORE + images[0]
        # 构建图片新名
        new_name = self.IMAGES_STORE + images[0].split(os.sep)[0] + os.sep + item['name'] + '.jpg'

        # 改名
        os.rename(old_name, new_name)

        return item


class MongoPipeline(object):

    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        databases = settings['MONGO_DB']
        colname = settings['MONGO_CLINE']

        self.heander = MongoClient(host, port)
        self.db = self.heander[databases]
        self.col = self.db[colname]

    def process_item(self, item, spider):
        date = dict(item)
        self.col.insert(date)
        return item

    def close_spider(self):
        self.heander.close()