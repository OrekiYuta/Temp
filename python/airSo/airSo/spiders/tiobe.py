import scrapy
import time


class TiobeSpider(scrapy.Spider):
    name = 'tiobe'
    allowed_domains = ['www.tiobe.com/tiobe-index']
    start_urls = ['http://www.tiobe.com/tiobe-index/']

    def parse(self, response):

        for item in response.css('#top20 > tbody > tr'):
            yield {
                'rank_this-year': item.css('td:nth-child(1)::text').get().strip(),
                'rank_last-year': item.css('td:nth-child(2)::text').get().strip(),
                'programming_language': item.css('td:nth-child(4)::text').get().strip(),
                'ratings': item.css('td:nth-child(5)::text').get().strip(),
                'change': item.css('td:nth-child(6)::text').get().strip(),
                'date': time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
            }

        for item in response.css('#otherPL > tbody > tr'):
            yield {
                'rank_this-year': item.css('td:nth-child(1)::text').get().strip(),
                'rank_last-year': '-',
                'programming_language': item.css('td:nth-child(2)::text').get().strip(),
                'Ratings': item.css('td:nth-child(3)::text').get().strip(),
                'change': '-',
                'date': time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
            }

        pass
