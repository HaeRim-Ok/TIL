import scrapy
from myscraper.items import MyscraperItem
from scrapy.http import Request

URL = 'http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230&page=%s'
start_page = 1
#http://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230&page=1

class MybotsSpider(scrapy.Spider):
    name = 'mybots'
    allowed_domains = ['naver.com']
    start_urls = [URL % start_page]

    def start_requests(self):
        for i in range(2):  # 0,1 (~page.2)
            yield Request(url= URL % (i + start_page), callback=self.parse)    # url 시작 -> parse 함수와 연동

    def parse(self, response):
        # 모두 list 형태로 반환
        titles = response.xpath('//*[@id="main_content"]/div[2]/ul/li/dl/dt[2]/a/text()').extract()
        writers = response.css('.writing::text').extract()
        previews = response.css('.lede::text').extract()

        # zip(titles, writers, previews)
        items = []
        # items에 XPATH, CSS를 통해 추출한 데이터를 저장
        for idx in range(len(titles)):
            item= MyscraperItem()
            item['title'] = titles[idx]
            item['writer'] = writers[idx]
            item['preview'] = previews[idx]

            items.append(item)

        return items

