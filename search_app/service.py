import logging
from pymongo.errors import ServerSelectionTimeoutError
logger = logging.getLogger(__name__)

class SearchService:

    def __init__(self,mongo_items, query_builder) -> None:
    
        self.items_db = mongo_items # mongo collection
        self.query_builder = query_builder
    
    async def find(self, search_term):         
        try:
            cursor = self.items_db.news_items.find(self.query_builder(search_term))
            raw_reults = await cursor.to_list(length=100)
            return list(
                map(
                    lambda item: {"bodytext":item["bodytext"],"headline":item["headline"],"url":item["url"]},
                    raw_reults
                )
                )
        except ServerSelectionTimeoutError as sste:
            logger.exception("Failed to connect to data source.", sste) 
            return []       
        except Exception as e:
            logger.exception("failed to search.",e)
            return []
