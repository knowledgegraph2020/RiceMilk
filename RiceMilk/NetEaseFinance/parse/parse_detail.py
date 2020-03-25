from bs4 import BeautifulSoup

from RiceMilk.tools.file_tools import convert_to_file
from RiceMilk.tools.http_tools import get_html
import pandas as pd
import re
from RiceMilk.tools.time_tools import format_dt, compare_dt


def get_next_html(url):
    '''
    获取下一页的html，并将转化编码格式
    :param url:
    :return:
    '''
    try:
        return get_html(url)
    except:
        return None


def get_all_urls_by_link(links,
                         path,
                         main_tile_style='#epContentLeft > h1',
                         dt_style='#epContentLeft > div.post_time_source',
                         content_style='#endText > p'):
    pattern = re.compile("[\u4e00-\u9fa5]")
    if links is not None:
        for l in links:
            try:
                data = get_html(l)
                main_title = data.select_one(main_tile_style).get_text().replace("\n", "")
                dt = data.select_one(dt_style).get_text().replace("\n", "")
                content = data.select(content_style)
                content = [c.get_text() for c in content if re.match(pattern, c.get_text())]
                content = ''.join(content).replace("\n", "")
                convert_to_file(l, main_title, dt, content, path)
            except Exception as e:
                print(e)
                continue


def recursive_international(response, path):
    recursive(response, path)


def range_recursive_international(response, start_dt, end_dt, path):
    range_recursive(response, start_dt, end_dt, path)


def recursive(response, path):
    # 递归获取所有新闻
    links = response.css('div.item_top h2 a::attr(href)').getall()
    next_link = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@href').extract()
    next_link = next_link[0]
    next_name = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@title').extract()
    next_name = next_name[0]
    get_all_urls_by_link(links, path)

    cnt = 1
    while True:
        cnt += 1
        if next_name != '下一页':
            break
        data = get_next_html(next_link)
        if data is not None:
            links = data.select('div.item_top > h2 > a[href]')
            links = [l['href'] for l in links]
            get_all_urls_by_link(links, path)
            next_btn = data.select_one(
                '#money_wrap > div > div.area_list.clearfix > div.col_l > div.list_page > li:nth-child(9) > a')
            next_link = next_btn['href']
            next_name = next_btn['title']


def range_recursive(response, start_dt, end_dt, path):
    df = pd.DataFrame()
    # get news from start date to end date
    links = response.css('div.item_top h2 a::attr(href)').getall()
    times = response.css('div.item_top span.time::text').getall()
    times = [format_dt(t) for t in times]
    next_link = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@href').extract()
    next_link = next_link[0]
    next_name = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@title').extract()
    next_name = next_name[0]

    df['dt'] = pd.to_datetime(times)
    start_dt = pd.to_datetime(start_dt)
    end_dt = pd.to_datetime(end_dt)
    df['link'] = links
    filtered = df[(df['dt'] >= start_dt) & (df['dt'] <= end_dt)]
    if 0 < len(filtered) <= len(times):
        result = filtered['link'].to_list()
        get_all_urls_by_link(result, path)

    cnt = 1
    del df
    while True:
        cnt += 1
        df = pd.DataFrame()

        if next_name != '下一页':
            break
        data = get_next_html(next_link)
        if data is not None:
            issused_time = data.find_all('span', attrs={'class': 'time'})
            issused_time = [i.get_text() for i in issused_time]
            links = data.select('div.item_top > h2 > a[href]')
            links = [l['href'] for l in links]

            df['dt'] = pd.to_datetime(issused_time)
            df['link'] = links
            filtered = df[(df['dt'] >= start_dt) & (df['dt'] <= end_dt)]
            result = filtered['link'].to_list()

            if 0 < len(result) <= len(issused_time):
                get_all_urls_by_link(result, path)
            elif len(issused_time) == len(result) and (
                    [compare_dt(it.get_text(), start_dt) for it in issused_time] == False).all():
                break

            del df
            next_btn = data.select_one(
                '#money_wrap > div > div.area_list.clearfix > div.col_l > div.list_page > li:nth-child(9) > a')
            next_link = next_btn['href']
            next_name = next_btn['title']


def recursive_HKstock(response, path):
    links = response.css('div.news_main_info h2 a::attr(href)').getall()
    # next_link = response.xpath('//*[@id="newidx_news_container"]/div[2]/a/@href').extract()
    # next_name = response.xpath('//*[@id="newidx_news_container"]/div[2]/a/text()').extract()
    get_all_urls_by_link(links,
                         path,
                         main_tile_style='#epContentLeft > h1',
                         dt_style='#epContentLeft > div.post_time_source',
                         content_style='#endText > p')


def recursive_house(response, path):
    '''
    recursive_house
    '''
    recursive(response,path)
    # links = response.css('div.item_top h2 a::attr(href)').getall()
    # next_link = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@href').extract()
    # next_link = next_link[0]
    # next_name = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@title').extract()
    # next_name = next_name[0]
    # get_all_urls_by_link(links, path)
    #
    # cnt = 1
    # while True:
    #     cnt += 1
    #     if next_name != '下一页':
    #         break
    #     data = get_next_html(next_link)
    #     if data is not None:
    #         links = data.select('div.item_top > h2 > a[href]')
    #         links = [l['href'] for l in links]
    #         get_all_urls_by_link(links, path)
    #         next_btn = data.select_one(
    #             '#money_wrap > div > div.area_list.clearfix > div.col_l > div.list_page > li:nth-child(9) > a')
    #         next_link = next_btn['href']
    #         next_name = next_btn['title']


def range_recursive_house(response, start_dt, end_dt, path):
    range_recursive(response, start_dt, end_dt, path)


def recursive_car(response, path):
    links = response.css('div.item_top h2 a::attr(href)').getall()
    next_link = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@href').extract()
    next_link = next_link[0]
    next_name = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@title').extract()
    next_name = next_name[0]
    get_all_urls_by_link(links, path)

    cnt = 1
    while True:
        cnt += 1
        if next_name != '下一页':
            break
        data = get_next_html(next_link)
        if data is not None:
            links = data.select('div.item_top > h2 > a[href]')
            links = [l['href'] for l in links]
            get_all_urls_by_link(links, path)
            next_btn = data.select_one(
                '#money_wrap > div > div.area_list.clearfix > div.col_l > div.list_page > li:nth-child(9) > a')
            next_link = next_btn['href']
            next_name = next_btn['title']


def range_recursive_car(response, start_dt, end_dt, path):
    range_recursive(response, start_dt, end_dt, path)


def recursive_fiancial(response, path):
    links = response.css('div.item_top h2 a::attr(href)').getall()
    next_link = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@href').extract()
    next_link = next_link[0]
    next_name = response.xpath('//*[@id="money_wrap"]/div/div[3]/div[1]/div[16]/li[8]/a/@title').extract()
    next_name = next_name[0]
    get_all_urls_by_link(links, path)

    cnt = 1
    while True:
        cnt += 1
        if next_name != '下一页':
            break
        data = get_next_html(next_link)
        if data is not None:
            links = data.select('div.item_top > h2 > a[href]')
            links = [l['href'] for l in links]
            get_all_urls_by_link(links, path)
            next_btn = data.select_one(
                '#money_wrap > div > div.area_list.clearfix > div.col_l > div.list_page > li:nth-child(9) > a')
            next_link = next_btn['href']
            next_name = next_btn['title']


def range_recursive_fiancial(response, start_dt, end_dt, path):
    range_recursive(response, start_dt, end_dt, path)
