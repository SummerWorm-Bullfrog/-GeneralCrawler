# -*- coding: utf-8 -*-
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class YqWorkerPipeline(object):
    def process_item(self, item, spider):
        return item
