import re
import json
from RiceMilk.tools.http_tools import get_html

def pro_sohu_head_line(url):
    links = []
    titles = []

    soup = get_html(url, 'utf-8')
    scripts = soup.find_all(["script"])

    # 拥有新闻标题以及链接的内容在第二个script里
    head_line_news_text = scripts[1].text

    dym_pat = re.compile(r'dynamicComponents: \[(.*)\]')
    head_line_news_match = dym_pat.search(str(head_line_news_text))
    head_line_news_json = json.loads('[' + head_line_news_match.group(1) + ']')

    # 拥有新闻标题以及链接的内容在第二个dict里
    head_line_news_dict = head_line_news_json[1]
    for key in head_line_news_dict:
        #print(key, head_line_news_dict[key])
        if key == 'data':
            for ele in head_line_news_dict[key]:
                print(ele['link'])
                print(ele['title'])
                links.append(ele['link'][5:])
                titles.append(ele['title'])

    return links, titles

def parse_headline0(response):
    # 头条通常不是一个单独新闻，链接中包含一系列新闻，herf以http开头
    headline0_links = []
    headline0_titles = []
    # // *[ @ id = "main-container"] / div[4] / div[2] / div[1] / div[1] / h1 / a
    head_line_url = response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[1]/div[1]/h1/a/@href').extract_first()
    print(head_line_url)
    if head_line_url.startswith('http'):
        head_line_links, head_line_titles = pro_sohu_head_line(head_line_url)
        headline0_links.extend(head_line_links)
        headline0_titles.extend(head_line_titles)

    for sel in response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[1]/div[1]'):
        title = sel.xpath('.//a/text()').extract()
        link = sel.xpath('.//a/@href').extract()
        headline0_links.extend(link)
        headline0_titles.extend(title)

    return headline0_links, headline0_titles

def parse_headline1(response):
    headline1_links = []
    headline1_titles = []
    # //*[@id="main-container"]/div[4]/div[2]/div[1]/div[2]/h1/a
    # //*[@id="main-container"]/div[4]/div[2]/div[1]/div[2]/p
    for sel in response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[1]/div[2]'):
        title = sel.xpath('.//a/text()').extract()
        link = sel.xpath('.//a/@href').extract()
        # print(title)
        # print(link)
        headline1_links.extend(link)
        headline1_titles.extend(title)

    return headline1_links, headline1_titles

def parse_financialnews(response):
    financialnews_links = []
    financialnews_titles = []
    # //*[@id="main-container"]/div[4]/div[2]/div[2]/ul[1]/li[2]/a
    # //*[@id="main-container"]/div[4]/div[2]/div[2]/ul[2]/li[1]/a
    for sel in response.xpath('//*[@id="main-container"]/div[4]/div[2]/div[2]/ul'):
        for sub_sel in sel.xpath('.//li'):
            title = sub_sel.xpath('.//a/text()').extract()
            link = sub_sel.xpath('.//a/@href').extract()
            # print(title)
            # print(link)
            financialnews_links.extend(link)
            financialnews_titles.extend(title)

    for sel in response.xpath('//*[@id="main-container"]/div[6]/div[1]/div[2]/div/div'):
        for sub_sel in sel.xpath('.//ul'):
            title = sub_sel.xpath('.//a/text()').extract()
            link = sub_sel.xpath('.//a/@href').extract()
            # print(title)
            # print(link)
            financialnews_links.extend(link)
            financialnews_titles.extend(title)

    return financialnews_links, financialnews_titles

# 股市理财
def parse_stockmoneynews(response):
    stockmoneynews_links = []
    stockmoneynews_titles = []
    # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[1]/ul/li[1]/a
    # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[2]/ul/li[1]/a
    for sel in response.xpath('//*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div'):
        for sub_sel in sel.xpath('.//ul'):
            title = sub_sel.xpath('.//a/text()').extract()
            link = sub_sel.xpath('.//a/@href').extract()
            # print(title)
            # print(link)
            stockmoneynews_links.extend(link)
            stockmoneynews_titles.extend(title)

    return stockmoneynews_links, stockmoneynews_titles

