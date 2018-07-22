# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from Scrapy_Youtube_Channels.utils import extract_emails


class CleanItemPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'channel_crawler':
            return item
        item['description'] = item['description'].strip()
        item['emails'] = extract_emails(item['description'])
        return item
