from queue import Queue
from threading import Thread
import requests
from fake_useragent import UserAgent
from lxml import etree

# 请求类
from lxml import etree


class CrawlInfo(Thread):
    def __init__(self, url_queue, html_queue):
        Thread.__init__(self)
        self.url_queue = url_queue
        self.html_queue = html_queue

    def run(self):
        headers = {
            "User-Agent": UserAgent().random
        }
        # 当队列中有数据就一直执行操作
        while self.url_queue.empty() == False:
            response = requests.get(self.url_queue.get(), headers=headers)
            # print(response.text)
            # 将请求的内容放进 内容队列
            if response.status_code == 200:
                self.html_queue.put(response.text)


# 解析类
class ParseInfo(Thread):
    def __init__(self, html_queue):
        Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while self.html_queue.empty() == False:
            etree_html = etree.HTML(self.html_queue.get())
            contents = etree_html.xpath('//div[@class="content"]/span[1]')
            with open('threadSp.txt', 'a', encoding='utf-8') as f:
                for content in contents:
                    content_xpath = content.xpath('string(.)')
                    print(content_xpath)
                    f.write(content_xpath + '\n')


if __name__ == '__main__':
    # url 队列
    url_queue = Queue()
    # 内容 队列
    html_queue = Queue()
    base_url = 'https://www.qiushibaike.com/text/page/{}/'
    for i in range(1, 14):
        url_format = base_url.format(i)
        url_queue.put(url_format)

    crawl_list = []
    # 创建线程并启动
    for i in range(0, 3):
        crawl_info = CrawlInfo(url_queue, html_queue)
        crawl_list.append(crawl_info)  # 放入线程列表 等待
        crawl_info.start()

    # https://blog.csdn.net/jiede1/article/details/79939351
    for crawl in crawl_list:
        crawl.join()  # 让主线程等待，不然主线程直接执行结束，上面三个子线程都没执行完

    parse_list = []
    for i in range(0, 3):
        parse_info = ParseInfo(html_queue)
        parse_list.append(parse_info)
        parse_info.start()

    for parse in parse_list:
        parse.join()
