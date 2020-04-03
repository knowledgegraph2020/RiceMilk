import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import datetime
import time
import os
import re


# path = '/Users/cengqiqi/Desktop/data/files_0328/2020-03-28/CifiFinance/期货-能源化工期货/白银雪崩式暴跌 黄金“弃儿”能咸鱼翻身？.txt'
# path = '/Users/cengqiqi/Desktop/data/files_0328/2020-03-28/CifiFinance/产经-经济/英国首相确诊 习近平同美国总统特朗普通电话-更新中.txt'
# path = '/Users/cengqiqi/Desktop/data/files_0328/2020-03-29/NetEaseFinance/car/大乘汽车困境：拖欠员工工资 土地将被政府收回.txt'


def open_current_file(path):
    
    """ 打开路径中的文章获取其 url, title, news_date, text """
        
    #print(path)
    f = open(path, "r")
    elements = f.readlines()
    url = elements[0].rstrip("\n")
    title = elements[1].rstrip("\n")
    news_date = elements[2].rstrip("\n").strip(" ")
    text = elements[3] if len(elements)>= 4 else title # 对于NetEaseFinance没有正文的情况


    # 对于sohu的储存格式
    if url.startswith('//'):
        url = "https:" +url
    
    # 对于sohu和NetEaseFinance的储存格式
    news_date = news_date[0:10]
    
    # 对于有内页的网站
    if len(elements) > 4:
        text_list = []
        text_num = [x for x in range(len(elements)) if (x+1)%4 == 0]
        # 要想让文章出现是有顺序的，利用url的最后一位就可以了
        for i in text_num:
            text_list.append(elements[i])
        text=''.join(text_list) # 合并list的每一段
        
    return url, title, news_date, text


def check_keyword(path, keyword_dict):
    

    #open file
    url, title, news_date, text = open_current_file(path)
    
    # 检查文中出现关键词的次数
    for keyword, weight in keyword_dict.items():   
        
        score = len(re.findall(keyword,text))*weight/len(text)
        # 考虑一下要不要除以文章总长度

    return score

def get_related_news(save_dir, start_date, end_date, keyword_dict):
    
    """ 这个方法将收集的新闻导入进来, 注意！这里的日期指的是储存新闻的日期而不是新闻新闻本身的日期 """
    
    available_date = os.listdir(save_dir)

    date_range = get_date_list(start_date, end_date)
    date_list = [x for x in date_range if x in available_date]
    
    related_news = {}
    
    for current_date in date_list:
    
        path = os.path.join(save_dir, current_date)
        web_folder_list = os.listdir(path)
        web_folder_list = [x for x in web_folder_list if not x.startswith('.') ] # 删除.DS_Store文件
        
        for web_folder in web_folder_list:
            
            path_web = os.path.join(path, web_folder)
            cate_folder_list = os.listdir(path_web)
            cate_folder_list = [x for x in cate_folder_list if not x.startswith('.') ] # 删除.DS_Store文件
        
            for cate_folder in cate_folder_list:
                
                path_cate = os.path.join(path_web, cate_folder)
                file_list = os.listdir(path_cate)
                file_list = [x for x in file_list if not x.startswith('.') ] # 删除.DS_Store文件
        
                for file in file_list:
                    
                    path_file = os.path.join(path_cate, file)
                    score = check_keyword(path_file, keyword_dict)
                    if score>0: related_news[path_file] = score
    
    return related_news


def top_news(candidates, top_n):
    
    """ 这个方法根据related_news中的score排序，选出最相关的top n, 返回一个path list"""
        
    candi_sort = sorted(candidates.items(), key=lambda x: x[1],reverse = True)
    
    if len(candi_sort) > top_n:
        top_temp = candi_sort[0:top_n]
        top_news_list = [x[0] for x in top_temp]
    else:
        top_news_list = [x[0] for x in candi_sort]
        
    return top_news_list

        
def getToday():
    return time.strftime("%Y-%m-%d") 

def get_date_list(start_date, end_date):
    
    """ 获取一个从start到end中间每一天的list, list里面每一个元素是str"""
        
    start = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    end = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    
    date_list = []
    current = start
    while current <= end:
        date_list.append(current.strftime("%Y-%m-%d")) 
        current = current + datetime.timedelta(days=1)

    return date_list 
        