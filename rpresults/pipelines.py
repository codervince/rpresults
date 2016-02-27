# -*- coding: utf-8 -*-
from scrapy import signals
import pymongo
import logging

# logger = logging.getLogger('rpresults_application')


class MongodbExportPipeline(object):
    def __init__(self, db_name):
        self.db_name = db_name

        self.mongo = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(
            crawler.settings.get('MONGO_DBNAME'),
        )

        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.mongo = pymongo.MongoClient()
        self.db = self.mongo[self.db_name]

        # Create index
        self.db.results.create_index([
            ("raceid", pymongo.ASCENDING),
            ("horseid", pymongo.ASCENDING)
        ], unique=True)

    def spider_closed(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        d = dict(item)

        # logger.info(d)

        # Update result object
        self.db.results.update_one(
            {'raceid': d['raceid'], 'horseid': d['horseid']},
            {'$set': d},
            upsert=True
        )

        # Update 'race' field
        self.db.results.update_many(
            {'raceid': d['raceid']},
            {'$set': {'race': d['race']}}
        )

        # Update 'prevrace' field
        self.db.results.update_many(
            {'prevrace.raceid': d['raceid']},
            {'$set': {'prevrace': d['race']}}
        )

        # Update 'nextrace' field
        self.db.results.update_many(
            {'nextrace.raceid': d['raceid']},
            {'$set': {'nextrace': d['race']}}
        )

        return item
