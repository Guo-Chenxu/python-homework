import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse

from lianjia.items import *


class NewHouseSpider(scrapy.Spider):
    """
    爬取新房数据
    """
    name = "new_house"
    allowed_domains = ["bj.fang.lianjia.com"]
    start_urls = ['https://bj.fang.lianjia.com/loupan/']
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.NewHouseItemPipeline": 300, }
    }

    def start_requests(self):
        for page in range(3, 3 + 5):
            yield Request(url=f'https://bj.fang.lianjia.com/loupan/pg{page}/', callback=self.parse, dont_filter=True)

    def parse(self, response: HtmlResponse, **kwargs):
        list_items = response.xpath(
            '/html/body/div[@class="resblock-list-container clearfix"]/ul[@class="resblock-list-wrapper"]/li[@class="resblock-list post_ulog_exposure_scroll has-results"]/div[@class="resblock-desc-wrapper"]')
        for item in list_items:
            new_house_item = NewHouseItem()
            new_house_item['name'] = item.xpath(
                './div[@class="resblock-name"]/a[@class="name "]/text()').extract_first()
            new_house_item['type'] = item.xpath(
                './div[@class="resblock-name"]/span[@class="resblock-type"]/text()').extract_first()
            new_house_item['location'] = "".join(item.xpath('./div[@class="resblock-location"]/*/text()').extract())
            new_house_item['room_type'] = "".join(item.xpath('./a[@class="resblock-room"]/*/text()').extract())
            new_house_item['area'] = item.xpath('./div[@class="resblock-area"]/span/text()').extract_first()
            new_house_item['unit_price'] = "".join(
                item.xpath('./div[@class="resblock-price"]/div[@class="main-price"]/*/text()').extract()) \
                .replace(u'\xa0', ' ')
            new_house_item['total_price'] = item.xpath('./div[@class="resblock-price"]/div[@class="second"]/text()') \
                .extract_first()
            yield new_house_item


class OldHouseSpider(scrapy.Spider):
    """
    爬取二手房数据, 点进链接爬取
    """
    name = "old_house"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ['https://bj.lianjia.com/ershoufang/']
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.OldHouseItemPipeline": 400, }
    }

    def start_requests(self):
        for page in range(3, 3 + 5):
            yield Request(url=f'https://bj.lianjia.com/ershoufang/pg{page}/', callback=self.parse, dont_filter=True)

    """
    爬取地点详细信息
    """

    def location_info(self, response: HtmlResponse, **kwargs):
        location_item = response.xpath(
            '/html/body/div[@class="overview"]/div[@class="content"]/div[@class="aroundInfo"]')
        old_house_item = kwargs['item']
        old_house_item['community'] = location_item.xpath(
            './div[@class="communityName"]/a[@class="info "]/text()').extract_first()
        old_house_item['location'] = "".join(
            location_item.xpath('./div[@class="areaName"]/span[@class="info"]//text()').extract()) \
            .replace(u'\xa0', ' ')
        yield old_house_item

    def parse(self, response: HtmlResponse, **kwargs):
        list_items = response \
            .xpath('/html/body/div[@class="content "]/div[@class="leftContent"]/ul/li')
        for item in list_items:
            detail_info_url = item.xpath('./a[@class="noresultRecommend img LOGCLICKDATA"]/@href').extract_first()
            item = item.xpath('./div[@class="info clear"]')
            old_house_item = OldHouseItem()
            old_house_item['room_type'] = item.xpath(
                './div[@class="address"]/div/text()').extract_first()
            old_house_item['total_price'] = item.xpath(
                './div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()').extract_first()
            old_house_item['unit_price'] = "".join(
                item.xpath('./div[@class="priceInfo"]/div[@class="totalPrice totalPrice2"]/*/text()').extract())
            yield Request(url=detail_info_url, dont_filter=True, callback=self.location_info,
                          cb_kwargs={'item': old_house_item})
