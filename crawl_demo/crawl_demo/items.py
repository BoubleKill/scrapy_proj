# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    module = scrapy.Field()
    column = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field()
    news_date = scrapy.Field()
    content = scrapy.Field()
    ori_content = scrapy.Field()
    _id = scrapy.Field()


class CrawlDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # module = scrapy.Field()
    pass


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    movie_title = scrapy.Field()
    movie_score = scrapy.Field()
    movie_stars = scrapy.Field()
    movie_time = scrapy.Field()
    movie_detail_url = scrapy.Field()
