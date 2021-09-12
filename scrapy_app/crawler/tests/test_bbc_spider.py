from time import sleep
import unittest
from unittest import mock
from scrapy import Spider, item
from scrapy.http.request import Request
from crawler.spiders.bbc import BBCSpider
from scrapy.http.response.xml import XmlResponse
from scrapy.selector import Selector
from crawler.tests.test_utils import response_from_file

class TestBBCSpider(unittest.TestCase):

    def test_parse_node_returns_item_request(self):
        body=b"""<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0" xmlns:media="http://search.yahoo.com/mrss/">
                <channel>
                <item>
                    <title><![CDATA[Social care: PM to unveil overhaul of sector in England]]></title>
                    <description><![CDATA[Boris Johnson will set out plans on Tuesday, amid a Tory backlash to tax rises to cover costs.]]></description>
                    <link>https://www.bbc.co.uk/news/uk-politics-58469872?at_medium=RSS&amp;at_campaign=KARANGA</link>
                    <guid isPermaLink="false">https://www.bbc.co.uk/news/uk-politics-58469872</guid>
                    <pubDate>Tue, 07 Sep 2021 01:34:52 GMT</pubDate>
                </item>
                </channel>
                </rss>"""

        spider = BBCSpider()
        feed_response = XmlResponse(url='http://feeds.bbci.co.uk/news/rss.xml?edition=uk', body=body)
        selector = Selector(feed_response)
        item_request = [x for x in spider._parse(feed_response)][0]
        self.assertEqual(item_request.url, 'https://www.bbc.co.uk/news/uk-politics-58469872?at_medium=RSS&at_campaign=KARANGA')
        self.assertEqual(item_request.callback.__name__, 'parse_page')
    
    def test_parse_page_simple(self):
        response = response_from_file('./bbc-spider-test-simple.html', Request('https://www.bbc.co.uk/news/uk-politics-58469872?at_medium=RSS&amp;at_campaign=KARANGA'))
        spider =  BBCSpider()
        item  =  spider.parse_page(response)
        self.assertEqual(item['url'],'https://www.bbc.co.uk/news/uk-politics-58469872?at_medium=RSS&amp;at_campaign=KARANGA')
        self.assertEqual(item['headline'],'Social care')
        self.assertEqual(item['bodytext'],'The prime minister will announce the plans to MPs, alongside money to help the tackle pressures on the NHS caused by the Covid pandemic.')
        self.assertIsNone(item.get('author'))        

    def test_parse_page_full_on(self):
        response = response_from_file('./bbc-spider-test.html', Request('https://www.bbc.co.uk/news/uk-politics-58469872?at_medium=RSS&amp;at_campaign=KARANGA'))
        spider =  BBCSpider()
        item  =  spider.parse_page(response)
        self.assertEqual(item['url'],'https://www.bbc.co.uk/news/uk-politics-58469872?at_medium=RSS&amp;at_campaign=KARANGA')
        self.assertEqual(item['headline'],'Social care: Boris Johnson to unveil overhaul of sector in England - BBC News-1')
        self.assertEqual(len(item['bodytext']),221)
        self.assertIsNone(item.get('author'))        
