import scrapy
from mymovie.items import MymovieItem

# list타입의 descs가 param & list 형태로 반환
# descs : 40개의 데이터 (공백포함) -> 10개의 데이터 (공백제거) 
def remove_space(descs:list) -> list:
    result=[]
    for i in range(len(descs)) :
        if len(descs[i].strip()) > 0:
            result.append(descs[i].strip()) 
    return result

class MymovieBotsSpider(scrapy.Spider):
    name = 'mymovie_bots'
    allowed_domains = ['naver.com']
    start_urls = ['http://movie.naver.com/movie/point/af/list.nhn']

    def parse(self, response):
        titles = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[2]/a[1]/text()').extract()
        stars = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[2]/div/em/text()').extract()
        descs = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[2]/text()').extract()
        converted_descs = remove_space(descs)

        writers = response.css('.author::text').extract()
        dates = response.xpath('//*[@id="old_content"]/table/tbody/tr/td[3]/text()').extract()

        for row in zip (titles, stars, converted_descs, writers, dates) :
            item = MymovieItem()
            item['title'] = row[0]
            item['star'] = row[1]
            item['desc'] = row[2]
            item['writer'] = row[3]
            item['date'] = row[4]

            yield item  # return과 기능은 동일하나, generator도 포함

        # items = []
        # for idx in range(len(titles)):
        #     item = MymovieItem()
        #     item['title'] = titles[idx]
        #     item['star'] = stars[idx]
        #     item['desc'] = converted_descs[idx]
        #     item['writer'] = writers[idx]
        #     item['date'] = dates[idx]

        #     items.append(item)
        # return items