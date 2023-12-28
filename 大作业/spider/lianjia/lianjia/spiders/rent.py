import scrapy

from scrapy import Request, Selector
from scrapy.http import HtmlResponse

from 大作业.spider.lianjia.lianjia.items import RentHouseItem


class Crawler:
    def process_url(self, response: HtmlResponse, **kwargs):
        """
        确定爬取的页数, 进一步处理url
        """
        # 判断如果查询记录为0条, 则直接返回
        total_nums = response.xpath(
            '/html/body/div[@class="wrapper"]/div[1]/div[@id="content"]/div[@class="content__article"]'
            '/p[@class="content__title"]/span[1]/text()').extract_first()
        if total_nums is not None and int(total_nums) == 0:
            yield

        # 获取将要爬取的页数
        total_page = response.xpath(
            '/html/body/div[@class="wrapper"]/div[1]/div[@id="content"]/div[@class="content__article"]'
            '/div[@class="content__pg"]/@data-totalpage').extract_first()
        total_page = int(total_page) if total_page is not None else 100
        # if total_nums is None:
        #     print("url: ", response.url, "  total_nums: ", total_nums)
        # if total_page is None:
        #     print("url: ", response.url, "  total_nums: ", total_nums, "  total_page: ", total_page)
        # total_page = 100

        url_parts = response.url.split('brp')
        for page in range(1, total_page + 1, 1):
            url = url_parts[0] + 'pg' + str(page) + 'brp' + url_parts[1]
            yield Request(url=url, callback=self.get_info, dont_filter=True,
                          cb_kwargs={'city': kwargs['city'],
                                     'low_price': kwargs['low_price'], 'high_price': kwargs['high_price'],
                                     'prefix': kwargs['prefix']})

    def get_info(self, response: HtmlResponse, **kwargs):
        """
        真正的爬虫函数
        """
        # 再次判断是否是0条记录
        total_nums = response.xpath(
            '/html/body/div[@class="wrapper"]/div[1]/div[@id="content"]/div[@class="content__article"]'
            '/p[@class="content__title"]/span[1]/text()').extract_first()
        if total_nums is not None and int(total_nums) == 0:
            yield

        low_price, high_price = int(kwargs['low_price']), int(kwargs['high_price'])
        prefix = str(kwargs['prefix'])

        list_items = response.xpath(
            '/html/body/div[@class="wrapper"]/div[1]/div[@id="content"]/div[@class="content__article"]'
            '/div[1]/div[@class="content__list--item"]')
        for list_item in list_items:
            rent_house_item = RentHouseItem()
            rent_house_item['city'] = kwargs['city']
            rent_house_item['name'] = list_item.xpath('./a[@class="content__list--item--aside"]/@title').extract_first()
            rent_house_item['url'] = prefix + list_item.xpath('./a[1]/@href').extract_first().strip()

            list_item = list_item.xpath('./div[@class="content__list--item--main"]')

            # 记录最低价格, 在当前价格范围内的进行存储, 避免数据重复
            price = list_item.xpath('./span[@class="content__list--item-price"]/em/text()').extract_first() \
                .split('-')[0]
            if not (low_price <= int(price) < high_price):
                continue
            rent_house_item['price'] = price

            # 获取面积, 户型, 朝向, 位置信息
            desc = list_item.xpath('string(./p[@class="content__list--item--des"])').extract_first().split()
            for d in desc:
                if d.count('㎡') != 0:
                    rent_house_item['area'] = d[:-1] if d.count('-') == 0 else d.split('-')[0]
                elif d.count('室') != 0 or d.count('房') != 0:
                    rent_house_item['room_type'] = d[:(
                        int(d.index('室')) if d.count('室') != 0 else int(d.index('房')))]
                elif d.count('-') == 2:
                    region = d.split('-')
                    rent_house_item['district'] = region[0]
                    rent_house_item['county'] = region[1]
                    rent_house_item['town'] = region[2]
                elif d.count('东') != 0 or d.count('南') != 0 or d.count('西') != 0 or d.count('北') != 0:
                    rent_house_item['orientation'] = "".join(d.strip().replace(" ", "").split("/"))

            yield rent_house_item


class BeiJingRentSpider(scrapy.Spider):
    """
    北京租房数据
    """
    name = "beijing_rent"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://bj.lianjia.com/zufang/"]
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.BeijingRentHouseItemPipeline": 200, }
    }

    def start_requests(self):
        crawler = Crawler()
        districts = ["dongcheng", "xicheng", "chaoyang", "haidian", "fengtai", "shijingshan", "tongzhou", "changping",
                     "daxing", "yizhuangkaifaqu", "shunyi", "fangshan", "mentougou", "pinggu", "huairou", "miyun",
                     "yanqing"]
        # districts = ["dongcheng"]
        step_price = 100
        for district in districts:
            # 价格0到三万
            for price in range(0, 3_0000, step_price):
                # print("url: ", f'https://bj.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/')
                yield Request(url=f'https://bj.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/',
                              callback=crawler.process_url, dont_filter=True,
                              cb_kwargs={'city': "北京", 'low_price': price, 'high_price': price + step_price,
                                         'prefix': "https://bj.lianjia.com"})
            # 三万以上
            # print("url: ", f'https://bj.lianjia.com/zufang/{district}/brp30000/')
            yield Request(url=f'https://bj.lianjia.com/zufang/{district}/brp30000/',
                          callback=crawler.process_url, dont_filter=True,
                          cb_kwargs={'city': "北京", 'low_price': 30000, 'high_price': 1000000,
                                     'prefix': "https://bj.lianjia.com"})


