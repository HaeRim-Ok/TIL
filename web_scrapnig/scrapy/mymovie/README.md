# 네이버 영화 평점 스크래핑

1. 스크래핑 하고자 하는 사이트 : https://movie.naver.com/movie/point/af/list.nhn
   - '**영화 제목, 감상평, 별점, 글쓴이, 날짜**' -> 총 5개의 데이터를 스크래핑 할 예정 
![image](https://user-images.githubusercontent.com/77096463/105628452-5fbd5300-5e80-11eb-81f7-cb10ce242f42.png)
<br/>
<br/>

2. 가상환경 실행
```
$ conda activate mymovie
$ cd C:\Users\Lenovo\Work\scrapy
```
<br/>
<br/>

3. 프로젝트 생성
```
$ scrapy startproject mymovie
$ cd mymovie
```
<br/>
<br/>

4. 스파이더 생성
   - 이름 : moviebots
   - 사이트 이름 가져올땐 http 프로토콜 생략
```
$ scrapy genspider mymovie_bots "movie.naver.com/movie/point/af/list.nhn"
$ code .
```
<br/>
<br/>

5. mymovie_bots.py 파일 수정 
   - 감상평(descs) 은 '\n\t'와 같은 공백 데이터 제거 작업이 필요하기에 remove_space() 함수를 설정하여, 공백을 제거한 후 데이터만 추출하도록 코드를 작성한다.
```python
def remove_space(descs:list) -> list:
    result=[]
    for i in range(len(descs)) :
        if len(descs[i].strip()) > 0:
            result.append(descs[i].strip()) 
    return result

...

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
```
<br/>
<br/>

6. spider 실행하기
```
$ scrapy crawl mymovie_bots
```


<br/>
<br/>





