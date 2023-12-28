# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from lianjia.items import *


class NewHouseItemPipeline:
    def __init__(self):
        self.new_house_file = None

    def open_spider(self, spider):
        try:
            self.new_house_file = open('new_house.json', 'w', encoding='utf-8')
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
        self.new_house_file.write(json_str)
        return item

    def close_spider(self, spider):
        self.new_house_file.close()


class OldHouseItemPipeline:
    def __init__(self):
        self.old_house_file = None

    def open_spider(self, spider):
        try:
            self.old_house_file = open('old_house.json', 'w', encoding='utf-8')
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
        self.old_house_file.write(json_str)
        return item

    def close_spider(self, spider):
        self.old_house_file.close()
