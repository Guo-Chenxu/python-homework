# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 新房
class NewHouseItem(scrapy.Item):
    name = scrapy.Field()  # 楼盘名称
    type = scrapy.Field()  # 类型
    location = scrapy.Field()  # 地点
    room_type = scrapy.Field()  # 房型
    area = scrapy.Field()  # 面积
    unit_price = scrapy.Field()  # 单价
    total_price = scrapy.Field()  # 总价


# 二手房
class OldHouseItem(scrapy.Item):
    community = scrapy.Field()  # 小区名称
    location = scrapy.Field()  # 地点
    room_type = scrapy.Field()  # 房型信息
    unit_price = scrapy.Field()  # 单价
    total_price = scrapy.Field()  # 总价
