# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import item
import pymongo


class FygamePipeline(object):

    collection_name = 'game_feiyu'

    def __init__(self, mongo_uri, mongo_user, mongo_pwd, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_user = mongo_user
        self.mongo_pwd = mongo_pwd
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_pwd=crawler.settings.get('MONGO_PWD'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db.authenticate(self.mongo_user, self.mongo_pwd)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        print(item)
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


