# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from RiceMilk.config.init import user_agent_list
from RiceMilk.CfiFinance.parse.parse_detail import get_news_link_static, get_news_link_JS, parse_Page, get_time
from RiceMilk.CfiFinance.parse.SeleniumRequest import SeleniumRequest
from RiceMilk.CfiFinance.parse.process import make_save_dir, get_full_path, getToday, getYesterday
from RiceMilk.tools.file_tools import add_to_exist_file
from scrapy import Request
from termcolor import colored

import scrapy
import os
import re
import time
import random


class CfifinanceSpider(scrapy.Spider):
    name = 'CfiFinance'
    allowed_domains = ['web']
    start_urls = ['http://cfi.cn']
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36"
        }
    
    #选择要访问的新闻类型
    get_static = True # 决定是否要静态页面，一般是要的
    get_JS = False # 决定一下是否要等待动态页面，会比较慢
    
    # 选择要访问的新闻类别
    industry = True
    stock = True
    futures = True
    forex = True
    
    # 选择新闻访问的日期
    start_time = getYesterday()
    end_time = getToday()

    def parse(self, response):
        
        """ 从中财网首页进入到各个不同大类到新闻 """
        
        links_names = []
     
        # 产经
        if self.industry:
            industry_link = response.xpath('//*[@id="mm2"]/a/@href').extract_first()
            industry_name = response.xpath('//*[@id="mm2"]/a/text()').extract_first()
            links_names.append([industry_link, industry_name])
            
        # 股票
        if self.stock:
            stock_link = response.xpath('//*[@id="mm4"]/a/@href').extract_first()
            stock_name = response.xpath('//*[@id="mm4"]/a/text()').extract_first()
            links_names.append([stock_link, stock_name])
            
        # 期货
        if self.futures:
            futures_link = response.xpath('//*[@id="mm12"]/a/@href').extract_first()
            futures_name = response.xpath('//*[@id="mm12"]/a/text()').extract_first()
            links_names.append([futures_link, futures_name])
            
        # 外汇
        if self.forex:
            forex_link = response.xpath('//*[@id="mm14"]/a/@href').extract_first()
            forex_name = response.xpath('//*[@id="mm14"]/a/text()').extract_first()
            links_names.append([forex_link, forex_name])
            
        for url_name in links_names:
            yield scrapy.Request(url=url_name[0],
                                 callback=self.parse_Category,
                                 meta={'name':url_name[1]},
                                 dont_filter=True)
        
        
        
    def parse_Category(self, response):
        
        """ 从大类新闻的页面进入每个大类里的子类别页面 """
        # 获取所有子类别链接
        cates_list =response.xpath("//*[@class = 'breadcrumb']//li//@href").extract()
        cates_name_list = response.xpath("//*[@class = 'breadcrumb']//li//text()").extract()
              
        
        # 去除一些重复或者纯数据类的页面
        if response.meta['name'] == "产经":
            cates_list = []#cates_list[1:] # 去除产经、期货和外汇的子类别 “首页” 标签
            cates_name_list = []#cates_name_list[1:]
        if response.meta['name'] == "股票":
            cates_list = cates_list[3:-1] # 去除股票大类的前三个和最后一个子类别
            cates_name_list = cates_name_list[3:-1]
        if response.meta['name'] == "期货":
            cates_list = cates_list[1:] # 去除产经、期货和外汇的子类别 “首页” 标签
            cates_name_list = cates_name_list[1:]
        if response.meta['name'] == "外汇":
            cates_list = cates_list[1:] # 去除产经、期货和外汇的子类别 “首页” 标签
            cates_name_list =  cates_name_list[1:]
        

        # if response.meta['name'] == "股票":
        #     cates_list = [cates_list[4] ]# 去除股票大类的前三个和最后一个子类别
        #     cates_name_list = [cates_name_list[4]]
            
        # 进入具体的子类别页面
        for i in range(len(cates_list)):
            url_news = "http://industry.cfi.cn/" +  cates_list[i]
            #
            cate_name = "/".join([response.meta['name'],cates_name_list[i]])
            cate_name = "-".join([response.meta['name'],cates_name_list[i]])
    
            yield scrapy.Request(url=url_news,
                                  callback=self.parse_subCategory, 
                                  meta={'father_name': response.meta['name'], 
                                        'full_name':cate_name},
                                  dont_filter=True)
        
        

    def parse_subCategory(self,response):
        
        """ 从新闻子类别页面进入到每一则具体新闻的页面 """
        
        full_name = response.meta['full_name']
        go_to_nextpage = True
        
        try:
            # 静态页面
            if self.get_static:
                is_static = True
                print("静态", response.meta['father_name'])
                news_title_list_1 = get_news_link_static(response, response.meta['father_name'])
                #news_title_list_1 = ['http://stock.cfi.cn/p20200325000152.html']
                for url_news in news_title_list_1:
                    # 检查时间
                    current_time = get_time(url_news)
                    if self.end_time < current_time:
                        go_to_nextpage = True
                    elif self.start_time > current_time:
                        go_to_nextpage = False
                    else:
                        # 进入链接
                        yield Request(url = url_news,
                                      callback = self.parse_NewsPage, 
                                      meta = {'full_name':full_name, 
                                              'is_static': is_static,
                                              'first_page': True}, 
                                      dont_filter=True)
                    
                    # print("静态: ",full_name, '   ',url_news)

            # 动态页面
            if self.get_JS:
                is_static = False
                print("动态", response.meta['father_name'])
                news_title_list_2 = get_news_link_JS(response,  response.meta['father_name'])
                #news_title_list_2 = ["http://industry.cfi.cn/newspage.aspx?id=20200323000057&p=0"]
                
                for url_news in news_title_list_2:
                     # 检查时间
                    current_time = get_time(url_news)
                    if self.end_time < current_time:
                        go_to_nextpage = True
                    elif self.start_time > current_time:
                        go_to_nextpage = False
                    else:
                        # 进入链接
                        yield SeleniumRequest(url= url_news,
                                              callback=self.parse_NewsPage, 
                                              meta = {'full_name':full_name, 
                                                      'is_static': is_static,
                                                      'first_page': True}, 
                                              dont_filter=True)
                        # print("动态: ",full_name, '   ',url_news)
     
        except:
            print("此类别新闻已经阅读完毕")
            pass
        else:
            # 统计在此页面抓取到的新闻总数 
            print("-------------------------------------")
            if self.get_static == True and self.get_JS == True:
                num_of_news = len(news_title_list_1)+len(news_title_list_2) 
            elif self.get_static == True and self.get_JS == False:
                num_of_news = len(news_title_list_1)
            elif self.get_static == False and self.get_JS == True:
                num_of_news = len(news_title_list_2)
            else:
                num_of_news = 0
            print("在此页面找到的新闻数目为：", num_of_news)
            
            # 翻页 
            if num_of_news > 0 and go_to_nextpage:
                next_page = "http://industry.cfi.cn/" +  response.xpath('//p[@align = "center"]/a[@style]/@href').extract_first()
                yield scrapy.Request(url=next_page,
                                      callback=self.parse_subCategory, 
                                      meta={'father_name': response.meta['father_name'],
                                            'full_name':response.meta['full_name']},
                                      dont_filter=True)
            
     

            
    def parse_NewsPage(self,response):
         
        ''' 打开新闻页面后抓取里面的标题\正文\时间和网址 '''
        
        news_type, url, time_, title, text, insidePage_link = parse_Page(response)
        text = "".join(text)
        title = title[0]
        
        # 如果有内页，再循环一次
        if insidePage_link:
            for url_news in insidePage_link:
                
                if response.meta['is_static']:
                    yield Request(url= url_news,
                              callback=self.parse_NewsPage, 
                              meta = {'full_name':response.meta['full_name'], 
                                      'is_static': response.meta['is_static'],
                                      'first_page': False},
                              dont_filter=True)
                else:
                    yield SeleniumRequest(url= url_news,
                          callback=self.parse_NewsPage, 
                          meta = {'full_name':response.meta['full_name'], 
                                  'is_static': response.meta['is_static'],
                                  'first_page': False},
                          dont_filter=True)
                    
                
                
        
        print('********************************************************')
        print('news category')
        print(news_type)
        print('url')
        print(url)
        print("title: ")
        print(title)
        print("text: ")
        print(text)
        print("date: ")
        print(time_)
        
        news_path = get_full_path(news_type, url, time_, title, text)
        add_to_exist_file(url, title, time_, text,news_path)

    
    
            
            
