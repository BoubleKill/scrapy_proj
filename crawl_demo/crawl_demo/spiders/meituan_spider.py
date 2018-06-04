# usr/bin/python3
# _*_ coding:utf-8 _*_
"""
    @version:  python 3.6.5
    @FileName: meituan_spider.py
    @Author:   Songgy
    @Time：    2018-05-28 09:33
    @Email:    songganyuan@d-bigdata.com
    @Description: 
"""
import hashlib
import scrapy
from ..items import MeituanItem


class MeituanSpider(scrapy.Spider):

        name = "meituan_top100"
        start_urls = ["https://maoyan.com/board/4"]
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }

        def parse(self, response):
            self.log('A response from %s just arrived!' % response.url)
            for p in range(0, 100, 10):
                parm = "?offset=%d" % p
                yield scrapy.Request(url=response.url+parm, callback=self.parse_detail)

        def parse_detail(self, response):
            mains = response.xpath("//div[@class='board-item-main']/div")
            for m in mains:
                item = MeituanItem()
                item["movie_title"] = m.xpath("div[1]/p[1]/a[@title]/text()").extract_first().strip()
                item["movie_stars"] = m.xpath("div[1]/p[2][@class='star']/text()").extract_first().strip()
                item["movie_time"] = m.xpath("div[1]/p[3][@class='releasetime']/text()").extract_first().split("：")[1].strip()
                item["movie_score"] = m.xpath("div[2]/p/i[1]/text()").extract_first().strip() + \
                                      m.xpath("div[2]/p/i[2]/text()").extract_first().strip()
                item["movie_detail_url"] = "https://maoyan.com"+m.xpath("div[1]/p[1]/a").xpath("@href").extract_first()
                item["_id"] = hashlib.md5(item["movie_title"].encode()+item["movie_time"].encode()).hexdigest()
                yield item

