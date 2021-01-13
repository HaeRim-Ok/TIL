# Python Web Programming with Django (1)

## 기본 설정

1. django 프로젝트 생성  

- `django-admin startproject mydjango_product .`
- 현재 위치에 mydjango_product 이름으로 새 프로젝트를 생성
  
  - 자동으로 skeleton에 해당하는 디렉토리 및 파일을 만들어 준다. 
  
  

2. django 프로젝트 설정 변경

- settings.py의 LANGUAGE_CODE와 TIME_ZONE 변경

```python
LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
```

- settings.py에 정적 파일 경로를 추가

```
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
```



3. DB 생성과 Django 서버 시작

- 데이터베이스 생성 -> db.sqlite3 생성됨

  - `python manage.py runserver`

- django 서버 시작 

  - `python manage.py runserver 8080`

  - 8000  (default) 포트는 이미 사용하고 있으므로 8080번 포트 사용하여 서버 시작

  

4. superuser 계정 생성

- `python manage.py createsuperuser`
- username, password, email 지정
- http://localhost:8080/admin/으로 접속



## Product App 작성

### Model 클래스

> Django Model을 통해 DB로의 접근 가능
>
> <python 클래스>와 <database 테이블> 매핑

1. app 디렉토리 생성

- `python manage.py startapp product`



2. app을 프로젝트에 반영

- mydjango_product/settings.py 수정

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'product',
]
```



3. product app의 Post Model 만들기

```
from django.db import models
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=0, max_digits=10)
    stock_quan = models.DecimalField(decimal_places=0, max_digits=5)
    desc = models.TextField()
    posted_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.posted_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name
```



4. DB에 테이블 만들기

- 마이그레이션 파일 (작업 지시 파일) 생성
  
  - `python manage.py makemigrations product`
- 실제 데이터베이스에 model 반영
  - `python manage.py migrate product`
  - 에러 : No migrations to apply (이미 존재하는 테이블이라고 나온다.)
    
    - `python manage.py dbshell` -> `.tables` -> `drop table <테이블이름>;` 
    
    

5. 관리자 페이지에 Post 모델 등록

- http://localhost:8080/admin/으로 접속하여 확인하기

```
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```



6. Product App에 글 등록 후, admin page에 출력되는 내용 커스터마이징

- 번호, 이름, 수량, 금액도 함께 출력하며, 이름을 눌렀을 때 세부 내용을 확인할 수 있도록 

```
from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_disaply = ['id', 'name', 'stock_quan', 'price']
    list_display_links = ['name']

    def count_text(self, obj):
        return '{}글자'.format(len(obj.text))
    count_text.short_description = 'Post 글자수'
    
admin.site.register(Post)
```



### QuerySet

> 데이터베이스로부터 data를 읽고, 필터링 하거나, 정렬할 수 있다. 
>
> python shell에서 실행한다.

1. Interactive Console 실행 : `python manage.py shell`



2. 모든 객체 조회하기 

- `from product.models import Post`
- `Post.objects.all()` 



3. 객체 생성하기

- `from django.contrib.auth.models import User`
- `me = User.objects.get(username='admin')`
- `Post.objects.create(user=me, name='sample', desc='test', price='1000', stock_quan=8)`



4. 필터링하기

- 특정 사용자가 작성한 글을 찾고자 할 때

  - `Post.objects.filter(user=me)`

- 글의 이름에 sample이라는 글자가 들어간 글을 찾고자 할 때

  - `Post.objects.filter(name__contains='sample')`

- 현재 시간보다 과거에 작성(posted_date)한 글의 목록을 가져올 때

  - `from django.utils import timezone`

  - `Post.objects.filter(posted_date__lte=timezone.now())`

  - `posted_date__lte=timezone.now()` : 현재 시간보다 작성된 시간이 **같거나 작을 때**

    

5. 정렬하기

- 작성일(posted_date) 기준 오름차순으로 정렬
  - `Post.objects.order_by('posted_date')`
- 작성일(posted_date) 기준 내림차순으로 정렬
  - `Post.objects.order_by('-posted_date')`
- 쿼리셋 함께 연결(chaining)
  - `Post.objects.filter(posted_date__lte=timezone.now()).order_by('posted_date')`