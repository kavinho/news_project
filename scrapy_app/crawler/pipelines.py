import logging
import pymongo
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)

class MongoPipeline:
    """
    This is a scrapy pipeline to push extracted data into Mongo.
    # TODO : Consider insert Async to Mongo
    #        Consider insert Async -> Queue(fail-retry)| message broker etc.. -> Mongo   

    """

    collection_name = 'news_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        except Exception as ex:
            logger.error("Could not insert item into Db", ex)    
        return item