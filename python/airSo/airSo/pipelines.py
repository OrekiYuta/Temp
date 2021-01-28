# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo


class AirsoPipeline(object):

    def open_spider(self, spider):
        self.client = pymongo().MongoClient("mongodb://0.0.0.0:27017/")

    def process_item(self, item, spider):
        self.client.bili.rank.insert_one(item)
        return item

    def close_spider(self, spider):
        self.client.close()
