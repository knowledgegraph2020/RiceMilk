#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:43:35 2020

@author: cengqiqi
"""

import requests


import RiceMilk.autoSender.config as cfg
import RiceMilk.autoSender.newsSearhcer as ns

import argparse
import datetime

###############################################################################

def send_wechat(sckey_list, news_num, save_dir, start_date, end_date, keyword_dict):
    # 找到相关文章的路径
    related = ns.get_related_news(save_dir, start_date, end_date, keyword_dict)
    top_path_list = ns.top_news(related, news_num)
    
    # 获取文章标题\文章链接
    url_list = []
    title_list = []
    news_date_list= []
    for path in top_path_list: 
        url, title, news_date, text = ns.open_current_file(path)
        url_list.append(url)
        title_list.append(title)
        news_date_list.append(news_date)
        
        
    # 微信推送
    
    title = "对公业务组新闻推送"
    
    text = ('大家好，以下是这一周的新闻推送内容\n\n'
            '{date0} - {title0}: {url0} \n\n '
            '{date1} - {title1}: {url1} \n\n '
            '{date2} - {title2}: {url2} \n\n '
            '{date3} - {title3}: {url3} \n\n '
            '{date4} - {title4}: {url4} \n\n').format(
            date0 = news_date_list[0], title0 = title_list[0], url0 = url_list[0],
            date1 = news_date_list[1], title1 = title_list[1], url1 = url_list[1],
            date2 = news_date_list[2], title2 = title_list[2], url2 = url_list[2],
            date3 = news_date_list[3], title3 = title_list[3], url3 = url_list[3],
            date4 = news_date_list[4], title4 = title_list[4], url4 = url_list[4],
            )
    
    
    #text为推送的title,desp为推送的描述
    for sckey in sckey_list:
        url = 'https://sc.ftqq.com/{sckey}.send?text={title}&desp={text}'\
            .format(sckey = sckey, title = title, text = text)
        requests.get(url)
        
