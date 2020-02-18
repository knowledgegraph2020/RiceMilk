from scrapy.spiders import Spider
import scrapy
import RiceMilk.SohuFinance.parse.parse_detail as pdl
from RiceMilk.SohuFinance.parse.process import make_save_dir
import os
import time


class SohuSpider(Spider):
    name = 'sohuFinance'
    start_urls = ['https://business.sohu.com/']

    def parse(self, response):
        news_dict = {}

        # h0
        print("h0================================================")
        headline0_links, headline0_titles = pdl.parse_headline0(response)
        #print(headline0_links, headline0_titles)
        print("The number of {} news is {}.".format("headline0", len(headline0_links)))
        news_dict["headline0"] = {"links": headline0_links, "titles": headline0_titles}

        # h1
        print("h1================================================")
        headline1_links, headline1_titles = pdl.parse_headline1(response)
        #print(headline1_links, headline1_titles)
        print("The number of {} news is {}.".format("headline1", len(headline1_links)))
        news_dict["headline1"] = {"links": headline1_links, "titles": headline1_titles}

        print("财经要闻============================================")
        print("财经新闻============================================")
        financialnews_links, financialnews_titles = pdl.parse_financialnews(response)
        print("The number of {} news is {}.".format("financial", len(financialnews_links)))
        news_dict["financial"] = {"links": financialnews_links, "titles": financialnews_titles}
        #print(financialnews_links, financialnews_titles)

        print("股市理财=============================================")
        stockmoneynews_links, stockmoneynews_titles = pdl.parse_stockmoneynews(response)
        print("The number of {} news is {}.".format("stock_and_money", len(stockmoneynews_links)))
        news_dict["stock_and_money"] = {"links": stockmoneynews_links, "titles": stockmoneynews_titles}

        print("公司产业==============================================")
        companyindustrynews_links, companyindustrynews_titles = pdl.parse_companyindustrynews(response)
        print("The number of {} news is {}.".format("company_and_industry", len(companyindustrynews_links)))
        news_dict["company_and_industry"] = {"links": companyindustrynews_links, "titles": companyindustrynews_titles}

        print("楼市观察,消费白酒======================================")
        estateliquornews_links, estateliquornews_titles = pdl.parse_estateliquornews(response)
        print("The number of {} news is {}.".format("estate_and_liquor", len(estateliquornews_links)))
        news_dict["estate_and_liquor"] = {"links": estateliquornews_links, "titles": estateliquornews_titles}

        print("315曝光,财经人物=======================================")
        businessmen315news_links, businessmen315news_titles = pdl.parse_315businessmennews(response)
        print("The number of {} news is {}.".format("businessmen_and_315", len(businessmen315news_links)))
        news_dict["businessmen_and_315"] = {"links": businessmen315news_links, "titles": businessmen315news_titles}

        print("公司深读===============================================")
        companydeepnews_links, companydeepnews_titles = pdl.parse_companydeepnews(response)
        print("The number of {} news is {}.".format("company_deep", len(companydeepnews_links)))
        news_dict["company_deep"] = {"links": companydeepnews_links, "titles": companydeepnews_titles}

        print("24小时热文=============================================")
        hot24hnews_links, hot24hnews_titles = pdl.parse_hot24hnews(response)
        print("The number of {} news is {}.".format("hotnews_24h", len(hot24hnews_links)))
        news_dict["hotnews_24h"] = {"links": hot24hnews_links, "titles": hot24hnews_titles}

        url_head = 'http:'
        for news_type, news in news_dict.items():
            #print(news_type, news)
            news_links = news['links']
            news_titles = news['titles']
            for i in range(len(news_links)):
                url = news_links[i]
                if url.startswith('//'):
                    yield scrapy.Request(url=url_head + url, callback=self.save_news_cont,
                                         meta={'title': news_titles[i], 'link': url, 'type': news_type})

    def save_news_cont(self, response):
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
