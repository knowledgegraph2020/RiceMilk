import re
import json
import scrapy
from scrapy import Request
from RiceMilk.tools.http_tools import get_html
from termcolor import colored



def get_news_link_static(response, father_cate):
    
    """ 标题前不带<script>标签的文章 """
    
    # 抓取文章链接
    if father_cate == "产经":
        news_title_list_1 = response.xpath('//td[@class="zitd2"]//div[@class="zidiv2"]/a//@href').extract() # 新闻标题列表
    if father_cate == "股票":
        news_title_list_1 = response.xpath('//*[@class = "xinwen"]/a/@href').extract() # 新闻标题列表
    if father_cate == "期货":
        news_title_list_1 = response.xpath('//*[@class = "lanmuye_xinwen"]/a/@href').extract() # 新闻标题列表
    if father_cate == "外汇":
        news_title_list_1 = response.xpath('//*[@class = "lanmuye_xinwen"]/a/@href').extract() # 新闻标题列表

        
    #打开文章抓取文章内容
    news_link_1 = []
    for x in news_title_list_1:
        
        url_news = "http://industry.cfi.cn/" +  x
        news_link_1.append(url_news)
        
    return news_link_1
    
def get_news_link_JS(response, father_cate):
    
    """ 带<script>标签的标题无法抓取到，在这里给它补上"""
    # 抓取文章链接
    if father_cate == "产经":
        news_title_list_2_temp = response.xpath('//td[@class="zitd2"]//div[@class="zidiv2"]/script[starts-with(text(),"unes")]').extract() 
    if father_cate == "股票":
        news_title_list_2_temp = response.xpath('//*[@class = "xinwen"]/script[starts-with(text(),"unes")]').extract() 
    if father_cate == "期货":
        news_title_list_2_temp = response.xpath('//*[@class = "lanmuye_xinwen"]/script[starts-with(text(),"unes")]').extract() 
    if father_cate == "外汇":
        news_title_list_2_temp = response.xpath('//*[@class = "lanmuye_xinwen"]/script[starts-with(text(),"unes")]').extract() 
        
        
    news_title_list_2 = [] 
    
    for i in news_title_list_2_temp:
        number = re.sub("\D","",i)
        title_ = 'p'+number+'.html'
        news_title_list_2.append(title_)
        
    news_link_2 = []
    for x in news_title_list_2:
        url_news = "http://industry.cfi.cn/" +  x
        news_link_2.append(url_news)
        
    return news_link_2


def parse_Page(response, first_page = True):

    
    ''' 打开新闻页面的标题和正文 '''

    jianxun = False
    #print("进入parse_2")
    
    ### date ##############################################################
    time_ = get_time(response.url)
    
    
    ### title ############################################################
    title = response.xpath('//h1/text()').extract()
    
    # 有的新闻是一条简讯 简讯类型1 # http://industry.cfi.cn/p20200313000229.html
    if not title:
        title = response.xpath('//table[@id = "pccontent"]//div[@id = "tdcontent"]/div/text()').extract()
        jianxun = True
    
    # 有的新闻是一条简讯 简讯类型2 # http://industry.cfi.cn/p20191207000081.html
    if not title:
        title = response.xpath('//table[@id = "pccontent"]//div[@id = "tdcontent"]//text()').extract()
        jianxun = True
    
    # 以防有的页面抓取错误 # http://industry.cfi.cn/p20200318000207.html
    if len(title[0]) > 50:
        title = []
    
    ### text #############################################################
    #text = 'coming later'
    
    # 检查一下是不是新闻文章有内页
    insidePage_link = [] # 搜集其他内页的link返回到上一层
    check_insidePage = [] # 检查本页是否有其他内页的link，还是说本页没有内页呢
    if response.meta['first_page']:
        check_insidePage = response.xpath('//nobr/a/@href').extract()
        check_insidePage = list(set(check_insidePage)) # 去重
    
        
    
    # 有内页的新闻文章 # http://industry.cfi.cn/newspage.aspx?id=20200323000057&p=0
    if check_insidePage:
    
        # 有可能每一页的格式都不一样
        text_div = response.xpath('//*[@id = "tdcontent"]/text() | //*[@id = "tdcontent"]/div/text() | //*[@id = "tdcontent"]/a/text()').extract()
        
        
        text=[]
        for element in text_div:
            element = element.strip() # 删掉句子前后空格
            if element: text.append(element) # 删掉全是空格的句子
            
        # 把剩余几页传回上一层，再走一遍这个方法
        insidePage_link =["http://industry.cfi.cn/" +  page for page in check_insidePage]
        print(colored("出现了有内页的新闻网站",'red'))
        print(colored(insidePage_link,'red'))
    # 为简讯的文章
    elif jianxun:
        text = title
    # 以防万一没抓到标题的文章
    elif not title:
        text = []
    # 正常新闻的文章
    else:
        text = []
        if response.meta['is_static']:
            text_div = response.xpath('//*[@id = "tdcontent"]/text()| //*[@id = "tdcontent"]/a/text()').extract()
        else:
            text_div = response.xpath("//*[@id = 'tdcontent']//div[name(.)!='script']//text()[name(.)!='h1']").extract()
         
        for element in text_div:
            element = element.strip() # 删掉句子前后空格
            if element: text.append(element) # 删掉全是空格的句子
            
    ### check #######################################################
        
    # 删除已经不存在的页面
    if title[0] == '--*该页面不存在--' or title[0] == '--~该页面不存在--':
        title = []
        text = []
        
    # 确保成功抓取了标题和文本
    elif title and text: 
        return response.meta['full_name'], response.url, time_, title,text, insidePage_link
               
    # 若还有页面没有被抓取到，输出页面的head信息
    else:
        print(colored("Warning: 这一页有一些信息没有被抓取到",'red'))
        print(colored("response.url",'red'))
        print(colored(response.xpath('//head/title').extract(),'red'))
     



def get_time(url):
    
    num = re.sub("\D","", url)
    year = num[0:4]
    month = num[4:6]
    day = num[6:8]
    time_ = '-'.join([year,month,day])
    
    return time_
            