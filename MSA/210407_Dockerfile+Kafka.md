# Dockerfile로 배포

1. order_ms.py
2. delivery_ms.py
3. kafka_consumer.py
4. (option) DB (Local DB or AWS RDS)
5. Zookeeper + Kafka 



### 1. delivery_ms.py

mysql DB 띄우기

```
PS C:\cloud\FLASK_DEMO2> docker run -d -p 13306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=true --name mydb mysql:5.7
26d42aa0114fa9dfb6c5a220f4fdab667d468fce7ec4eeba2a21fb74c9535fe1

PS C:\cloud\FLASK_DEMO2> docker ps
CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS                                NAMES
26d42aa0114f   mysql:5.7   "docker-entrypoint.s…"   6 seconds ago   Up 3 seconds   33060/tcp, 0.0.0.0:13306->3306/tcp   mydb
```

```
PS C:\cloud\FLASK_DEMO2> docker inspect mydb
```

"IPAddress": "172.17.0.2" 임을 확인

<br>

이에 맞춰 delivery_ms.py도 수정

```python
...
config = {
    'host': '172.17.0.2',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'mydb'
}
...
```

<br>

HeidiSQL에 localhost/13306으로 접속한 뒤 mydb 데이터베이스 생성 > delivery_status, orders table 생성

```sql
CREATE TABLE delivery_status(
  `id` int NOT NULL AUTO_INCREMENT,
  `delivery_id` varchar(50) DEFAULT NULL,
  `order_json` text,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ;

CREATE TABLE orders(
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) NOT NULL,
  `order_id` varchar(100) NOT NULL,
  `coffee_name` varchar(100) NOT NULL,
  `coffee_price` int NOT NULL,
  `coffee_qty` int DEFAULT '1',
  `ordered_at` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;
```

<br>

mariadb -> pymysql로 변경

```python
...

import flask_restful
#import mariadb
import pymysql
import json
import uuid

...

config = {
    'host': '172.17.0.2',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'mydb'
}

...

class Delivery(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()
 		...

# {"status" : "COMPLETED"}
class DeliveryStatus(flask_restful.Resource):
    def __init__(self):
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()
		...
```

<br>

Dockerfile 생성 (Dockerfile_delivery)

```dockerfile
FROM python:3.7.9-stretch

WORKDIR /myflask

RUN pip install flask
RUN pip install flask_restful
RUN pip install pymysql

COPY ./delivery_ms.py /myflask/app.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "6000"]
```

<br>

Dockerfile 빌드 및 실행

```
(msa) C:\cloud\FLASK_DEMO2>docker build -t mementohaeri/flask_delivery_ms -f Dockerfile_delivery .
```

```
(msa) C:\cloud\FLASK_DEMO2>docker run -d -p 16000:6000 mementohaeri/flask_delivery_ms
cee402d8a57a0cb31614182be266beffb6372107a84ecf489e2459b0a3a6d09e

(msa) C:\cloud\FLASK_DEMO2>docker ps
CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                NAMES
cee402d8a57a   mementohaeri/flask_delivery_ms   "flask run --host 0.…"   5 seconds ago    Up 4 seconds    0.0.0.0:16000->6000/tcp              funny_elion
26d42aa0114f   mysql:5.7                        "docker-entrypoint.s…"   18 minutes ago   Up 18 minutes   33060/tcp, 0.0.0.0:13306->3306/tcp   mydb
```

<br>

6000번 포트로 HTTP GET 메서드 전송 시 STATUS가 200임을 확인 (아직 데이터를 입력하지 않아 빈 값을 가져온다.)

![image](https://user-images.githubusercontent.com/77096463/113803467-958f8980-9797-11eb-8933-6383c2215b6f.png)

<br>

----------

