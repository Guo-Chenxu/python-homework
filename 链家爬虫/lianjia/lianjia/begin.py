from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    configure_logging()
    process = CrawlerProcess(get_project_settings())
    process.crawl("new_house")
    process.crawl("old_house")
    process.start()
