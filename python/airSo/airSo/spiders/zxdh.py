import scrapy


class BiliSpider(scrapy.Spider):
    name = 'zxdh'
    allowed_domains = ['www.agefans.net']
    start_urls = ['https://www.agefans.net/']

    def parse(self, response):

        for item in response.xpath('//ul[@id="anime_update"]//li'):
            yield {
                'time': item.xpath('./span/text()').extract()[0],
                'name': item.xpath('./a/text()').extract_first()
            }
        pass

