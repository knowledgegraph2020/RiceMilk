#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:10:53 2020

@author: cengqiqi
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import datetime
import time
import os
import re

import RiceMilk.autoSender.config as cfg
import RiceMilk.autoSender.newsSearhcer as ns


def send_email(receivers, news_num, save_dir, start_date, end_date, keyword_dict):
    
    
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


    # 设置邮件
    message =  MIMEMultipart()
    message['From'] = Header("邮件推送程序", 'utf-8')   # 发送者
    message['To'] =  Header("对公天团", 'utf-8')        # 接收者
    
    # 添加附件
    for i in range(len(top_path_list)):
        att = MIMEApplication(open(top_path_list[i], 'rb').read())
        att.add_header('Content-Disposition', 'attachment', filename= f"{title_list[i]}.txt")
        message.attach(att)
    
    # 邮件正文
    text = '大家好，这里是这一周的相关新闻，具体内容可以点击附件下载 ... '
    mail_msg = """
                <p>大家好，这里是这一周的相关新闻，具体内容可以点击链接查看，或者在附件下载 ...</p>
                <p><a href= "{url0}">{date0} - {title0}</a></p>
                <p><a href= "{url1}">{date1} - {title1}</a></p>
                <p><a href= "{url2}">{date2} - {title2}</a></p>
                <p><a href= "{url3}">{date3} - {title3}</a></p>
                <p><a href= "{url4}">{date4} - {title4}</a></p>
                """.format(url0 = url_list[0], date0 = news_date_list[0], title0 = title_list[0],
                url1 = url_list[1], date1 = news_date_list[1], title1 = title_list[1],
                url2 = url_list[2], date2 = news_date_list[2], title2 = title_list[2],
                url3 = url_list[3], date3 = news_date_list[3], title3 = title_list[3],
                url4 = url_list[4], date4 = news_date_list[4], title4 = title_list[4])
    message.attach(MIMEText(mail_msg, 'html', 'utf-8'))
     
    
    # 邮件标题 
    subject = '对公业务小组新闻推送 ({date})'.format(date = ns.getToday())
    message['Subject'] = Header(subject, 'utf-8')
     
    # 邮件发送
    sender = '279392235@qq.com' 
    
    
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        sender_email = input("请输入发送者邮箱： ")
        sender_password = input("请输入发件人邮箱授权码： ")
        s.login(sender_email,sender_password);
        
        for group_member in receivers:
            s.sendmail(sender, group_member, message.as_string())
            print(f"邮件发送成功: {group_member}")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")




