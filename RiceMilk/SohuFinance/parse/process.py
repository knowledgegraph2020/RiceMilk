import RiceMilk.SohuFinance.parse.config as cfg
import scrapy
import time
import os, re
import logging
from logging.handlers import TimedRotatingFileHandler

# def make_save_dir():
#     today_ = time.strftime("%Y-%m-%d")
#     sohu_save_dir = os.path.join(cfg.save_dir, today_, 'SohuFinance')
#     if not os.path.exists(sohu_save_dir):
#         os.makedirs(sohu_save_dir)
#     return sohu_save_dir

def make_save_dir(news_type):
    today_ = time.strftime("%Y-%m-%d")
    sohu_save_dir = os.path.join(cfg.save_dir, today_, 'SohuFinance', news_type)
    if not os.path.exists(sohu_save_dir):
        os.makedirs(sohu_save_dir)
    return sohu_save_dir

def get_logger():
    logger = logging.getLogger("logger")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler(filename=cfg.log_path,
                                           when="D",
                                           interval=1,
                                           backupCount=90)
        handler.suffix = "%Y-%m-%d.log"
        handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(handler)
    return logger

