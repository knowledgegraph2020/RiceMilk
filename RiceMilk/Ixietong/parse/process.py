#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:05:07 2020

@author: cengqiqi
"""
import time
import os
import RiceMilk.Ixietong.parse.config as cfg


def make_save_dir():
    today_ = time.strftime("%Y-%m-%d")
    cfi_save_dir = os.path.join(cfg.save_dir, today_, 'ixietong', '爱协同')
    if not os.path.exists(cfi_save_dir):
        os.makedirs(cfi_save_dir)
    return cfi_save_dir