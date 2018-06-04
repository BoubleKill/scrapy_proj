# usr/bin/python3
# _*_ coding:utf-8 _*_
"""
    @version:  python 3.6.5
    @FileName: shantou_credit_spider.py
    @Author:   Songgy
    @Time：    2018-05-28 09:33
    @Email:    songganyuan@d-bigdata.com
    @Description: 
"""
import json

import scrapy
from ..items import NewsCrawlItem


class ShantouNewsSpider(scrapy.Spider):

        name = "shantou_credit"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }

        def start_requests(self):
            url = "http://credit.st.gov.cn/shantoucredit_pubserver/front/article/list"
            size = 500
            parms = [
                {"page": 0, "size": size, "module": "信用动态", "column": "国内动态"},
                {"page": 0, "size": size, "module": "信用动态", "column": "省内动态"},
                {"page": 0, "size": size, "module": "信用动态", "column": "汕头动态"},
                {"page": 0, "size": size, "module": "政策法规", "column": "国内政策"},
                {"page": 0, "size": size, "module": "政策法规", "column": "省内政策"},
                {"page": 0, "size": size, "module": "政策法规", "column": "汕头政策"},
                {"page": 0, "size": size, "module": "典型案例", "column": "信用典型案例"},
            ]
            # Request 是Scrapy发送POST请求的方法，但是其body参数只接受str or bytes类型
            for parm_data in parms:
                yield scrapy.Request(
                    url=url,
                    method="POST",
                    headers=self.headers,
                    meta=parm_data,
                    body=json.dumps(parm_data),
                    callback=self.parse_json
                )

        def parse(self, response):
            self.log('A response from %s just arrived!' % response.url)
            pass

        def parse_json(self, response):
            if response.status != 200:
                self.log('Something wrong for a response: url=%s, data=%s' % (response.url, json.dumps(response.meta)))
            ret = json.loads(response.text).get("data")
            total = ret.get("count")
            dataList = ret.get("detail") if ret.get("detail") else 0
            self.log("total=%d" % total)
            for data in dataList:
                item = NewsCrawlItem()
                for k in ["module", "column", "source", "title", "content", "ori_content"]:
                    item[k] = data.get(k)
                item["news_date"] = data.get("publishtime")
                item["_id"] = data.get("id")
                yield item




