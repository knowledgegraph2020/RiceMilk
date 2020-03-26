import RiceMilk.CfiFinance.parse.config as cfg
import scrapy
import time
import os
import datetime


def make_save_dir(news_type):
    today_ = time.strftime("%Y-%m-%d")
    #cfi_save_dir = os.path.join(cfg.save_dir, today_, 'CifiFinance', news_type)
    cfi_save_dir = os.path.join( cfg.save_dir, today_, 'CifiFinance', news_type)
    if not os.path.exists(cfi_save_dir):
        os.makedirs(cfi_save_dir)
    return cfi_save_dir



def get_full_path(news_type, url, time_, title, text):
    
    # title = title[0]
    Cfi_save_path = make_save_dir(news_type)
    news_path = os.path.join(Cfi_save_path, title + '.txt')

    return news_path
    # with open(news_path, 'a') as wf: # 加入新内容而不是覆盖

    #     print(title, url)
    #     content = text
    #     cont = "".join(content)
    #     news_time = time_
    #     wf.write(cont) 
        
        
        
  
def getToday():
    return time.strftime("%Y-%m-%d")

def getYesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    yesterday = str(yesterday)
    return yesterday    

        
        
        
        
        