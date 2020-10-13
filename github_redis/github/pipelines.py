# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from scrapy.exceptions import DropItem


class GithubTestPipeline(object):

    def process_item(self, item, spider):
        if item['email']:
            print(item)
        return item


class GithubPipeline(object):

    def __init__(self, mongo_url, mongo_db,collection):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DB'),
            collection = crawler.settings.get('COLLECTION'),
        )

    def process_item(self, item, spider):
        # 数据去重
        try:
            is_exist = self.db[self.collection].find({"url": item['url']})
        except:
            logging.error("数据库连接超时或异常，重试...！")
            is_exist = self.db[self.collection].find({"url": item['url']})
        if is_exist.count() >= 1:
            logging.info(f"{item['url']}:已存在，删除")
            raise DropItem

        if item['email'] == 'Sign in to view email':
            logging.error('登录时间过长，需重新登录')
            spider.crawler.engine.close_spider(spider)
            raise DropItem

        # elif not item['email']:
        #     logging.warning(f"{item['url']}:邮箱未公开，删除")
        #     raise DropItem
        else:
            self.db[self.collection].insert(dict(item))
            logging.warning(f"数据插入成功:{item['url']}")
            return item

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_url)
            self.db = self.client[self.mongo_db]
        except Exception as e:
            logging.error("数据库连接超时或异常，重试...！")
            self.client = pymongo.MongoClient(self.mongo_url)
            self.db = self.client[self.mongo_db]
            # raise ConnectionError("数据库连接超时或异常，请检查！")

    def close_spider(self, spider):
        logging.warning("爬虫完成，关闭...")
        total_nums = self.db[self.collection].find().count()
        email_nums = self.db[self.collection].find({"email": {"$ne": ''}}).count()
        logging.warning(f"共计爬取:{total_nums}个账户信息，其中含有邮箱的为:{email_nums}个")
        self.client.close()




