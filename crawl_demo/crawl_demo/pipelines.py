# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql


class CrawlDemoPipeline(object):
    def process_item(self, item, spider):
        return item


class PyMySQLPipeline(object):
    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_pwd, mysql_db, mysql_table):
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_pwd = mysql_pwd
        self.mysql_db = mysql_db
        self.mysql_table = mysql_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get("MYSQL_HOST"),
            mysql_port=crawler.settings.get("MYSQL_PORT"),
            mysql_user=crawler.settings.get("MYSQL_USER"),
            mysql_pwd=crawler.settings.get("MYSQL_PWD"),
            mysql_db=crawler.settings.get("MYSQL_DB"),
            mysql_table=crawler.settings.get("TABLE_ITEM_INFO")
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_pwd,
            db=self.mysql_db,
            charset="utf8"
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        name = item.__class__.__name__
        table = self.mysql_table.get(name).get("table")
        data = dict(item)
        keys = ", ".join(["`%s`" % k for k in data.keys()])
        vals = ", ".join(["%s"]*len(data))
        sql = "INSERT INTO `%s` (%s) VALUES (%s);" % (table, keys, vals)
        self.cursor.execute(sql, tuple(data.values()))
        self.conn.commit()
        return item

    def close_client(self, spider):
        self.conn.close()


class MongoPipeline(object):
    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get("MONGO_DB"),
            mongo_host=crawler.settings.get("MONGO_HOST"),
            mongo_port=crawler.settings.get("MONGO_PORT")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_client(self, spider):
        self.client.close()

	