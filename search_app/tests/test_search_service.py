import unittest
import asyncio
from unittest.case import expectedFailure
from search_app.service import SearchService
from unittest.mock import AsyncMock, MagicMock

class TestSearchService(unittest.TestCase):

    async def find_items(self, service, search_term):
        return await service.find(search_term)

    def test_find_returns_results(self):
        # arrange    
        expected = [{'bodytext': 'text', 'headline': 'line', 'url': 'http://url'}]
        query_builder = MagicMock()
        query_builder.return_value = {'search':'item'}
        # arrange - mock mongo cursor
        cursor = MagicMock()
        cursor.to_list = AsyncMock()
        cursor.to_list.side_effect = lambda length: [{"bodytext":"text","headline":"line","url":"http://url","_id":"1234"}]
        mongo_items = MagicMock()
        mongo_items.news_items.find.return_value = cursor
        service = SearchService(mongo_items,query_builder)
        event_loop = asyncio.get_event_loop()
        # action
        result = event_loop.run_until_complete(self.find_items(service, 'good'))
        # assert
        self.assertEqual(result, expected)

