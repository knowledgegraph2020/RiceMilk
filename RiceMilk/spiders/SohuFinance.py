from scrapy.spiders import Spider
import scrapy
from RiceMilk.tools.http_tools import get_html
from RiceMilk.SohuFinance.parse.parse_detail import pro_sohu_head_line
from RiceMilk.SohuFinance.parse.process import make_save_dir
import os
import time


class SohuSpider(Spider):
    name = 'sohuFinance'
    start_urls = ['https://business.sohu.com/']

    def parse(self, response):
        # http_links = []
        news_links = []
        news_titles = []

        # 头条通常不是一个单独新闻，链接中包含一系列新闻，herf以http开头
        # // *[ @ id = "main-container"] / div[4] / div[2] / div[1] / div[1] / h1 / a
        head_line_url = response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[1]/div[1]/h1/a/@href').extract_first()
        print(head_line_url)
        if head_line_url.startswith('http'):
            head_line_links, head_line_titles = pro_sohu_head_line(head_line_url)
            news_links.extend(head_line_links)
            news_titles.extend(head_line_titles)

        # h0
        print("h0================================================")
        for sel in response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[1]/div[1]'):
            title = sel.xpath('.//a/text()').extract()
            link = sel.xpath('.//a/@href').extract()
            print(title)
            print(link)
            news_links.extend(link)
            news_titles.extend(title)

        #h1
        print("h1================================================")
        #//*[@id="main-container"]/div[4]/div[2]/div[1]/div[2]/h1/a
        #//*[@id="main-container"]/div[4]/div[2]/div[1]/div[2]/p
        for sel in response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[1]/div[2]'):
            title = sel.xpath('.//a/text()').extract()
            link = sel.xpath('.//a/@href').extract()
            print(title)
            print(link)
            news_links.extend(link)
            news_titles.extend(title)

        print("财经要闻=================================================")
        #//*[@id="main-container"]/div[4]/div[2]/div[2]/ul[1]/li[2]/a
        #//*[@id="main-container"]/div[4]/div[2]/div[2]/ul[2]/li[1]/a
        for sel in response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[2]/ul'):
            for sub_sel in sel.xpath('.//li'):
                title = sub_sel.xpath('.//a/text()').extract()
                link = sub_sel.xpath('.//a/@href').extract()
                print(title)
                print(link)
                news_links.extend(link)
                news_titles.extend(title)

        # 财经新闻
        print("财经新闻=================================================")
        # //*[@id="main-container"]/div[6]/div[1]/div[2]/div/div[1]/ul/li[1]/a
        # //*[@id="main-container"]/div[6]/div[1]/div[2]/div/div[2]/ul/li[1]/a
        for sel in response.xpath('//*[@id="main-container"]/div[6]/div[1]/div[2]/div/div'):
            for sub_sel in sel.xpath('.//ul'):
                title = sub_sel.xpath('.//a/text()').extract()
                link = sub_sel.xpath('.//a/@href').extract()
                print(title)
                print(link)
                news_links.extend(link)
                news_titles.extend(title)

        # 股市理财
        print("股市理财=================================================")
        # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[1]/ul/li[1]/a
        # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[2]/ul/li[1]/a
        for sel in response.xpath('//*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div'):
            for sub_sel in sel.xpath('.//ul'):
                title = sub_sel.xpath('.//a/text()').extract()
                link = sub_sel.xpath('.//a/@href').extract()
                print(title)
                print(link)
                news_links.extend(link)
                news_titles.extend(title)

        # 公司产业
        print("公司产业=================================================")
        # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[1]/ul/li[1]/a
        # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[2]/ul/li[1]/a
        for sel in response.xpath('//*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div'):
            for sub_sel in sel.xpath('.//ul'):
                title = sub_sel.xpath('.//a/text()').extract()
                link = sub_sel.xpath('.//a/@href').extract()
                print(title)
                print(link)
                news_links.extend(link)
                news_titles.extend(title)

        # 楼市观察,消费白酒
        print("楼市观察,消费白酒=================================================")
        # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[2]/div[1]/ul/li[1]/a
        # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[2]/div[2]/ul/li[2]/a
        for sel in response.xpath('//*[@id="main-container"]/div[8]/div[1]/div[2]/div[2]/div'):
            for sub_sel in sel.xpath('.//ul'):
                title = sub_sel.xpath('.//a/text()').extract()
                link = sub_sel.xpath('.//a/@href').extract()
                print(title)
                print(link)
                news_links.extend(link)
                news_titles.extend(title)

        print(news_links)
        print(len(news_links))
        url_head = 'http:'
        for i in range(len(news_links)):
            url = news_links[i]
            if url.startswith('//'):
                yield scrapy.Request(url=url_head + url, callback=self.process_news_link, meta={'title': news_titles[i], 'link': url})

        # 315曝光,财经人物
        print("315曝光,财经人物=================================================")
        # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[3]/div[1]/ul/li[1]/a
        # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[3]/div[2]/ul/li[1]/a
        for sel in response.xpath('//*[@id="main-container"]/div[8]/div[1]/div[2]/div[3]/div'):
            for sub_sel in sel.xpath('.//ul'):
                title = sub_sel.xpath('.//a/text()').extract()
                link = sub_sel.xpath('.//a/@href').extract()
                print(title)
                print(link)
                news_links.extend(link)
                news_titles.extend(title)

        print(news_links)
        print(len(news_links))
        url_head = 'http:'
        for i in range(len(news_links)):
            url = news_links[i]
            if url.startswith('//'):
                yield scrapy.Request(url=url_head + url, callback=self.process_news_link,
                                     meta={'title': news_titles[i], 'link': url})

        # 公司深读
        print("公司深读=================================================")
        # //*[@id="main-container"]/div[6]/div[2]/div[2]/div[2]/ul/li[1]/a/span/span
        # //*[@id="main-container"]/div[6]/div[2]/div[2]/div[2]/ul/li[2]/a/span/span
        for sel in response.xpath('//*[@id="main-container"]/div[6]/div[2]/div[2]/div[2]/ul/li'):
            title = sel.xpath('a/span/span/text()').extract()
            link = sel.xpath('a/span/span/@href').extract()
            print(title)
            print(link)
            news_links.extend(link)
            news_titles.extend(title)

        print(news_links)
        print(len(news_links))
        url_head = 'http:'
        for i in range(len(news_links)):
            url = news_links[i]
            if url.startswith('//'):
                yield scrapy.Request(url=url_head + url, callback=self.process_news_link,
                                     meta={'title': news_titles[i], 'link': url})

        # 24小时热文
        print("24小时热文=================================================")
        # //*[@id="main-container"]/div[8]/div[2]/div[2]/div[2]/ul/li[1]/a/span/span
        # //*[@id="main-container"]/div[8]/div[2]/div[2]/div[2]/ul/li[2]/a/span/span
        for sel in response.xpath('//*[@id="main-container"]/div[8]/div[2]/div[2]/div[2]/ul/li'):
            title = sel.xpath('a/span/span/text()').extract()
            link = sel.xpath('a/span/span/@href').extract()
            print(title)
            print(link)
            news_links.extend(link)
            news_titles.extend(title)

        print(news_links)
        print(len(news_links))
        url_head = 'http:'
        for i in range(len(news_links)):
            url = news_links[i]
            if url.startswith('//'):
                yield scrapy.Request(url=url_head + url, callback=self.process_news_link,
                                     meta={'title': news_titles[i], 'link': url})

    def process_news_link(self, response):
        title = response.meta['title']
        title = title.replace("/", "|")
        sohu_save_path = make_save_dir()
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
