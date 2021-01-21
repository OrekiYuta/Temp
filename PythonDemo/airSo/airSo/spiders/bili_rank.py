import scrapy

from airSo.items import BiliTiem
# from fake_useragent import UserAgent


class BiliRankSpider(scrapy.Spider):
    name = 'bili_rank'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/v/popular/rank/all']

    def parse(self, response):
        item = BiliTiem()
        title = response.xpath('//a[@class="title"]/text()').extract()
        playNum = response.xpath('//div[@class="detail"]/span[@class="data-box"][1]/text()').extract()
        upName = response.xpath('//div[@class="detail"]/a/span[@class="data-box up-name"][1]/text()').extract()
        score = response.xpath('//div[@class="pts"]/div/text()').extract()

        for title, playNum, upName, score in zip(title, playNum, upName, score):
            item['title'] = title
            item['playNum'] = playNum
            item['upName'] = upName
            item['score'] = score

            yield item

        pass
