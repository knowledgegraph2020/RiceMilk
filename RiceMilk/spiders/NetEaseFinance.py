# -*- coding: utf-8 -*-
import random
import logging
import scrapy

from RiceMilk.NetEaseFinance.parse.process import parse_international, parse_HKstock, parse_house, parse_car, \
    parse_financial
from RiceMilk.config.init import user_agent_list
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NeteasefinanceSpider(scrapy.Spider):
    name = 'NetEaseFinance'
    allowed_domains = ['money.163.com/']

    # 随机选择模拟浏览器
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }

    def __init__(self, start=None, end=None, *args, **kwargs):
        if start == 'None':
            self.start = None
        else:
            self.start = start
        self.end = end

    def start_requests(self):
        urls = [
            'https://money.163.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # links
        links = []
        names = []
        # 国际
        international_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[2]/a[2]/@href").extract()
        international_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[2]/a[2]/text()").extract()
        links.extend(international_href)
        names.extend(international_name)
        # 股票
        stock_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[1]/@href").extract()
        stock_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[1]/text()").extract()
        links.extend(stock_href)
        names.extend(stock_name)
        # 科创板
        sci_tech_board_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[3]/@href").extract()
        sci_tech_board_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[3]/text()").extract()
        links.extend(sci_tech_board_href)
        names.extend(sci_tech_board_name)
        # 美股
        US_stock_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[4]/@href").extract()
        US_stock_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[4]/text()").extract()
        links.extend(US_stock_href)
        names.extend(US_stock_name)
        # 港股
        HK_stock_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[5]/@href").extract()
        HK_stock_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[5]/text()").extract()
        links.extend(HK_stock_href)
        names.extend(HK_stock_name)
        # 易会满频道
        yihuiman_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[6]/@href").extract()
        yihuiman_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[3]/a[6]/text()").extract()
        links.extend(yihuiman_href)
        names.extend(yihuiman_name)
        # 商业
        business_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[4]/a[1]/@href").extract()
        business_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[4]/a[1]/text()").extract()
        links.extend(business_href)
        names.extend(business_name)
        # 房产
        house_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[4]/a[2]/@href").extract()
        house_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[4]/a[2]/text()").extract()
        links.extend(house_href)
        names.extend(house_name)
        # 汽车
        car_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[4]/a[3]/@href").extract()
        car_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[4]/a[3]/text()").extract()
        links.extend(car_href)
        names.extend(car_name)
        # 基金
        fund_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[5]/a[1]/@href").extract()
        fund_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[5]/a[1]/text()").extract()
        links.extend(fund_href)
        names.extend(fund_name)
        # 理财
        finance_href = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[5]/a[3]/@href").extract()
        finance_name = response.xpath(
            "//*[@id=\"index2016_wrap\"]/div/div[3]/div[2]/div[2]/div/div[2]/div/span[5]/a[3]/text()").extract()
        links.extend(finance_href)
        names.extend(finance_name)

        name_link = dict(zip(links,names))

        for url in links:
            yield scrapy.Request(url=url,
                                 callback=self.parse_subtitle,
                                 dont_filter=True,
                                 meta={'name':name_link.get(url)},
                                 headers=self.headers)

    def parse_subtitle(self,response):
        name = response.meta['name']

        if name == '国际':
            logger.info('parsing international.....')
            parse_international(response,self.start,self.end)
            logger.info('parsed international.....')
        elif name == '港股':
            logger.info('parsing HK stock.....')
            parse_HKstock(response,self.start,self.end)
            logger.info('parsed HK stock.....')
        elif name == '房产':
            logger.info('parsing housing.....')
            parse_house(response,self.start,self.end)
            logger.info('parsed housing.......')
        elif name == '汽车':
            logger.info('parsing car.....')
            parse_car(response, self.start, self.end)
            logger.info('parsed car.......')
        elif name == '理财':
            logger.info('parsing fiancial.....')
            parse_financial(response,self.start,self.end)
            logger.info('parsed fiancial.......')
