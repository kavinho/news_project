import unittest
from unittest.case import expectedFailure
from search_app.query_builder import build_mongo_query

class TestQueryBuilder(unittest.TestCase):

    def test_builds_query(self):
        expected = {'headline': {'$regex': 'great news', '$options': 'i'}}
        actual = build_mongo_query('great news')
        self.assertEqual(expected, actual)