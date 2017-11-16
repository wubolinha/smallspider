"""
This example shows two ways to redirect flows to another server.

启动方式：

    mitmdump -q -s  Spider61vip.py

抓去61儿童网vip数据
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
        localadd='E:\爬取到的数据\六一儿童网\swf_index\六一儿童网\儿童动画\国学\古诗\\';
        urllib.request.urlretrieve(url, localadd+name+'.swf')
        print("下载成功，保存到："+localadd+name+'.swf')
    except Exception:
        print("下载失败："+url)


def request(flow: http.HTTPFlow) -> None:
    url =flow.request.url
    if (url.endswith('.swf')):
        print( url  )
        if (  'blank' not in url  and 'media'  in url):
                referurl= url
                print(referurl)
                global index
                index = index + 1
                name=str(referurl).split('/')[-1].split('.')[0]
                print(str(index) +    ' swf地址：' + url +'  '+name)
                downloadswf(url,name)






