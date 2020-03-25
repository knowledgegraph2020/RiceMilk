from scrapy.spiders import Spider
import scrapy
import RiceMilk.SohuFinance.parse.parse_detail as pdl
from RiceMilk.SohuFinance.parse.process import make_save_dir, get_logger
from RiceMilk.tools.file_tools import convert_to_file
import time

logger = get_logger()
class SohuSpider(Spider):
    name = 'sohuFinance'
    start_urls = ['https://business.sohu.com/']

    def parse(self, response):
        news_dict = {}

        # h0
        logger.info("h0================================================")
        try:
            headline0_links, headline0_titles = pdl.parse_headline0(response)

            logger.info("The number of {} news is {}.".format("headline0", len(headline0_links)))
            news_dict["headline0"] = {"links": headline0_links, "titles": headline0_titles}
        except Exception:
            logger.error("headLine0 error!!!", exc_info=1)


        # h1
        logger.info("h1================================================")
        headline1_links, headline1_titles = pdl.parse_headline1(response)
        logger.info("The number of {} news is {}.".format("headline1", len(headline1_links)))
        news_dict["headline1"] = {"links": headline1_links, "titles": headline1_titles}

        logger.info("财经要闻============================================")
        logger.info("财经新闻============================================")
        financialnews_links, financialnews_titles = pdl.parse_financialnews(response)
        logger.info("The number of {} news is {}.".format("financial", len(financialnews_links)))
        news_dict["financial"] = {"links": financialnews_links, "titles": financialnews_titles}

        logger.info("股市理财=============================================")
        stockmoneynews_links, stockmoneynews_titles = pdl.parse_stockmoneynews(response)
        logger.info("The number of {} news is {}.".format("stock_and_money", len(stockmoneynews_links)))
        news_dict["stock_and_money"] = {"links": stockmoneynews_links, "titles": stockmoneynews_titles}

        logger.info("楼市观察,消费白酒======================================")
        estateliquornews_links, estateliquornews_titles = pdl.parse_estateliquornews(response)
        logger.info("The number of {} news is {}.".format("estate_and_liquor", len(estateliquornews_links)))
        news_dict["estate_and_liquor"] = {"links": estateliquornews_links, "titles": estateliquornews_titles}

        logger.info("315曝光,财经人物=======================================")
        businessmen315news_links, businessmen315news_titles = pdl.parse_315businessmennews(response)
        logger.info("The number of {} news is {}.".format("businessmen_and_315", len(businessmen315news_links)))
        news_dict["businessmen_and_315"] = {"links": businessmen315news_links, "titles": businessmen315news_titles}

        logger.info("公司深读===============================================")
        companydeepnews_links, companydeepnews_titles = pdl.parse_companydeepnews(response)
        logger.info("The number of {} news is {}.".format("company_deep", len(companydeepnews_links)))
        news_dict["company_deep"] = {"links": companydeepnews_links, "titles": companydeepnews_titles}

        logger.info("24小时热文=============================================")
        hot24hnews_links, hot24hnews_titles = pdl.parse_hot24hnews(response)
        logger.info("The number of {} news is {}.".format("hotnews_24h", len(hot24hnews_links)))
        news_dict["hotnews_24h"] = {"links": hot24hnews_links, "titles": hot24hnews_titles}

        url_head = 'http:'
        for news_type, news in news_dict.items():
            # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
            # print(news_type)
            # print(news)
            news_links = news['links']
            news_titles = news['titles']
            for i in range(len(news_links)):
                url = news_links[i]
                if url.startswith('//'):
                    yield scrapy.Request(url=url_head + url, callback=self.save_news_cont,
                                         meta={'title': news_titles[i], 'link': url, 'type': news_type})

    def save_news_cont(self, response):
        def hanzi_only(text):
            return "".join([char for char in text if '\u4e00' <= char <= '\u9fff'])

        title = response.meta['title']
        #title = title.replace("/", "|")
        #title = hanzi_only(title)
        news_type = response.meta['type']
        sohu_save_path = make_save_dir(news_type)

        link = response.meta['link']

        content = response.xpath('//*[@id="mp-editor"]//p//text()').extract()
        cont = "".join(content).replace("/n","")
        news_time = response.xpath('//*[@id="news-time"]//text()').extract()
        #print(news_time)
        if news_time:
            news_time = news_time[0]
        else:
            news_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

        convert_to_file(link, title, news_time, cont, sohu_save_path)
        logger.info("news_type: {}, news_title: {}, news_link: {}, news_date: {}".format(news_type, title, link, news_time))
