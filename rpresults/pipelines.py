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

        # Create indexes
        self.db.results.create_index([
            ("raceid", pymongo.ASCENDING),
            ("horseid", pymongo.ASCENDING)
        ], unique=True)

        self.db.trainers.create_index([
            ("trainerid", pymongo.ASCENDING)
        ], unique=True)

        self.db.jockeys.create_index([
            ("jockeyid", pymongo.ASCENDING)
        ], unique=True)

        self.db.venues.create_index([
            ("venueid", pymongo.ASCENDING)
        ], unique=True)

        self.db.races.create_index([
            ("raceid", pymongo.ASCENDING)
        ], unique=True)

        self.db.horses.create_index([
            ("horseid", pymongo.ASCENDING)
        ], unique=True)

    def spider_closed(self, spider):
        self.mongo.close()

    def process_item(self, item, spider):
        d = dict(item)  # raceid + horseid

        # logger.info(d)

        trainer = d.pop('trainer')  # trainerid
        self.db.trainers.update_one(
            {'trainerid': trainer['trainerid']},
            {'$set': trainer},
            upsert=True
        )

        jockey = d.pop('jockey')  # jockeyid
        self.db.jockeys.update_one(
            {'jockeyid': jockey['jockeyid']},
            {'$set': jockey},
            upsert=True
        )

        race = d.pop('race')  # raceid
        # race_venue = race.pop('venue')  # venueid
        # print("venue in pipeline:", race_venue)
        # self.db.venues.update_one(
        #     {'venueid': race_venue['venueid']},
        #     {'$set': race_venue},
        #     upsert=True
        # )

        self.db.races.update_one(
            {'raceid': race['raceid']},
            {'$set': race},
            upsert=True
        )

        horse = d.pop('horse')  # horseid
        self.db.horses.update_one(
            {'horseid': horse['horseid']},
            {'$set': horse},
            upsert=True
        )

        self.db.results.update_one(
            {'raceid': d['raceid'], 'horseid': d['horseid']},
            {'$set': d},
            upsert=True
        )
        return item
