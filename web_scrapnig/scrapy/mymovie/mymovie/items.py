# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Model - DB와 연관되는 데이터 (객체)

class MymovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 받아오는 데이터는 문자 타입이다.
    title = scrapy.Field()
    star = scrapy.Field()
    desc = scrapy.Field()
    writer = scrapy.Field()
    date = scrapy.Field()
