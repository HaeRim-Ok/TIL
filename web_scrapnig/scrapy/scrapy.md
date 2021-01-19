# Scrapy 설치 및 사용법

> Scrapy: 웹 스크래핑할 때 많이 사용하는 파이썬 기반 라이브러리이며, 데이터 수집봇을 만들 수 있음
> 수많은 웹페이지로부터 원하는 형태로 데이터를 추출하여 저장하며, 빅데이터로 활용한다. 
> (정규 표현식의 한계를 보완함)

## 1. 설치 및 기본 사용법

[Anaconda Prompt]

1. scrapy 라이브러리 설치

```
$ pip install scrapy
```

2. scrapy 쉘로 진입

```
$ scrapy shell
```

3. 데이터를 수집할 웹 주소 입력
   - `fetch()` : 데이터를 선별하여 추출할 때
   - 정상적으로 값을 가지고 왔다면 200 출력

```
# Naver News Web
> fetch (‘https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001’)
```


4. 로컬 디렉토리에 저장된 페이지의 내용을 보여줌 (실제 네이버 뉴스 사이트 아님)

```
> view(response)
```

5. view(response)의 결과로 출력되는 웹 페이지의 소스코드 출력

```
> print(response.text)
```

<br/><br/>

## 2. 네이버뉴스 스크래핑 간단 실습

**가상환경 설정**

1. 가상환경 생성 및 활성화

```
$ conda create --name myscrapy
$ conda activate myscrapy
```

2. 가상환경 내 scrapy 설치

```
$ conda install scrapy
$ conda list 
$ scrapy shell
```

<br/>

**데이터 가져오기**

1. 웹 주소 입력

```
> fetch(‘https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230’) 
```

2. 로컬 디렉토리에 저장된 페이지의 내용 확인

```
> view(response)
```

3. 웹 페이지의 '뉴스 제목'만 추출
   - 개발자 도구를 통해 추출하고자 하는 데이터의 태그를 찾는다.
   - a 태그의 xpath를 복사하여 반복적인 패턴에 의해 가져올 수 있는 정보를 가져온다. 
     - 추출하고자 하는 데이터에 따라 태그의 속성, 태그 종류 등 상이할 수 있음

```
> response.xpath('//*[@id="main_content"]/div[2]/ul/li/dl/dt[2]/a/text()').extract()
```

4. 웹 페이지의 '신문사'만 추출
   - span class="writing"

```
> response.css('.writing::text').extract()
```

5. 웹 페이지의 '미리보기 내용'만 추출
   - span class="lede"

```
> response.css('.lede::text').extract()
```





