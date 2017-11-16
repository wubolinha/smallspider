#
#
#   根据 swf 链接 获取 swf 详细信息
#
#
import os

import requests
import re
import pymongo
import shutil
from bs4 import BeautifulSoup
from  selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

#PhantomJS  不加在图片，开启缓存
SERVICE_ARGS=['--load-images=false','--disk-cache=true']

browser=webdriver.PhantomJS(service_args= SERVICE_ARGS)# 使用  无界面浏览器 PhantomJS
wait=WebDriverWait(browser, 10)#网页加载需要一定的时间，10秒内没有加载完毕就算是超时

# 浏览器代理设置
#proxy=webdriver.Proxy()
#proxy.proxy_type=ProxyType.MANUAL
#proxy.http_proxy='127.0.0.1:8080'

# 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
#proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
#browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

#  无界面浏览器PhantomJS 默认窗口小，影响浏览淘宝
browser.set_window_size(1400,900)

index=0;

allswf_path=os.path.dirname(__file__)+'/allswf.txt'


def get_one_page(url):
    try:
        browser.get(url)
        html = browser.page_source  # 获取整个网页源代码
        return html
    except Exception:
        return html


# 生成分类路径
def  generate_path(Tag):
    paths= Tag.replace(' → ','_')
    return  paths

#
# 在  E:\爬取到的数据\六一儿童网\swf_index 目录下寻找 名字 相符合的swf文件
#  然后，分类，重命名
#

AllSwfPath='E:\爬取到的数据\六一儿童网\swf_index\\'
def sortAndrenameFile(product):
    num_name=product.get('url').split('/')[-1].split('.')[0]
    ori_swffile=AllSwfPath+num_name+'.swf'
    if os.path.exists( ori_swffile ):
        classify= product.get('classify').replace('_','\\')
        classifypath=AllSwfPath+classify+'\\'+product.get('title')+'.swf'
        if( os.path.exists( AllSwfPath+classify ) ):
            pass
        else:
            os.makedirs(AllSwfPath+classify)
        shutil.move(ori_swffile, classifypath)
        print( str(product.get('index'))  +'---->  '+ori_swffile+'  -----> '+classifypath +' 移动完成 ')



def geturlline():
    file_object = open(allswf_path,'r' , encoding='UTF-8')
    global  index
    for line in file_object:
        if(line.startswith('http')):
            print( line )
            html = pq(get_one_page(line))
           # html = BeautifulSoup(get_one_page(  line   ), "lxml")
            title = html ('.title > h1:nth-child(1) > a:nth-child(1)').text()
            if  len(title) >=1:
                index = index + 1
                product = {
                    'index': index,
                    'title':  title,
                    'classify': generate_path(html('.title > span:nth-child(2)').text()),
                    'url': line.split('\n')[0]

                }
                sortAndrenameFile(product)


def main():
    geturlline()


if __name__=='__main__':
    main()


