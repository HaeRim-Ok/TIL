# Selenium 설치 및 사용법

> 웹 어플리케이션 테스트 프레임워크
>
> 웹 사이트에서 버튼 클릭, 이벤트 처리 가능
>
> Javascript 실행 가능
>
> 웹 브라우저 실행을 대신하기 위해 web driver 설치





```
# 가상환경 진입
$ conda activate [환경이름]

# 가상환경 빠져나오기
$ conda deactivate

# 가상환경 제거
$ conda remove --name [환경이름] --all

# 가상환경 목록 확인
$ conda info --envs
```





## 1. Selenium 설치

1. https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/ 접속
   
   - windows version 설치
   
2. selenium 설치  (powershell / cmd) 

```
$ pip install selenium
```


3. 가상환경 생성  

```
$ conda create --name [가상환경]
```

4. 가상환경 진입  
   - Anaconda Prompt가 에러 발생할 확률 낮음

```
$ conda activate [가상환경]
```

5. 가상환경 내 라이브러리 설치  (둘 중 하나)

```
$ conda install selenium
$ pip install selenium
```

6. 경로 변경  

```
$ cd C:\Users\Lenovo\Work\git
```

7. 새 파일 생성 

```
$ code selenium_test.py
```







## 2. selenium_test.py

```python
from selenium import webdriver

# windows -> path에 \ 하나씩 더 추가
path = "C:\\Users\\Lenovo\\Desktop\\cloud-service\\webdriver\\chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://www.naver.com")
print(driver.title) # 탭의 이름 
```




