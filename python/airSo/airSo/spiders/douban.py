import this
import scrapy
from scrapy import Request

from airSo.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com/top250']
    # 把 这里的 start_urls 写在 start_requests() 里能执行更多操作，这里的只是简单的设置 url
    # start_urls = ['http://movie.douban.com/top250/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36',
    }

    # 这些方法参数 self 应该是指上面定义的那些变量
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        # 调试
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        item = DoubanItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = \
                movie.xpath('.//div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['score_num'] = movie.xpath('.//div[@class="star"]/span[4]/text()').re(r'(\d+)人评价')[0]
            yield item

        # 翻页，获取翻页的 href 值,再次发起 request 请求
        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url
            yield Request(next_url, headers=self.headers, dont_filter=True)
# [scrapy.spidermiddlewares.offsite] DEBUG: Filtered offsite request to