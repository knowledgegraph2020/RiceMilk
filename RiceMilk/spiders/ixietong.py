# -*- coding: utf-8 -*-
import scrapy

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import datetime
import time
import os 
import RiceMilk.Ixietong.parse.config as cfg
from RiceMilk.Ixietong.parse.parse_detail import getToday, getYesterday, date_converter, getLastWeek
from RiceMilk.Ixietong.parse.parse_detail import scroll, page_parse

start_date = '2020-03-01'
end_date = '2020-03-31'

class IxietongSpider(scrapy.Spider):
    name = 'ixietong'
    allowed_domains = ['web']
    start_urls = ['https://www.baidu.com']

    
    def __init__(self, start_time = getLastWeek()[0], end_time = getLastWeek()[1],
                 url = 'https://m.citic.com/ixt-web/',
                 #url = 'https://m.citic.com/ixt-web/?token=9df151ba90db7498af4aca3b709b52ed&id=be1fe63ffbe7422ba5148063f009e7ab&categoryKey=ZX&flag=articleDetail#/',
                  *args,**kwargs):
        
        super(IxietongSpider, self).__init__(*args,**kwargs)
        
        
        # 选择新闻访问的日期
        self.start_time =  start_time # 默认值为昨天
        self.end_time = end_time # 默认值为昨天
        self.url = url # 因为需要扫码，所以一般需要手动输入



    def parse(self, response):
        
        print("**************************************************************")
        #print(response.body)
        print("**************************************************************")
        
        
        #start_urls = 'https://m.citic.com/ixt-web/?token=9df151ba90db7498af4aca3b709b52ed&id=be1fe63ffbe7422ba5148063f009e7ab&categoryKey=ZX&flag=articleDetail#/'
        #start_urls = 'https://m.citic.com/ixt-web/?token=40c76bd0d243b42cdf7b088894b183b8&id=be1fe63ffbe7422ba5148063f009e7ab&categoryKey=ZX&flag=articleDetail#/recommend'
           
    
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        
        #self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/Users/cengqiqi/chromedriver')
        #driver = webdriver.Chrome(executable_path='/Users/cengqiqi/chromedriver')
        #driver = webdriver.Chrome(executable_path='/data/chromedriver')
        driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/data/chromedriver')
           
        
        driver.get(self.url)
        
        
        time.sleep(7)
        driver.implicitly_wait(15) 
        # WebDriverWait(driver, timeout=10).until(
        #         expected_conditions.presence_of_element_located((By.ID,'tdcontent'))
        #         )
        
        
        # 下拉
        earlist_news_date = driver.find_elements_by_xpath('//p[@class = "source"]/span[2]')[-1].get_attribute('textContent')
        earlist_news_date = date_converter(earlist_news_date)  
        while earlist_news_date > start_date: 
            scroll(driver)
            earlist_news_date = driver.find_elements_by_xpath('//p[@class = "source"]/span[2]')[-1].get_attribute('textContent')
            earlist_news_date = date_converter(earlist_news_date)  
                        
        
        for index in range(1000):
            
            current_news_date = driver.find_elements_by_xpath('//p[@class = "source"]/span[2]')[index].get_attribute('textContent')
            current_news_date = date_converter(current_news_date)
            print(index)
            
            if current_news_date < start_date and index>5:
                break
            elif current_news_date>=start_date and current_news_date<=end_date:
                page_parse(driver, index)

