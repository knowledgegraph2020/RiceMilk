import os
from RiceMilk.NetEaseFinance.parse.parse_detail import recursive_international, range_recursive, recursive_HKstock, recursive_house, \
    range_recursive_house, recursive_car, range_recursive_car, recursive_fiancial, range_recursive_fiancial
import shutil

def parse_international(response, start_dt, end_dt):
    # path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + end_dt + '/international'
    path = '/data/files/'+ end_dt + '/NetEaseFinance/international'
    if start_dt is None:
        # 递归获取当前时间以前的所有新闻
        recursive_international(response, path)
    elif start_dt is not None and end_dt is not None:
        # 只获取指定时间段的新闻
        range_recursive(response, start_dt, end_dt, path)


def parse_HKstock(response, start_dt, end_dt):
    # path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + end_dt + '/HKstock'
    path = '/data/files/' + end_dt + '/NetEaseFinance/HKstock'
    recursive_HKstock(response,path)


def parse_house(response, start_dt, end_dt):
    # path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + end_dt + '/house'
    path = '/data/files/' + end_dt + '/NetEaseFinance/house'

    if start_dt is None:
        recursive_house(response,path)
    elif start_dt is not None and end_dt is not None:
        range_recursive_house(response, start_dt, end_dt,path)


def parse_car(response, start_dt, end_dt):
    # path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + end_dt + '/car'
    path = '/data/files/' + end_dt + '/NetEaseFinance/car'

    if start_dt is None:
        recursive_car(response,path)
    elif start_dt is not None and end_dt is not None:
        range_recursive_car(response, start_dt, end_dt,path)


def parse_financial(response, start_dt, end_dt):
    # path = os.path.dirname(os.path.abspath(__file__)) + '/data/' + end_dt + '/fiancial'
    path = '/data/files/' + end_dt + '/NetEaseFinance/fiancial'

    if os.path.exists(path):
        shutil.rmtree(path)

    if start_dt is None:
        recursive_fiancial(response, path)
    elif start_dt is not None and end_dt is not None:
        range_recursive_fiancial(response, start_dt, end_dt, path)
