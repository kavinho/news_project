import scrapy

class NewsItem(scrapy.Item):
    """
    A news item representing  data processed from a feed.
    """
    url = scrapy.Field()
    headline = scrapy.Field()
    bodytext = scrapy.Field()
    author = scrapy.Field()