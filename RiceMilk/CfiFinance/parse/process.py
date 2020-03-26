import RiceMilk.CfiFinance.parse.config as cfg
import scrapy
import time
import os


def make_save_dir(news_type):
    today_ = time.strftime("%Y-%m-%d")
    #cfi_save_dir = os.path.join(cfg.save_dir, today_, 'CifiFinance', news_type)
    cfi_save_dir = os.path.join( "/Users/cengqiqi/Desktop/data/", today_, 'CifiFinance', news_type)
    if not os.path.exists(cfi_save_dir):
        os.makedirs(cfi_save_dir)
    return cfi_save_dir



def save_news_cont(news_type, url, time_, title, text):
    
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
        
        
        
        

def convert_to_file(link, main_title, dt, content, path):

    merge_path = path
    
    with open(merge_path, 'a') as f:
        f.write(link + "\n")
        f.write(main_title + "\n")
        f.write(dt + "\n")
        f.write(content+ "\n")
        
        
        
        
        