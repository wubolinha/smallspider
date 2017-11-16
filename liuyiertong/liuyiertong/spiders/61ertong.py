#
#
# 运行
#      scrapy crawl 61ertong
#
import logging
from time import sleep

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor



class  Spider61ertong(CrawlSpider):
    index = 0;
    name="61ertong"
    allowed_domains=['61ertong.com']
    start_urls=['http://www.61ertong.com/']
    file_object = open('E:\爬取到的数据\六一儿童网\\allswf.txt', 'w')  # 可追加可写，文件若不存在就创建
    file_object.write('所有包含swf文件的网页：\n')
    file_object.close()



    rules = (
        # 规则过滤
        Rule(LinkExtractor(allow=('http://www.61ertong.com/erge/',
                                  'http://www.61ertong.com/zhishi/',
                                  'http://www.61ertong.com/gushi/',
                                  'http://www.61ertong.com/xueyingyu/'),
                           ), callback='parse_item', follow=True),
    )



    def parse_item(self, response):
        next_page = str(response.url)
        # 使用进程池处理每个url
        if '_' in next_page:
            pass
        else:
            self.index = 1 + self.index
            file_object = open('E:\爬取到的数据\六一儿童网\\allswf.txt', 'a+')  # 可追加可写，文件若不存在就创建
            file_object.write(next_page+'\n')
            file_object.close()
            print('----------------------> ' + str(self.index) + ', ' + next_page)
            #self.getpage(next_page)






