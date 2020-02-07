import RiceMilk.SohuFinance.parse.config as cfg

import time
import os

def make_save_dir():
    today_ = time.strftime("%Y-%m-%d")
    sohu_save_dir = os.path.join(cfg.save_dir, today_, 'SohuFinance')
    if not os.path.exists(sohu_save_dir):
        os.makedirs(sohu_save_dir)
    return sohu_save_dir

