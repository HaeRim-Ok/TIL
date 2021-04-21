# Python Web Programming with Django (2)

## Product App 작성

### URL Routing

> 1. 프로젝트/settings.py에 최상위 URLConf 모듈 지정
>
> - URLConf : URL과 일치하는 view를 찾기 위한 패턴들의 집합
> - 특정 URL과 VIEW 매핑
> - Django서버로 http 요청 -> URLConf 매핑 리스트 찾으며 검색

1. Product App 하위에 urls.py 생성

- mydjango_product/urls.py 수정 -> product.urls의 경로를 추가
  - admin/ 시작하는 url을 view와 매핑하여 찾으며 검색
  - http://127.0.0.1:8080/ 요청 오면 product.urls 검색

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
]
```

2. product/urls.py 작성 

- product 관련 url 따로 정의
- http://127.0.0.1:8080/ 요청 오면 views.post_list 메서드가 실행되도록 매핑

```
from django.urls import path
from . import views

urlpatterns = [
 path('', views.post_list, name='post_list'),
]
```



### View

> View : 애플리케이션의 로직  담당, 모델에서 필요한 정보를 받아 템플릿에 전달 (컨트롤러 역할)
>
> - URLConf에 매핑된 Callable Object
>   - 첫 번째 인자 : HttpRequest 인스턴스 
>   - HttpResponse 인스턴스를 리턴

1. product/views.py

- request를 parameter로 받아 post_list ()로 처리 -> render() 메서드 호출 -> product/post_list.html 템플릿을 리턴 

```
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone

# post 목록
def post_list(request):
    posts = Post.objects.filter(posted_date__lte = timezone.now()).order_by('posted_date')
    return render(request, 'product/post_list.html', {'posts': posts})
```



### Template

> 정보를 일정한 형태로 표시하기 위한 재사용 가능한 파일
>
> HTML 형식을 따른다.
>
> product/templates/product 디렉토리에 저장

1. post_list.html 템플릿 수정

```html
<!DOCTYPE html>
{% load static %}
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Django Product</title>
</head>

<body>
    <div class="page-header">
        <h1> <a href="{% url 'post_list'%}">Hello Django</a></h1>
    </div>
    <div class="content container">
        <div class = "row">
            <div class="col-md-8">
                {% for post in posts %}
                <div class="post">
                    <div class="date">
                        <p>Posted: {{post.posted_date}}</p>
                    </div>
                    <h4><a href="{% url 'post_detail' pk=post.pk %}">{{post.name}}</a></h4>
                    <p>{{post.desc|linebreaksbr}}</p>
                </div>
            {% endfor %}
            </div>
        </div>
    </div>

</body>
</html>
```



### 템플릿에서 동적 데이터 처리

> View가 Model로부터 data를 가져올 때 쿼리셋을 사용한다.

1. 템플릿 수정

- 파이썬 문법과 동일 -> 모든 객체 출력
- |linebreaksbr : br태그의 기능처럼 텍스트에서 행이 바뀌면 문단으로 변환

```
{% for post in posts %}
	{{post}}
	<p>{{post.desc|linebreaksbr}}</p>
{% endfor %}
```

2. Django Template Engine: django 기본 지원 템플릿 엔진

3. Template Engine의 문법

   1) Django Template Tag : {% %} 형식이며 빌트인 Tag는 아래와 같다.

   2) block tag : 템플릿 상속에서 사용

   ```
   {% block block-name %}
    content
   {% endblock %}
   ```

   3) comment tag : 템플릿 주석 (클라이언트 화면에서 보이지 않는다)

   ```
   {% comment %}
    content
   {% endcomment %}
   ```

   4) csrf_token tag : Cross Site Request Forgeries 막기 위한 CSRF Middleware 제공

   ​								: CSRF 토큰 체크 및 토큰 발급

   ```
   {% csrf_token %}
   ```

   5) extends tag : 자식 템플릿에서 부모 템플릿 명시

   ```
   {% extends "base.html" %}
   ```

   6) for tag : 객체 순회 (파이썬과 동일)

   ```
   { % for post in posts %}
    content
   {% endfor %}
   ```

   7) for ... empty tag : for tag에서 object 못 찾거나 비었을 때 empty block수행 

   ```
   {% for post in posts %}
    content1
   {% empty %}
    content2
   {% endfor %}
   ```

   8) if tag : 파이썬과 동일

   ```
   {% if post %}
    content1
   {% elif posts%}
    content2
   {% else %}
    content3
   {% endif %}
   ```

   9) url tag: URL Reverse 수행한 URL 출력

   ```
   {% url 'post_detail.html' %}
   ```



###  템플릿에 CSS 적용

> css 파일을 깔끔하게 정리하고 싶다면 ctrl + alt + l 사용

1. CSS 파일 작성

- product/static/css/product.css 작성

```css
/* css selector */
.page-header {
    background-color: #ff9400;
    margin-top: 0; /* 바깥쪽 여백*/
    padding: 20px 20px 20px 40px; /* 시계방향 순*/
}

