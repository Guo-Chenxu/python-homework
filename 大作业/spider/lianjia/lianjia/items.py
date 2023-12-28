# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RentHouseItem(scrapy.Item):
    city = scrapy.Field()  # 市, 如 北京
    name = scrapy.Field()  # 房子名称, 如 整租·忠实里 1室1厅 东
    district = scrapy.Field()  # 行政区, 如 海淀
    county = scrapy.Field()  # 县级板块, 如 四季青
    town = scrapy.Field()  # 最小一级, 如 五福玲珑居北区
    orientation = scrapy.Field()  # 房屋朝向
    room_type = scrapy.Field()  # 房屋类型, 如 1 表示 1居室
    price = scrapy.Field()  # 价格, 单位 元/月
    area = scrapy.Field()  # 面积, 单位 平方米
    url = scrapy.Field()  # 房子信息链接
