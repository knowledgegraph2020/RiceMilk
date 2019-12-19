from scrapy.cmdline import execute

import sys
import os
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(__file__))

if __name__ == '__main__':
    # 传入的参数，网站名称
    flag = sys.argv[1]
    start_dt = sys.argv[2]
    end_dt = sys.argv[3]
    if start_dt is None:
        raise Exception("start is None")
        sys.exit(1)
    if end_dt is None:
        raise Exception("end is None")
        sys.exit(1)
    # if start_dt > end_dt:
    #     raise Exception("start_dt is not allowed greater than end_dt")
    #     sys.exit(1)
    if flag is None:
        raise Exception("flag is None")
    else:
        # 按照网站的name进行执行任务
        logger.info("scrapy crawl {0} -a start={1} -a end={2}".format(flag, start_dt, end_dt).split())
        execute("scrapy crawl {0} -a start={1} -a end={2}".format(flag, start_dt, end_dt).split())
