"""
This example shows two ways to redirect flows to another server.

启动方式：

    mitmdump -q -s  Spider61.py

"""
from bs4 import BeautifulSoup
from mitmproxy import http
import  requests
from requests import RequestException
import urllib

index=0

def get_one_page(url):
    try:
        response=requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code==200:
            return response.text
        return  None
    except RequestException:
        return None

def downloadswf(url,name):
    try:
        localadd='E:\爬取到的数据\六一儿童网\swf\\';
        urllib.request.urlretrieve(url, localadd+name+'.swf' )
        print("下载成功，保存到："+localadd+name+'.swf')
    except Exception:
        print("下载失败："+url)


def request(flow: http.HTTPFlow) -> None:
    url =flow.request.url
    if ( url.endswith('swf' )    and 'blank' not in url  and 'media'  in url):
            refer = flow.request.headers.get('Referer')
            global  index
            index=index+1
            html = BeautifulSoup( get_one_page(str(refer)) ,"lxml"  )
            tag=html.select('body > div.play_nav > div > h1 > a')
            name= str(tag).split('>')[1].split('<')[0]
            downloadswf(url,name)
            print( str(index)+', '+name+' swf地址：'+url+" ,引用："+str(refer) )





