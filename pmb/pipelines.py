# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests

class PmbPipeline(object):
    API_HOST = 'http://localhost:5000'
    def process_item(self, item, spider):
        if item['meta']['type'] == 'sedinte':
            requests.post(self.API_HOST + '/spider/sedinte', json=item)

        elif item['meta']['type'] == 'dezbateri':
            requests.post(self.API_HOST + '/spider/dezbateri', json=item['data'])

        return item