# 公司产业
def parse_companyindustrynews(response):
    companyindustrynews_links = []
    companyindustrynews_titles = []
    # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[1]/ul/li[1]/a
    # //*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div[2]/ul/li[1]/a
    for sel in response.xpath('//*[@id="main-container"]/div[6]/div[1]/div[4]/div[2]/div'):
        for sub_sel in sel.xpath('.//ul'):
            title = sub_sel.xpath('.//a/text()').extract()
            link = sub_sel.xpath('.//a/@href').extract()
            # print(title)
            # print(link)
            companyindustrynews_links.extend(link)
            companyindustrynews_titles.extend(title)
    return companyindustrynews_links, companyindustrynews_titles

# 楼市观察,消费白酒
def parse_estateliquornews(response):
    estateliquornews_links = []
    estateliquornews_titles = []
    # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[2]/div[1]/ul/li[1]/a
    # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[2]/div[2]/ul/li[2]/a
    for sel in response.xpath('//*[@id="main-container"]/div[8]/div[1]/div[2]/div[2]/div'):
        for sub_sel in sel.xpath('.//ul'):
            title = sub_sel.xpath('.//a/text()').extract()
            link = sub_sel.xpath('.//a/@href').extract()
            # print(title)
            # print(link)
            estateliquornews_links.extend(link)
            estateliquornews_titles.extend(title)
    return estateliquornews_links, estateliquornews_titles

# 315曝光,财经人物
def parse_315businessmennews(response):
    businessmen315news_links = []
    businessmen315news_titles = []
    # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[3]/div[1]/ul/li[1]/a
    # //*[@id="main-container"]/div[8]/div[1]/div[2]/div[3]/div[2]/ul/li[1]/a
    for sel in response.xpath('//*[@id="main-container"]/div[8]/div[1]/div[2]/div[3]/div'):
        for sub_sel in sel.xpath('.//ul'):
            title = sub_sel.xpath('.//a/text()').extract()
            link = sub_sel.xpath('.//a/@href').extract()
            # print(title)
            # print(link)
            businessmen315news_links.extend(link)
            businessmen315news_titles.extend(title)

    return businessmen315news_links, businessmen315news_titles

# 公司深读
def parse_companydeepnews(response):
    companydeepnews_links = []
    companydeepnews_titles = []
    # //*[@id="main-container"]/div[6]/div[2]/div[2]/div[2]/ul/li[1]/a/span/span
    # //*[@id="main-container"]/div[6]/div[2]/div[2]/div[2]/ul/li[2]/a/span/span
    for sel in response.xpath('//*[@id="main-container"]/div[6]/div[2]/div[2]/div[2]/ul/li'):
        title = sel.xpath('a/span/span/text()').extract()
        link = sel.xpath('a/span/span/@href').extract()
        # print(title)
        # print(link)
        companydeepnews_links.extend(link)
        companydeepnews_titles.extend(title)

    return companydeepnews_links, companydeepnews_titles

# 24小时热文
def parse_hot24hnews(response):
    hot24hnews_links = []
    hot24hnews_titles = []
    # //*[@id="main-container"]/div[8]/div[2]/div[2]/div[2]/ul/li[1]/a/span/span
    # //*[@id="main-container"]/div[8]/div[2]/div[2]/div[2]/ul/li[2]/a/span/span
    for sel in response.xpath('//*[@id="main-container"]/div[8]/div[2]/div[2]/div[2]/ul/li'):
        title = sel.xpath('a/span/span/text()').extract()
        link = sel.xpath('a/span/span/@href').extract()
        # print(title)
        # print(link)
        hot24hnews_links.extend(link)
        hot24hnews_titles.extend(title)

    return hot24hnews_links, hot24hnews_titles



