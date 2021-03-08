# Deployment (배포)

**빅뱅 배포**<br>
애플리케이션의 전체 또는 대부분을 한 번에 업데이트

**롤링 배포 (단계적 배포)**<br>
애플리케이션의 이전 버전 (파란색)을 점차적으로 새 버전(초록색) 으로 교체

![image](https://user-images.githubusercontent.com/77096463/110263563-77990280-7ffa-11eb-9025-1e6f0323f576.png)

<br>

**Blue-Green, Red-Black, A/B 배포** <br>
두 개의 동일한 프로덕션 환경이 병렬로 작동<br>
하나는 모든 트래픽을 수신하는 실행 환경, 다른 하나는 유휴 상태<br>

![image](https://user-images.githubusercontent.com/77096463/110263703-d494b880-7ffa-11eb-8b2f-2b26c26a5c71.png)

새로운 버전의 애플리케이션은 Green 환경에 배포되고 기능 및 성능 테스트를 수행<br>
테스트 결과가 성공이면 애플리케이션의 트래픽을 파란색에서 초록색으로 라우팅

![image](https://user-images.githubusercontent.com/77096463/110263826-2ccbba80-7ffb-11eb-908a-b378fde6feb8.png)

초록색이 활성화된 후 문제가 발생하면 트래픽을 다시 파란색으로 라우팅 <br>
Blue-Green 배포에서는 두 시스템 모두가 동일한 지속 계층 또는 데이터베이스 백엔드를 사용해야 함

**Canary (카나리아) 배포**<br>
프로덕션 인프라의 작은 부분에 새 애플리케이션 코드를 배포해서 소수의 사용자만 해당 애플리케이션으로 라우팅<br>
보고된 오류가 없는 새 버전은 나머지 인프라에 점차적으로 롤 아웃

![image](https://user-images.githubusercontent.com/77096463/110264178-02c6c800-7ffc-11eb-935b-9eba1ae22896.png)

<br>

**Amazon API Gateway**<br>
개발자가 규모와 관계 없이 API를 쉽게 생성, 게시, 유지관리, 모니터링, 보안 유지를 할 수 있도록 하는 완전 관리형 서비스<br>
API : 애플리케이션이 백엔드 서비스의 데이터, 비즈니스 로직 또는 기능에 액세스할 수 있도록 해주는 역할<br>
API 유형 : RESTful API, WebSocket API
![image](https://user-images.githubusercontent.com/77096463/110264661-2b02f680-7ffd-11eb-9831-fc01545ad7a9.png)

<br>

-----------

# **API Gateway Canary Release Deployment**

### Lab 구성도

![image](https://user-images.githubusercontent.com/77096463/110264762-66052a00-7ffd-11eb-9d4f-a931420f1821.png)

<br>

IAM 역할 확인 -> CloudWatch Logs와 DynamoDB 권한 가짐

![image](https://user-images.githubusercontent.com/77096463/110265022-f5aad880-7ffd-11eb-8f61-f4cb47dd7204.png)

<br>

### Create First Lambda Function

첫 번째 람다 함수 생성
- 함수 이름 : mathCeil
- 실행 역할 : 기존 역할 사용 -> cfst~ 역할 선택

![image](https://user-images.githubusercontent.com/77096463/110265120-30ad0c00-7ffe-11eb-93fa-862ee2f36937.png)

<br>

아래의 코드를 index.js에 작성하기

```js
console.log('Loading Lambda function');

exports.handler = async (event, context, callback) => {
    let resultNum = Math.ceil(999.99); //소수점 이하 올림

    callback(null, 'this is the original function (Math.ceil) = ' + resultNum);
};
```

![image](https://user-images.githubusercontent.com/77096463/110265329-a44f1900-7ffe-11eb-8ee2-a6ad9eb938e3.png)

### Create Second Lambda Function

두 번째 람다 함수 생성

- 함수 이름 : mathFloor
- 실행 역할 : 기존 역할 사용 -> cfst~ 역할 선택

![image](https://user-images.githubusercontent.com/77096463/110265434-e5dfc400-7ffe-11eb-8835-858ab746794e.png)

<br>

아래의 코드를 index.js에 작성하기

```js
console.log('Loading Lambda function');

exports.handler = async (event, context, callback) => {
    let resultNum = Math.floor(999.99);	//소수점 이하 내림

    callback(null, 'this is the canary function (Math.floor) = ' + resultNum);
};
```

![image](https://user-images.githubusercontent.com/77096463/110265483-03149280-7fff-11eb-9c67-d39c5f454aa4.png)

<br>

### Create and Deploy Our API Within API Gateway

### Create the API

> 외부에서 람다 함수 호출할 수 있도록 API 생성<br>

API Gateway > REST API > 구축<br>
- 새 API
- API 이름 : devopsCanary
- 설명 : API Gateway Canary Testing
- 엔드포인트 유형 : 지역

![image](https://user-images.githubusercontent.com/77096463/110265624-571f7700-7fff-11eb-82b1-698ec82eb889.png)

<br>

리소스 탭 작업 > 메서드 생성 > / > GET 선택 <br>
/-GET- 설정 > Lambda 함수 -> mathCeli 선택

![image](https://user-images.githubusercontent.com/77096463/110265786-b7aeb400-7fff-11eb-882e-46273e167e4a.png)

<br>

API 동작 방식 확인

![image](https://user-images.githubusercontent.com/77096463/110265889-f6dd0500-7fff-11eb-8bde-b19d7d1d98ec.png)

<br>

API 테스트
![image](https://user-images.githubusercontent.com/77096463/110266154-94d0cf80-8000-11eb-8210-a500d2a0ff5b.png)

<br>

### Deploy the First Function

리소스 탭 작업 > API 배포 

![image](https://user-images.githubusercontent.com/77096463/110266391-09a40980-8001-11eb-8d47-253220fbc11c.png)

<br>

test 스테이지 편집기에서 URL 주소를 클릭했을 때 새로고침을 여러번 해도 아까 API 테스트했던 결과와 동일한 결과가 나오는 것을 확인한다. (API 게이트웨이에 연결되어 있는 람다 함수가 MathCeil 하나이므로)

![image](https://user-images.githubusercontent.com/77096463/110266479-3821e480-8001-11eb-8286-a1cfdfe8b78b.png)

<br>

Canary 탭 > Canary로 지정된 요청 백분율을 10%로 변경 
- 브라우저로 API 게이트웨이 엔드포인트 호출해도 변화가 없음을 확인 -> 새로운 버전이 등록되지 않았기 때문


![image](https://user-images.githubusercontent.com/77096463/110267586-7d471600-8003-11eb-949d-8f25565fb621.png)

<br>

람다 함수를 mathFloor로 변경

![image](https://user-images.githubusercontent.com/77096463/110267749-c4cda200-8003-11eb-8e17-1e77d59d5092.png)

<br>

테스트를 여러번 수행해도 동일한 결과 (999) 를 반환하는 것을 확인

![image](https://user-images.githubusercontent.com/77096463/110267792-dd3dbc80-8003-11eb-96fb-b659b10a76e7.png)

<br>

### Deploy the Second Function

API 배포 -> 배포 스테이지 : test (Canary 사용)

![image](https://user-images.githubusercontent.com/77096463/110267869-01999900-8004-11eb-99ea-7da6822fbad4.png)

<br>

주소는 동일한데 1:9의 비율로 999, 1000 값이 번갈아가며 나옴

![image](https://user-images.githubusercontent.com/77096463/110267939-24c44880-8004-11eb-856e-89aed741bd9c.png)

<br>![image](https://user-images.githubusercontent.com/77096463/110267954-2a219300-8004-11eb-8183-5bfe3e73d3ff.png)

<br>

Canary로 지정된 요청 비율을 50%로 조정

![image](https://user-images.githubusercontent.com/77096463/110268094-766cd300-8004-11eb-9045-0a0755cd4c75.png)

<br>

동일한 URL에서 새 버전과 이전 버전이 5:5 비율로 제공됨을 확인할 수 있다.

### Promote the Canary

Canary 탭 > Canary 승격 

- test로 지정된 요청 백분율 : 100%로 변경됨

![image](https://user-images.githubusercontent.com/77096463/110268309-cba8e480-8004-11eb-94fc-8c0456e1f890.png)

<br>

이제 URL 접속 시 새로운 버전의 실행 결과인 999만 제공됨을 확인

![image](https://user-images.githubusercontent.com/77096463/110268418-f2ffb180-8004-11eb-89bd-50641a3dae4d.png)