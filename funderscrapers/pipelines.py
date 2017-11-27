# -*- coding: utf-8 -*-

# Item pipelines
import pymongo
import datetime
import hashlib
import json


class SaveDBPipeline(object):

    fund_collection = 'scraped_funds'
    notification_collection = 'notifications'

    def __init__(self, stats, mongo_uri, mongo_db):
        self.stats = stats
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            stats=crawler.stats,
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.stats.set_value('savedb/itemssaved', 0)
        self.stats.set_value('savedb/newitems', 0)
        self.stats.set_value('savedb/changeditems', 0)
        self.stats.set_value('savedb/unchangeditems', 0)

    def close_spider(self, spider):
        self.client.close()
        self.send_notification("Finished scraping {}".format(spider.name))

    def send_notification(self, message, fund="", content=""):
        self.db[self.notification_collection].insert_one({
            "notice": message,
            "fund": fund,
            "date_issued": datetime.datetime.now(),
            "content": content
        })

    def process_item(self, item, spider):
        date_scraped = datetime.datetime.now()
        con = self.db[self.fund_collection]
        new_item = dict(item)
        content = json.dumps(new_item, sort_keys=True)
        new_item["contentHash"] = hashlib.md5(content.encode()).hexdigest()
        new_item["last_scraped"] = date_scraped
        new_item["first_scraped"] = date_scraped
        _id = new_item["link"]
        notif_content = "Fund: {}\nFunder: {}".format(
            new_item["title"], spider.name)

        existing_item = con.find_one({"_id": _id})
        # check whether fund already exists
        if existing_item:
            latest_scrape = existing_item.get('scrapes', [])[-1]
            # if it does then check whether it is changed
            if latest_scrape.get("contentHash", "") != new_item.get("contentHash", ""):
                # if it is then "changed fund notification"
                self.send_notification("Fund changed", _id, content=notif_content)
                existing_item["scrapes"].append(new_item)
                self.stats.inc_value('savedb/changeditems')

            else:
                # if not then just update the last_scraped date
                existing_item["scrapes"][-1]["last_scraped"] = date_scraped
                self.stats.inc_value('savedb/unchangeditems')
                
            existing_item["funder"] = spider.name
            con.find_one_and_replace({"_id": _id}, existing_item)
            self.stats.inc_value('savedb/itemssaved')
        else:
            # if it doesn't then "new fund notification"
            self.send_notification("New fund", _id, content=notif_content)
            con.insert_one({
                "_id": _id,
                "funder": spider.name,
                "scrapes": [new_item]
            })
            self.stats.inc_value('savedb/itemssaved')
            self.stats.inc_value('savedb/newitems')

        return item
