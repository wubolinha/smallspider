# 使用 selenium,chromedriver 抓去淘宝页面
#  参考 selenium with python 官方文档 http://selenium-python.readthedocs.io/waits.html
#  使用  PyQuery解析整个网页源代码
import re
import pymongo
from  selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq


#mongo 数据库配置
MONGO_URL='localhost'
MONGO_DB='taobao'
MONGO_TABLE='product'

#PhantomJS  不加在图片，开启缓存
SERVICE_ARGS=['--load-images=false','--disk-cache=true']

keyword="手机"
#browser=webdriver.Chrome()  # 使用 chrome浏览器
browser=webdriver.PhantomJS(service_args= SERVICE_ARGS)# 使用  无界面浏览器 PhantomJS
wait=WebDriverWait(browser, 10)#网页加载需要一定的时间，10秒内没有加载完毕就算是超时

#  无界面浏览器PhantomJS 默认窗口小，影响浏览淘宝
browser.set_window_size(1400,900)

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def search():
    print("正在搜索")
    try:
        browser.get('http://www.taobao.com')
        input = wait .until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))  #使用 CSS选择器
        )
        submit=wait.until(
            EC.element_to_be_clickable( (By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button' ) )
        )
        input.send_keys(keyword);  #模拟输入
        submit.click();  #  模拟点击
        total= wait .until(   #获取总页数
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))  #使用 CSS选择器
        )
        get_product(1)
        return  total.text; # 返回总页数
    except TimeoutException:
        return search();     #超时 重新加一次


def next_page(page_number):
    try:
        input = wait.until(   #页码输入框
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input' ))  # 使用 CSS选择器
        )
        submit = wait.until(  # 确定 按钮
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input.clear();#清除输入框
        input.send_keys(page_number);
        submit.click();    #  翻页
        #是否翻页成功：判断当前高亮的页码数是否和输入的页码数一样
        wait.until( EC.text_to_be_present_in_element(( By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span' )
                                                      ,str(page_number)) )
        get_product(page_number)
    except TimeoutException:
        next_page(page_number);

def main():
        total=search();
        # 使用re模块获取数字
        total=int(re.compile('(\d+)').search(total).group(1));
        print( "总页数:",total )
        for i in range(2,total+1):
            print("当前页：",i)
            next_page(i)


def get_product(id):
    # 商品列表是否加载成功
    wait.until( EC.presence_of_all_elements_located( ( By.CSS_SELECTOR,'#mainsrp-itemlist .items .item'  )  ),10 )
    html=browser.page_source   # 获取整个网页源代码
    doc=pq(html)  #  使用  pyquery 解析网页代码
    items=doc('#mainsrp-itemlist .items .item').items()
    index=0
    for item in items:
        index=index+1;
        product={
            'position':   '第 '+str(id)+' 页 '+str(index)+' 项',
            'title': item.find('.title').text(),
            'price': item.find('.price').text(),
            'image':item.find('.pic .img').attr('data-src'), # 获取图片的 data-src 属性
            'deal': item.find('.deal-cnt').text()[:-3], # 多少人付款
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        #print( product )
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print("存储到mongodb成功：",result)
    except Exception:
        print("存储到mongodb失败",result)

if __name__ == '__main__':
    main()




