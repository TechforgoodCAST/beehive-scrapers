# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime


class SaveDBPipeline(object):

    collection_name = 'scraped_funds'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        date_scraped = datetime.datetime.now()
        con = self.db[self.collection_name]
        new_item = dict(item)
        new_item["last_scraped"] = date_scraped
        new_item["first_scraped"] = date_scraped
        _id = new_item["link"]

        existing_item = con.find_one({"_id": _id})
        # check whether fund already exists
        if existing_item:
            latest_scrape = existing_item.get('scrapes', [])[-1]
            # if it does then check whether it is changed
            if (latest_scrape.get("contentHash", "") != new_item.get("contentHash", "") or
                latest_scrape.get("description", "") != new_item.get("description", "") or
                latest_scrape.get("title", "") != new_item.get("title", "")):
                # if it is then "changed fund notification"
                self.db["notifications"].insert_one({
                    "notice": "Fund changed",
                    "fund": _id,
                    "date_issued": datetime.datetime.now()
                })
                existing_item["scrapes"].append(new_item)

            else:
                # if not then just update the last_scraped date
                existing_item["scrapes"][-1]["last_scraped"] = date_scraped
                
            existing_item["funder"] = spider.name
            con.find_one_and_replace({"_id": _id}, existing_item)
        else:
            # if it doesn't then "new fund notification"
            self.db["notifications"].insert_one({
                "notice": "New fund",
                "fund": _id,
                "date_issued": datetime.datetime.now()
            })
            con.insert_one({
                "_id": _id,
                "funder": spider.name,
                "scrapes": [new_item]
            })

        return item
