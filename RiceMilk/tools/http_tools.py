import random

import requests
from bs4 import BeautifulSoup

from RiceMilk.config.init import user_agent_list
from requests.packages import urllib3
urllib3.disable_warnings()
import ssl
if hasattr(ssl, '_create_unverified_context'):
      ssl._create_default_https_context = ssl._create_unverified_context

def get_html(url,charset='gb18030'):
    '''
    获取给定链接的网页html
    :param url:
    :return:
    '''
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }
    resp = requests.get(url, headers=headers, verify=False)
    resp = BeautifulSoup(resp.content.decode(charset, 'ignore'), 'html.parser')
    # soup = normalize_response(res, is_scrapy=False)
    if resp is not None:
        return resp
    else:
        return None