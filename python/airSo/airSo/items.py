# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirsoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class DoubanItem(scrapy.Item):
    # 排名
    ranking = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 评论人数
    score_num = scrapy.Field()
    pass


class BiliTiem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    playNum = scrapy.Field()
    upName = scrapy.Field()
    score = scrapy.Field()
