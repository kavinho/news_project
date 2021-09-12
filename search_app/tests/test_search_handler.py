import unittest
import tornado.web
from tornado.testing import AsyncHTTPTestCase
from search_app.search_handler import SearchHandler
from search_app.service import SearchService
from unittest.mock import AsyncMock, MagicMock

class TestSearchHandler(AsyncHTTPTestCase):

    def get_app(self):
        expected = [{'bodytext': 'text', 'headline': 'line', 'url': 'http://url'}]
        query_builder = MagicMock()
        query_builder.return_value = {'search':'item'}
        # arrange - mock mongo cursor
        cursor = MagicMock()
        cursor.to_list = AsyncMock()
        cursor.to_list.side_effect = lambda length: [{"bodytext":"t","headline":"l","url":"url","_id":"1234"}]
        mongo_items = MagicMock()
        mongo_items.news_items.find.return_value = cursor
        service = SearchService(mongo_items,query_builder)

        application = tornado.web.Application([
        (r'/find', SearchHandler, {'search_service': SearchService(mongo_items ,query_builder)})

        ])
        return application

    def test_handler_searches_query(self):
        response = self.fetch('/find?query=good')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'{"results": [{"bodytext": "t", "headline": "l", "url": "url"}]}')

    def test_hanlder_responds_no_query(self):
        response = self.fetch('/find')
        self.assertEqual(response.code, 400)