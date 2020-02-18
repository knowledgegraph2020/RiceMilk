import RiceMilk.SohuFinance.parse.config as cfg
import scrapy
import time
import os

# def make_save_dir():
#     today_ = time.strftime("%Y-%m-%d")
#     sohu_save_dir = os.path.join(cfg.save_dir, today_, 'SohuFinance')
#     if not os.path.exists(sohu_save_dir):
#         os.makedirs(sohu_save_dir)
#     return sohu_save_dir

def make_save_dir(news_type):
    today_ = time.strftime("%Y-%m-%d")
    sohu_save_dir = os.path.join(cfg.save_dir, today_, 'SohuFinance', news_type)
    if not os.path.exists(sohu_save_dir):
        os.makedirs(sohu_save_dir)
    return sohu_save_dir

def save_news_cont(response):
    title = response.meta['title']
    title = title.replace("/", "|")
    news_type = response.meta['type']
    sohu_save_path = make_save_dir(news_type)
    news_path = os.path.join(sohu_save_path, title + '.txt')
    with open(news_path, 'w') as wf:

        print(title, response.meta['link'])

        content = response.xpath('//*[@id="mp-editor"]//p//text()').extract()
        cont = "".join(content)
        news_time = response.xpath('//*[@id="news-time"]//text()').extract()
        print(news_time)
        if news_time:
            wf.write(news_time[0] + '\n')
        else:
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
            wf.write(now + '\n')
        wf.write(cont)

