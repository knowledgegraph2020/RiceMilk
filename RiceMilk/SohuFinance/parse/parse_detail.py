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