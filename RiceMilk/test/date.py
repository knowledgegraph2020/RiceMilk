import random
import os
from RiceMilk.config.init import user_agent_list


if __name__ == '__main__':
    # dt = time.strptime('2017-11-24 17:30:00','%Y-%m-%d %H:%M:%S')
    # dt = time.strftime('%Y-%m-%d',dt)
    # nag = int(dt) - int('2019-12-08')
    # dt2 = time.strptime('2017-11-25 17:30:00','%Y-%m-%d %H:%M:%S')

    # 随机选择模拟浏览器
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }

    dt = ['2019-12-01','2019-12-02','2019-12-03','2019-12-04','2019-12-05','2019-12-06','2019-12-07','2019-12-08']
    links = ['https://money.163.com/19/1210/08/F016QGEP00259F18.html',
             'https://money.163.com/19/1210/08/F0162I2200259DLP.html',
             'https://money.163.com/19/1210/07/F015TH1000258105.html',
             'https://money.163.com/19/1210/07/F015NOL600258105.html',
             'https://money.163.com/19/1210/07/F015L5JR00258105.html',
             'https://money.163.com/19/1210/07/F015MKP1002580S6.html',
             'https://money.163.com/19/1210/07/F01485CP00259DLP.html',
             'https://money.163.com/19/1210/00/F00BST1G002580S6.html']

    # df = pd.DataFrame()
    # df['dt'] = dt
    # df['link'] = links
    #
    # print(df.__len__())
    # result = df[(df['dt']>'2019-12-03') & (df['dt'] < '2019-12-07')]
    # print(result.__len__())
    # result = result['link'].to_list()
    # print(result)

    # if not os.path.exists('./data/first'):
    #     os.makedirs('./data/first')
    p = os.path.dirname(os.path.abspath(__file__))
    print(p)