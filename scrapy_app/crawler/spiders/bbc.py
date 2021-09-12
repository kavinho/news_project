# -*- coding: utf-8 -*-
import logging
from scrapy.spiders import XMLFeedSpider
from scrapy.http import Request

from crawler.loader import NewsLoader
from cssselect import HTMLTranslator
from itemloaders.processors import Identity, TakeFirst
from itemloaders.processors import Join, Compose, MapCompose

import re
logger = logging.getLogger(__name__)

class BBCSpider(XMLFeedSpider):
    """
    This crawls into BBC rss feed and pushed news items into MongoDb.
    Only one level of news items is processed.
    """

    name = 'bbc'
    start_urls = ['http://feeds.bbci.co.uk/news/rss.xml?edition=uk']

    def parse_node(self, response, selector):

        # xml feed response.    
        url = selector.xpath('link/text()').extract_first()
        if url:
            meta = {'originalurl': url} 
            # init loading actual news item
            yield self.url_to_request(url, meta=meta)
        else:
            self.logger.debug('No URL for %s' % str(selector.extract()))

    def url_to_request(self, url, callback=None, meta={}):
        
        if callback is None:
            callback = self.parse_page
        return Request(url.strip(), callback=callback, meta=meta)

    def parse_page(self, response):
        n_loader = NewsLoader(selector=response.selector)
        n_loader.add_xpath('headline', 'head/title/text()', lambda x: [re.sub(r' - BBC (News(beat)?|Sport)$', '', x[0])])
        n_loader.add_fromresponse(response)
        n_loader.add_htmlmeta()
        n_loader.add_scrapymeta(response)
        n_loader.add_readability(response)
        return n_loader.load_item()