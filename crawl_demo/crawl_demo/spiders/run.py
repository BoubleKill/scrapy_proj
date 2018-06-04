# usr/bin/python3
# -*- coding:utf-8 -*-
"""
    @version:  python 3.6.5
    @FileName: run.py
    @Author:   Songgy
    @Time：    2018-05-30 09:53
    @Email:    songganyuan@d-bigdata.com
    @Description: 
"""

from scrapy import cmdline

cmdline.execute("scrapy crawl shantou_credit".split())
# cmdline.execute("scrapy crawl meituan_top100".split())







