# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from 大作业.spider.lianjia.lianjia.items import RentHouseItem


# useful for handling different item types with a single interface


def write_to_csv(csv_writer: any, item: RentHouseItem):
    item = RentHouseItem(item)
    csv_writer.writerow(
        [item.get('city'), item.get('name'), item.get('district'), item.get('county'), item.get('town'),
         item.get('price'), item.get('area'), item.get('orientation'), item.get('room_type'), item.get("url")])
    return item


class BeijingRentHouseItemPipeline:
    def __init__(self):
        self.file = None
        self.csv_writer = None

    def open_spider(self, spider):
        try:
            self.file = open('bj_rent_house.csv', 'w', encoding='utf-8', newline="")
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(
                ["city", "name", "district", "county", "town", "price", "area", "orientation", "room_type", "url"])
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        return write_to_csv(self.csv_writer, item)

    def close_spider(self, spider):
        self.file.close()


class ShangHaiRentHouseItemPipeline:

    def __init__(self):
        self.file = None
        self.csv_writer = None

    def open_spider(self, spider):
        try:
            self.file = open('sh_rent_house.csv', 'w', encoding='utf-8', newline="")
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(
                ["city", "name", "district", "county", "town", "price", "area", "orientation", "room_type", "url"])
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        return write_to_csv(self.csv_writer, item)

    def close_spider(self, spider):
        self.file.close()


class GuangZhouRentHouseItemPipeline:

    def __init__(self):
        self.file = None
        self.csv_writer = None

    def open_spider(self, spider):
        try:
            self.file = open('gz_rent_house.csv', 'w', encoding='utf-8', newline="")
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(
                ["city", "name", "district", "county", "town", "price", "area", "orientation", "room_type", "url"])
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        return write_to_csv(self.csv_writer, item)

    def close_spider(self, spider):
        self.file.close()


class ShenZhenRentHouseItemPipeline:

    def __init__(self):
        self.file = None
        self.csv_writer = None

    def open_spider(self, spider):
        try:
            self.file = open('sz_rent_house.csv', 'w', encoding='utf-8', newline="")
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(
                ["city", "name", "district", "county", "town", "price", "area", "orientation", "room_type", "url"])
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        return write_to_csv(self.csv_writer, item)

    def close_spider(self, spider):
        self.file.close()


class ZhuMaDianRentHouseItemPipeline:

    def __init__(self):
        self.file = None
        self.csv_writer = None

    def open_spider(self, spider):
        try:
            self.file = open('zmd_rent_house.csv', 'w', encoding='utf-8', newline="")
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(
                ["city", "name", "district", "county", "town", "price", "area", "orientation", "room_type", "url"])
        except Exception as e:
            print(e)

    def process_item(self, item, spider):
        return write_to_csv(self.csv_writer, item)

    def close_spider(self, spider):
        self.file.close()
