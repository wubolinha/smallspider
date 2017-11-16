# 抓取猫眼电影Top100 榜单

import  requests
from requests import RequestException


def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return  None
    except RequestException:
        return None

def main():
    url='http://www.61ertong.com/';
    html=get_one_page(url)
    print(html)

if __name__=='__main__':
    main()


