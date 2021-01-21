from scrapy import cmdline
#  为要调试的文件名
name = 'douban'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
