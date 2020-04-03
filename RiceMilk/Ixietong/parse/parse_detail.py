import re
import json
import scrapy
import time
import datetime
from scrapy import Request
from RiceMilk.tools.http_tools import get_html
from RiceMilk.Ixietong.parse.process import make_save_dir
from RiceMilk.tools.file_tools import convert_to_file
from termcolor import colored



def getToday():
    return time.strftime("%Y-%m-%d")

def getYesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    yesterday = str(yesterday)
    return yesterday   

def getLastWeek(): 
    today=datetime.date.today()     
    
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    yesterday = str(yesterday)
    
    sevenday=datetime.timedelta(days=7) 
    week_start=today-sevenday  
    week_start = str(week_start)
    
    return yesterday, week_start   
 
def date_converter(chinese):
    """该方法可以把爱协同吧网站的中文日期转化为数字表示形式"""
    number = re.findall(r'\d+',chinese)
    if len(number) == 2:
        month = number[0]
        day = number[1]
        year = str(datetime.datetime.now().year)
        num_date = '-'.join([year,month,day])
    elif len(number) == 3:
        year = number[0]
        month = number[1]
        day = number[2]
        num_date = '-'.join([year,month,day])
    else:
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
        num_date = '-'.join([year,month,day])
    
    return num_date


def scroll(driver):
    """ 该方法使页面自动往下拉 """
    # 要在下拉框内下拉
    #list_ = driver.find_element_by_xpath('//*[@class = "hide-scroll-line"]') 
    
    # 逐渐滚动浏览器窗口，令ajax逐渐加载
    for i in range(0,1):
        #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #driver.execute_script('document.getElementsByClassName("hide-scroll-line")[0].scrollTo(0,document.body.scrollHeight)') 
        driver.execute_script('document.getElementsByClassName("hide-scroll-line")[0].scrollTop=10000') # 要在下拉框内下拉
        time.sleep(2)
        driver.implicitly_wait(15) 



def page_parse(driver, index):
    
    """ 解析页面并储存 """
    news_page = getElementWithIndex(driver, index)
    news_page.click()
    driver.implicitly_wait(10) 
    # 标题
    element_title = driver.find_element_by_xpath("//*[@class='ad-content']/h2")
    title = element_title.get_attribute('textContent')
    print(title)
    
    # 正文
    elements_news = driver.find_elements_by_xpath('//*[@id = "artContent"]//p')
    news = [x.get_attribute('textContent') for x in elements_news]
    text = []
    for x in news:
        element = re.sub('\s', ' ', x)# 删掉句子前后空格
        if element: text.append(element) # 删掉全是空格的句子
        
    text = " ".join(text)
    #print(text)
    
    # 链接
    url = driver.current_url
    
    # 日期
    elements_date = driver.find_elements_by_xpath("//*[@class='ad-content']/h2/following-sibling::div[1]/p")
    temp_date = elements_date[0].get_attribute('textContent')
    month, day = re.findall(r'\d+',temp_date)
    year = str(datetime.datetime.now().year)
    date = '-'.join([year,month,day])

    # 储存路径
    path = make_save_dir()
    
    
    convert_to_file(url, title, date, text, path)
    driver.back()
    time.sleep(2)

     
def getElementWithIndex(driver, index):
    elements = driver.find_elements_by_xpath('//*[@class = "oneimg item"]//h2')
    return elements[index]
            

        
  





    
