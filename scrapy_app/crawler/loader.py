# -*- coding: utf-8 -*-

import logging
import re
import readability.readability
import lxml
from pprint import pprint
from gzip import compress
from base64 import b64encode
from w3lib.html import replace_escape_chars 
from w3lib.html import remove_tags, remove_comments
from crawler.items import NewsItem
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, TakeFirst
from itemloaders.processors import Join, Compose, MapCompose

logger = logging.getLogger(__name__)

def _remove_fluff(strl):
    for s in strl:
        if s.startswith('http'):
            continue
        s = re.sub(r'.*[Bb]y ', r'', s).strip()
        if s:
            yield s

def _strip_strl(strl):
    for s in strl:
        yield s.strip()

def _split_and(strl):
    for s in strl:
        for tok in s.split(' and '):
            yield tok

def to_str(s):
    if isinstance(s, bytes):
        s = s.decode('utf-8')
    return s

class NewsLoader(ItemLoader):
    """
    A convenience class provied by scrap to conver raw data into sanitized NewsItem.
    USed some google code to get results quickly.
    TODO: figure out how to extract author
    """
    default_item_class = NewsItem
    default_output_processor = TakeFirst()
        
    clean_fn = MapCompose(lambda x: x.strip(),
                          lambda x: replace_escape_chars(x, replace_by=' '),
                         )
    headline_in = clean_fn

    bodytext_in = Compose(Join(' '),lambda x: replace_escape_chars(x, replace_by=' '))
    bodytext_out = TakeFirst()
    
    rawpagegzipb64_out = Compose(TakeFirst(),
                                 compress,
                                 b64encode,
                                 lambda x: str(x, encoding='UTF-8'),
                                )

    bylines_in = Compose(_strip_strl,
                         _remove_fluff,
                         _split_and,
                         Join(','))
    bylines_out = Compose(TakeFirst(), lambda x: x.split(','))

    def add_fromresponse(self, response):
        """Extracts standard data from the response object itself"""
        # TODO: Should be we using the canonicalised value of this from og:url
        #       or whatever to avoid dupes? Not important when taking a feed,
        #       but may be necessary to avoid duplicative crawls.
        self.add_value('url', response.url)

    def add_htmlmeta(self):
        self.add_xpath('author',
                       'head/meta[@name="author" or '
                            '@property="author"]/@content')

    def add_scrapymeta(self, response):
        """Extracts the content passed through meta tags from the Request. This
           is normally metadata from the RSS feed which linked to the article,
           or from Google News sitemaps."""

        if 'RSSFeed' in response.meta:
            d = response.meta['RSSFeed']
            self.add_value('headline',     d.get('title'))

    def add_readability(self, response):
        # anything to extract ?    
        if self.get_output_value('headline') and self.get_output_value('bodytext'):
            return
        # get cleaned up data
        readified_doc = readability.readability.Document(response.text)

        if not self.get_output_value('headline'):
            logger.debug(f'Using readability fallback for headline: {self.get_output_value("url")}')
            self.add_value('headline',
                           readified_doc.short_title())

        if not self.get_output_value('bodytext'):
            logger.debug(f'Using readability fallback for bodytext: {self.get_output_value("url")}')
            reparsed = lxml.html.fromstring(readified_doc.summary())

            self.add_value('bodytext',
                           reparsed.xpath('//body//text()')
                          )