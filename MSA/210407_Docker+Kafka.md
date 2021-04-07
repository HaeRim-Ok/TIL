# Docker로 배포

1. order_ms.py
2. delivery_ms.py
3. kafka_consumer.py
4. (option) DB (Local DB or AWS RDS)
5. Zookeeper + Kafka 



### 1. DB

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

### 2. delivery_ms.py

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

### 3. Zookeeper + Kafka

git clone

```
(msa) C:\cloud\FLASK_DEMO2>git clone https://github.com/wurstmeister/kafka-docker.git
```

<br>

네트워크 생성

```
(msa) C:\cloud\FLASK_DEMO2\kafka-docker>docker network create --gateway 172.19.0.1 --subnet 172.19.0.0/24 my-coffee-network
704cce63302734e986f596141e03ed94e9a5589c54279ca2d9fc2d1bcc73390b
```

<br>

docker-compose-single-broker.yml 파일 수정 후 실행

- `depends_on` : zookeeper 먼저 기동 후 kafka 기동

```yaml
version: '2'
services:
  zookeeper:
    image: wurstmeister/zookeeper
    ports:
      - "2181:2181"
    networks:
      my-network:
        ipv4_address: 172.19.0.100
  kafka:
    image: wurstmeister/kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_ADVERTISED_HOST_NAME: 172.19.0.101
      KAFKA_CREATE_TOPICS: "test:1:1"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - zookeeper
    networks:
      my-network:
        ipv4_address: 172.19.0.101

networks:
  my-network:
    name: my-coffee-network
```

```
(msa) C:\cloud\FLASK_DEMO2\kafka-docker>docker-compose -f docker-compose-single-broker.yml up -d
```

```
(msa) C:\cloud\FLASK_DEMO2\kafka-docker>docker ps
CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                                NAMES
235ad27bc94f   wurstmeister/kafka               "start-kafka.sh"         14 seconds ago   Up 13 seconds   0.0.0.0:9092->9092/tcp                               kafka-docker_kafka_1
9f7b0c608044   wurstmeister/zookeeper           "/bin/sh -c '/usr/sb…"   26 seconds ago   Up 25 seconds   22/tcp, 2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp   kafka-docker_zookeeper_1
cee402d8a57a   mementohaeri/flask_delivery_ms   "flask run --host 0.…"   2 hours ago      Up 2 hours      0.0.0.0:16000->6000/tcp                              funny_elion
26d42aa0114f   mysql:5.7                        "docker-entrypoint.s…"   2 hours ago      Up 2 hours      33060/tcp, 0.0.0.0:13306->3306/tcp                   mydb
```

<br>




