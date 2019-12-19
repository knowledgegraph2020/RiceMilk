#!/usr/bin/env bash

pip3 install pandas
pip3 install bs4

# get current datetime
yesterday=`date -d last-day +%Y-%m-%d`
echo $yesterday

echo 'execute NetEaseFinance start......'
echo 'into RiceMilk root path.......'
cd /data/RiceMilk
scrapy crawl NetEaseFinance -a start=$yesterday -a end=$yesterday
echo 'execute NetEaseFinance end......'
