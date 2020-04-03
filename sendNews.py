#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:06:16 2020

@author: cengqiqi
"""

import RiceMilk.autoSender.config as cfg
import RiceMilk.autoSender.emailSender  as emailSender
import RiceMilk.autoSender.wechatSender  as wechatSender
import argparse
import datetime


def auto_date_range():
    
    """ 获取过去一周的起始时间"""
    
    end = datetime.date.today()
    start = end - datetime.timedelta(days=7)
    
    start = start.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    
    return start, end

start, end = auto_date_range()

 
        
# 添加传入参数
parser = argparse.ArgumentParser(description='Auto Email Sender')

parser.add_argument("--save_dir", type=str, default = cfg.save_dir)

parser.add_argument("--keyword_dict", type=str, action='append', default = ['中信=0.8'])
parser.add_argument("--receivers", type=str, action='append', default = ['zengqiqi31@yeah.net'])
parser.add_argument("--news_num", type=int, default = 5)
parser.add_argument("--start_date", type=str, default = start)
parser.add_argument("--end_date", type=str, default = end)
parser.add_argument("--sckey_list", type=str, action='append', default = ['SCU91267T8c899534da1c2ca492c24758dc43771f5e7d5995dc1c3'])

args = parser.parse_args()


keyword_and_weight = args.keyword_dict
keyword_dict ={}
for x in keyword_and_weight:
    key, value = x.split("=")
    keyword_dict[key] = float(value)
    
save_dir = args.save_dir
receivers = args.receivers
news_num = args.news_num
start_date = args.start_date
end_date = args.end_date
sckey_list = args.sckey_list


print(receivers)
print(keyword_dict)

# class sendEmail():
    
#     def __init__(self, save_dir, keyword_dict, receivers,
#                  news_num, start_date, end_date):
#         self.save_dir =  save_dir
#         self.keyword_dict = keyword_dict
#         self.receivers = receivers
#         self.news_num = news_num
#         self.start_date = start_date
#         self.end_date = end_date


#save_dir = cfg.save_dir
#save_dir = '/Users/cengqiqi/Desktop/data/files_0328/'
#keyword_dict = {'中信':0.8, '银行':0.2}

#save_dir = '/data/files/'



#receivers = ['zengqiqi31@yeah.net']
# news_num = 5
# start_date = '2020-03-25'
# end_date = '2020-03-28'

emailSender.send_email(receivers, news_num, save_dir, start_date, end_date, keyword_dict)
wechatSender.send_wechat(sckey_list, news_num, save_dir, start_date, end_date, keyword_dict)