class ShangHaiRentSpider(scrapy.Spider):
    """
    上海租房数据
    """
    name = "shanghai_rent"
    allowed_domains = ["sh.lianjia.com"]
    start_urls = ["https://sh.lianjia.com/zufang/"]
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.ShangHaiRentHouseItemPipeline": 400, }
    }

    def start_requests(self):
        crawler = Crawler()
        districts = ["jingan", "xuhui", "huangpu", "changning", "putuo", "pudong", "baoshan", "hongkou", "yangpu",
                     "minhang", "jinshan", "jiading", "chongming", "fengxian", "songjiang", "qingpu"]
        # districts = ["huangpu"]
        step_price = 100
        for district in districts:
            # 价格0到三万
            for price in range(0, 3_0000, step_price):
                # print("url: ", f'https://sh.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/')
                yield Request(url=f'https://sh.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/',
                              callback=crawler.process_url, dont_filter=True,
                              cb_kwargs={'city': "上海", 'low_price': price, 'high_price': price + step_price,
                                         'prefix': "https://sh.lianjia.com"})
            # 三万以上
            # print("url: ", f'https://sh.lianjia.com/zufang/{district}/brp30000/')
            yield Request(url=f'https://sh.lianjia.com/zufang/{district}/brp30000/',
                          callback=crawler.process_url, dont_filter=True,
                          cb_kwargs={'city': "上海", 'low_price': 30000, 'high_price': 1000000,
                                     'prefix': "https://sh.lianjia.com"})


class GuangZhouRentSpider(scrapy.Spider):
    """
    广州租房数据
    """
    name = "guangzhou_rent"
    allowed_domains = ["gz.lianjia.com"]
    start_urls = ["https://gz.lianjia.com/zufang/"]
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.GuangZhouRentHouseItemPipeline": 600, }
    }

    def start_requests(self):
        crawler = Crawler()
        districts = ["tianhe", "yuexiu", "liwan", "haizhu", "panyu", "baiyun", "huangpugz", "conghua", "zengcheng",
                     "huadou", "nansha"]
        # districts = ["conghua"]
        step_price = 100
        for district in districts:
            # 价格0到三万
            for price in range(0, 3_0000, step_price):
                # print("url: ", f'https://gz.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/')
                yield Request(url=f'https://gz.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/',
                              callback=crawler.process_url, dont_filter=True,
                              cb_kwargs={'city': "广州", 'low_price': price, 'high_price': price + step_price,
                                         'prefix': "https://gz.lianjia.com"})
            # 三万以上
            # print("url: ", f'https://gz.lianjia.com/zufang/{district}/brp30000/')
            yield Request(url=f'https://gz.lianjia.com/zufang/{district}/brp30000/',
                          callback=crawler.process_url, dont_filter=True,
                          cb_kwargs={'city': "广州", 'low_price': 30000, 'high_price': 1000000,
                                     'prefix': "https://gz.lianjia.com"})


class ShenZhenRentSpider(scrapy.Spider):
    """
    深圳租房数据
    """
    name = "shenzhen_rent"
    allowed_domains = ["sz.lianjia.com"]
    start_urls = ["https://sz.lianjia.com/zufang/"]
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.ShenZhenRentHouseItemPipeline": 800, }
    }

    def start_requests(self):
        crawler = Crawler()
        districts = ["luohuqu", "futianqu", "nanshanqu", "yantianqu", "baoanqu", "longgangqu", "longhuaqu",
                     "guangmingqu", "pingshanqu", "dapengxinqu"]
        # districts = ["dapengxinqu"]
        step_price = 100
        for district in districts:
            # 价格0到三万
            for price in range(0, 3_0000, step_price):
                # print("url: ", f'https://sz.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/')
                yield Request(url=f'https://sz.lianjia.com/zufang/{district}/brp{price}erp{price + step_price}/',
                              callback=crawler.process_url, dont_filter=True,
                              cb_kwargs={'city': "深圳", 'low_price': price, 'high_price': price + step_price,
                                         'prefix': "https://sz.lianjia.com"})
            # 三万以上
            # print("url: ", f'https://sz.lianjia.com/zufang/{district}/brp30000/')
            yield Request(url=f'https://sz.lianjia.com/zufang/{district}/brp30000/',
                          callback=crawler.process_url, dont_filter=True,
                          cb_kwargs={'city': "深圳", 'low_price': 30000, 'high_price': 1000000,
                                     'prefix': "https://sz.lianjia.com"})


class ZhuMaDianRentSpider(scrapy.Spider):
    """
    驻马店租房数据
    """
    name = "zhumadian_rent"
    allowed_domains = ["zmd.lianjia.com"]
    start_urls = ["https://zmd.lianjia.com/zufang/"]
    custom_settings = {
        'ITEM_PIPELINES': {"lianjia.pipelines.ZhuMaDianRentHouseItemPipeline": 10000, }
    }

    def start_requests(self):
        crawler = Crawler()
        step_price = 1000
        # 价格0到四千
        for price in range(0, 4000, step_price):
            # print("url: ", f'https://zmd.lianjia.com/zufang/brp{price}erp{price + step_price}/')
            yield Request(url=f'https://zmd.lianjia.com/zufang/brp{price}erp{price + step_price}/',
                          callback=crawler.process_url, dont_filter=True,
                          cb_kwargs={'city': "驻马店", 'low_price': price, 'high_price': price + step_price,
                                     'prefix': "https://zmd.lianjia.com"})
        # 四千以上
        # print("url: ", f'https://zmd.lianjia.com/zufang/brp4000/')
        yield Request(url=f'https://zmd.lianjia.com/zufang/brp4000/',
                      callback=crawler.process_url, dont_filter=True,
                      cb_kwargs={'city': "驻马店", 'low_price': 4000, 'high_price': 1000000,
                                 'prefix': "https://zmd.lianjia.com"})