.page-header h1, .page-header h1 a, .page-header h1 a:visited, .page-header h1 a:active {
    color: #ffffff;
    font-size: 36pt;
    text-decoration: none;
}
```

2. 템플릿에 적용

- product/templates/product/post_list.html 에 적용
- 새로운 css 파일을 적용하려면 서버를 내렸다가 다시 올려야한다.

```html
<!DOCTYPE html>
{% load static %}
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Django Product</title>
    <link rel="stylesheet" href="{%static 'css/blog.css' %}">
</head>
```

3. 부트스트랩 적용

-  product/templates/product/post_list.html 에 적용

```html
<!DOCTYPE html>
{% load static %}
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Django Product</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext" type="text/css">
    <link rel="stylesheet" href="{%static 'css/blog.css' %}">
</head>
```



### 템플릿 상속

> 동일한 정보 혹은 레이아웃을 사용하고자 할 때 재사용 파일을 목적으로 템플릿을 상속할 수 있다.
>
> 한 번만 수정하면 되기 때문에 유지보수에 용이하다.

1. 기본 템플릿 html (base.html) 생성 - 부모

- product/templates/product/base.html 생성

- {% block content %}{% endblock %} 으로 대체

  ```html
  <!DOCTYPE html>
  {% load static %}
  <html lang="ko">
  <head>
      <meta charset="UTF-8">
      <title>Django Product</title>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
      <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Lobster&subset=latin,latin-ext" type="text/css">
      <link rel="stylesheet" href="{%static 'css/blog.css' %}">
  </head>
  
  <body>
      <div class="page-header">
          <h1> <a href="{% url 'post_list'%}">Hello Django</a></h1>
      </div>
      <div class="content container">
          <div class = "row">
              <div class="col-md-8">
                {% block content %}
                {% endblock %}
              </div>
          </div>
      </div>
  
  </body>
  </html>
  ```

2. post_list.html 수정 - 자식

- product/templates/product/post_list.html

- 두 템플릿 연결하기 위해 {% extends 'product/base.html' %} 추가
- {% block content %}, {% endblock %} 사이에 코드 추가
- pk : Post모델의 primary key

```html
{% extends 'product/base.html'%}

{% block content %}
    {% for post in posts %}
    <div class="post">
        <div class="date">
            <p>Posted: {{post.posted_date}}</p>
        </div>
        <h4><a href="{% url 'post_desc' pk=post.pk %}">{{post.name}}</a></h4>
        <p>{{post.desc|linebreaksbr}}</p>
    </div>
    {% endfor %}
{% endblock %}
```



### Post Detail (글 상세) 페이지 작성하기

1. urls.py에 url 추가

- product/urls.py 수정
- post/ : URL이 POST 문자를 포함해야 함
- pk 변수에 값을 넣어서 post_detail view로 전송하겠다는 의미

```html
from django.urls import path
from . import views

urlpatterns = [
 path('', views.post_list, name='post_list'),
 path('post/<int:pk>', views.post_detail, name='post_detail'),
]
```

2. post_detail.html 페이지 수정

- product/templates/product/post_detail.html

```html
{% extends 'product/base.html'%}

{% block content %}
    <div class="post">
        {% if post.posted_date%}
            <div class="date">
                <p>Published: {{post.posted_date}}</p>
            </div>
        {% endif %}
        <h2>{{post.name}}</h2>
        <p>{{post.desc|linebreaksbr}}</p>
    </div>
{% endblock %}
```

3. views.py에 post_detail() 추가

```html
# Post 상세 목록
def post_detail(request, pk):
    # pk(왼)은 get_object_or_404()에 있는 param
    post = get_object_or_404(Post, pk=pk)
    return render(request,'product/post_detail.html', {'post': post})
```

4. post_list.html에 post detail 링크 추가

- {post.name} 클릭 시, 상세 페이지로 이동 가능

```
{% extends 'product/base.html'%}

{% block content %}
    {% for post in posts %}
    <div class="post">
        <div class="date">
            <p>Posted: {{post.posted_date}}</p>
        </div>
        <h4><a href="{% url 'post_detail' pk=post.pk %}">{{post.name}}</a></h4>
        <p>{{post.desc|linebreaksbr}}</p>
    </div>
    {% endfor %}
{% endblock %}
```

