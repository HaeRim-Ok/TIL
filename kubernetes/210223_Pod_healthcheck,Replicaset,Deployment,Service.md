# Pod 헬스 체크 기능

헬스 체크 : pod의 컨테이너 애플리케이션이 정상적으로 동작하는지 확인하는 기능
- 헬스 체크 결과 **이상 감지** : 컨테이너 강제 종료 후 재시작
- **kubelet**이 헬스 체크 담당

<br>

활성 프로브 (Liveness Probe)
- 컨테이너 애플리케이션이 정상적으로 실행 중인지 검사
- 검사 실패하면 pod의 컨테이너 강제 종료 후 재시작
- 매니페스트에 명시적으로 설정해야 사용 가능

<br>

준비상태 프로브 (Readiness Probe)
- 컨테이너의 애플리케이션이 요청을 받을 준비가 되었는지 검사
- 검사 실패하면 서비스에 의한 요청 트래픽 전송 준비
- pod가 기동되고 준비될 때까지 요청이 전송되지 않도록 하기 위해 사용
- 매니페스트에 명시적으로 설정해야 사용 가능

<br>

1. 작업 디렉터리 생성 후 매니페스트 파일 (yaml) 작성

```
[vagrant@master ~]$ mkdir hc-probe
[vagrant@master ~]$ cd hc-probe/
[vagrant@master hc-probe]$ vi webapl-pod.yaml
```

```yaml
# webapl-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: webapl
spec:
  containers:
    - name: webapl
      image: mementohaeri/webapl:0.1     # 핸들러를 구현한 어플리케이션
      livenessProbe:                 # 애플리케이션의 동작 여부를 확인
        httpGet:                     # 지정된 포트와 경로로 HTTP GET 요청을 주기적으로 실행  
          path: /healthz             # 확인 경로
          port: 3000                 # 확인 포트
        initialDelaySeconds: 3       # 검사 개시 대기 시간
        periodSeconds: 5             # 검사 주기
      readinessProbe:                # 애플리케이션이 준비되었는지 확인
        httpGet:
          path: /ready
          port: 3000
        initialDelaySeconds: 15
        periodSeconds: 6
```

2. webapl 컨테이너 이미지 정의하기 위해 Dockerfile 작성

```dockerfile
# Dockerfile
FROM alpine:latest

RUN apk update && apk add --no-cache nodejs npm

WORKDIR /
ADD ./package.json /
RUN npm install			# package.json 안의 의존 모델 설치
ADD ./webapl.js /

CMD node /webapl.js
```

3. 헬스 체크를 위한 웹 애플리케이션 파일 작성

```js
//  웹 어플리케이션 
const express = require('express')
const app = express()
var start = Date.now()               // 어플리케이션이 시작된 시간

//  http://CONTAINER_IP:3000/healthz 형식으로 요청이 들어왔을 때 수행하는 기능을 정의하는 함수
app.get('/healthz', function(request, response) {
    var msec = Date.now() - start    // 어플리케이션이 시작된 후 경과된 시간
    var code = 200
    if (msec > 40000 ) {             // 경과된 시간이 40초 보다 작으면 200을, 크면 500을 응답코드로 반환
    code = 500
    }
    console.log('GET /healthz ' + code)
    response.status(code).send('OK')
})

app.get('/ready', function(request, response) {
    var msec = Date.now() - start
    var code = 500
    if (msec > 20000 ) {
    code = 200
    }
    console.log('GET /ready ' + code)
    response.status(code).send('OK')
})

app.get('/', function(request, response) {
    console.log('GET /')
    response.send('Hello from Node.js')
})

app.listen(3000);
```

4. 컨테이너 이미지 생성 후 레포지토리에 등록

```
[vagrant@master hc-probe]$ docker build --tag mementohaeri/webapl:0.1 .
[vagrant@master hc-probe]$ docker push mementohaeri/webapl:0.1 
```

5. pod 배포 후 헬스체크 기능 확인

```
[vagrant@master hc-probe]$ kubectl apply -f webapl-pod.yaml
```

```
[vagrant@master hc-probe]$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
webapl   1/1     Running   1          2m3s
```

6. logs 확인

```
[vagrant@master hc-probe]$ kubectl logs webapl
GET /healthz 200
GET /healthz 200
GET /healthz 200
GET /ready 500   	15 + 6초  
GET /healthz 200	20초
GET /ready 200    	15 + 12초 → 20초 초과	⇒ READY 상태 1/1가 설정
GET /healthz 200
GET /ready 200
GET /healthz 200
	:
```

7. 만일 Readiness Probe가 성공했을 때 webapl 컨테이너의 state값이 Running으로, Ready값이 true로 출력된다.

```
[vagrant@master hc-probe]$ kubectl describe pods webapl
Name:         webapl
Namespace:    default
Priority:     0
Node:         node1/192.168.56.11
Start Time:   Tue, 23 Feb 2021 14:50:27 +0000
Labels:       <none>
Annotations:  cni.projectcalico.org/podIP: 192.168.166.173/32
	:
    Port:           <none>
    Host Port:      <none>
    State:          Running
        Started:      Tue, 23 Feb 2021 04:41:17 +0000
    Ready:          True	
    :
```

<br>

<br>

# Replica Set

같은 스펙을 가지는 pod를 여러 개 생성하고 관리한다. 즉, 정해진 수의 동일한 pod가 항상 실행되도록 관리한다. 만일 노드 장애 등의 이유로 pod를 사용할 수 없는 상황이 생긴다면 다른 노드에서 pod를 다시 생성한다.

동일한 pod를 일일이 정의할 수도 있지만 이는 매우 비효율적이다. pod 가 삭제되거나 pod에 접근할 수 없는 경우 관리자가 직접 pod를 삭제하고 재생성해야하는 문제가 발생한다.

<br>

### 레플리카셋 생성 및 삭제

1. 기존에 생성한 리소스 정리

```
[vagrant@master hc-probe]$ kubectl delete -f webapl-pod.yaml
[vagrant@master hc-probe]$ cd ..
[vagrant@master ~]$ kubectl delete -f nginx-pod-with-ubuntu.yaml
[vagrant@master ~]$ cd sidecar
[vagrant@master sidecar]$ kubectl delete -f webserver.yaml
```

2. 레플리카셋 정의 (yaml)

```yaml
# replicaset-nginx.yaml

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx-pods-label
  template:                         ⇐ 포드 스펙, 포드 템플릿 → 생성할 포드를 명시
    metadata:
      name: my-nginx-pod
      labels:
        app: my-nginx-pods-label
    spec:
      containers:
        - name: my-nginx-container
          image: nginx:latest
          ports:
          - containerPort: 80
            protocol: TCP
```

3. 레플리카셋 생성 및 확인

```
[vagrant@master ~]$ kubectl apply -f replicaset-nginx.yaml
replicaset.apps/replicaset-nginx created

[vagrant@master ~]$ kubectl get pods,replicaset
NAME                         READY   STATUS    RESTARTS   AGE
pod/replicaset-nginx-46qmm   1/1     Running   0          11s
pod/replicaset-nginx-4725f   1/1     Running   0          11s
pod/replicaset-nginx-kcnx4   1/1     Running   0          11s

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.extensions/replicaset-nginx   3         3         3       11s
```

4. pod 개수 증가시킨 후 실행

```
[vagrant@master ~]$ cp replicaset-nginx.yaml replicaset-nginx-4pods.yaml
[vagrant@master ~]$ vi replicaset-nginx-4pods.yaml
```

```yaml
# replicaset-nginx-4pods.yaml

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-nginx
spec:
  replicas: 4			# replicaset-nginx 파일에 개수만 변경
  selector:
    matchLabels:
      app: my-nginx-pods-label
  template:
    metadata:
      name: my-nginx-pod
      labels:
        app: my-nginx-pods-label
    spec:
      containers:
        - name: my-nginx-container
          image: nginx:latest
          ports:
          - containerPort: 80
            protocol: TCP
```

여기서 `kubectl apply -f replicaset-nginx-4pods.yaml` 명령어 수행 시 **configured** 작업이 출력된다. 이는 기존 리소스를 수정하였다는 의미로, 기존 pod의 개수를 3개에서 4개로 변경했기 때문이다. (새로 생성된게 아님!)

```
[vagrant@master ~]$ kubectl apply -f replicaset-nginx-4pods.yaml
replicaset.apps/replicaset-nginx configured
```

```
[vagrant@master ~]$ kubectl get pods,replicasets
NAME                         READY   STATUS    RESTARTS   AGE
pod/replicaset-nginx-46qmm   1/1     Running   0          4m8s
pod/replicaset-nginx-4725f   1/1     Running   0          4m8s
pod/replicaset-nginx-b5ms5   1/1     Running   0          98s
pod/replicaset-nginx-kcnx4   1/1     Running   0          4m8s

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.extensions/replicaset-nginx   4         4         4       4m8s
```

5. 레플리카셋 삭제
- 레플리카셋 삭제하면 레플리카셋으로 생성한 pod도 함께 삭제된다.
  

```
[vagrant@master ~]$ kubectl delete rs replicaset-nginx
[vagrant@master ~]$ kubectl get pods,replicasets

No resources found.	
```

<br>

### 레플리카셋 동작원리

1. app: my-nginx-pods-label 라벨을 가지는 pod 생성 후 적용

```
[vagrant@master ~]$ vi nginx-pod-without-rs.yaml
```

```yaml
# nginx-pod-without-rs.yaml

apiVersion: v1
kind: Pod
metadata:
  name: my-nginx-pod
  labels:
    app: my-nginx-pods-label
spec:
  containers:
    - name: my-nginx-container
      image: nginx:latest
      ports:
      - containerPort: 80
```

```
[vagrant@master ~]$ kubectl apply -f nginx-pod-without-rs.yaml
```

pods 확인할 때 라벨을 확인한다.

```
[vagrant@master ~]$ kubectl get pods --show-labels
NAME           READY   STATUS    RESTARTS   AGE   LABELS
my-nginx-pod   1/1     Running   0          7s    app=my-nginx-pods-label	
```

2. app: my-nginx-pods-label 라벨을 가지는 pod  3개 생성 후 적용

```
[vagrant@master ~]$ vi replicaset-nginx.yaml
```

```yaml
# replicaset-nginx.yaml

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx-pods-label
  template:
    metadata:
      name: my-nginx-pod
      labels:
        app: my-nginx-pods-label
    spec:
      containers:
        - name: my-nginx-container
          image: nginx:latest
          ports:
          - containerPort: 80
            protocol: TCP
```

```
[vagrant@master ~]$ kubectl apply -f replicaset-nginx.yaml
```

동일한 라벨을 가진 기존 pod가 있는 경우 레플리카셋을 통해 pod 생성 시 그것을 제외한 pod를 생성한다. 그래서 아래와 같이 기존의 pod가 존재하면 2개의 pod만 추가된다.

```
[vagrant@master ~]$ kubectl get pods,replicasets --show-labels
NAME                         READY   STATUS    RESTARTS   AGE     LABELS
pod/my-nginx-pod             1/1     Running   0          2m59s   app=my-nginx-pods-label
pod/replicaset-nginx-7xw5w   1/1     Running   0          31s     app=my-nginx-pods-label
pod/replicaset-nginx-jvnsj   1/1     Running   0          31s     app=my-nginx-pods-label

NAME                                     DESIRED   CURRENT   READY   AGE   LABELS
replicaset.extensions/replicaset-nginx   3         3         3       31s   <none>
```

3. 1번에서 생성한 my-nginx-pod 삭제 후 pods 확인
- 기존의 pod 삭제하면 레플리카셋에서 설정한 pod의 개수가 3이기 때문에 새로운 pod가 자동으로 추가된다.


```
[vagrant@master ~]$ kubectl delete pods my-nginx-pod
pod "my-nginx-pod" deleted
[vagrant@master ~]$ kubectl get pods,replicasets --show-labels
NAME                         READY   STATUS    RESTARTS   AGE     LABELS
pod/replicaset-nginx-7xw5w   1/1     Running   0          8m52s   app=my-nginx-pods-label
pod/replicaset-nginx-c8qzr   1/1     Running   0          5s      app=my-nginx-pods-label
pod/replicaset-nginx-jvnsj   1/1     Running   0          8m52s   app=my-nginx-pods-label

NAME                                     DESIRED   CURRENT   READY   AGE     LABELS
replicaset.extensions/replicaset-nginx   3         3         3       8m52s   <none>
```

4. 레플리카셋이 생성한 pod의 라벨 변경 후 pod 정보 조회

```
[vagrant@master ~]$ kubectl edit pods replicaset-nginx-7xw5w
```

아래 두 부분을 주석 처리 후 저장한다.

```
# labels:
#  app: my-nginx-pods-label 
```

방금 수정한 pod의 label은 <none>으로 변경되며, 레플리카셋에서 설정한 라벨의 pod가 새로 생성된다. **왜냐하면 레플리카셋은 label을 기준으로 pod를 관리하기 때문이다.** 

```
[vagrant@master ~]$ kubectl get pods,replicasets --show-labels
NAME                         READY   STATUS    RESTARTS   AGE     LABELS
pod/replicaset-nginx-7xw5w   1/1     Running   0          11m     <none>
pod/replicaset-nginx-c8qzr   1/1     Running   0          2m27s   app=my-nginx-pods-label
pod/replicaset-nginx-jvnsj   1/1     Running   0          11m     app=my-nginx-pods-label
pod/replicaset-nginx-wg4r2   1/1     Running   0          47s     app=my-nginx-pods-label

NAME                                     DESIRED   CURRENT   READY   AGE   LABELS
replicaset.extensions/replicaset-nginx   3         3         3       11m   <none>
```

5. 레플리카셋 삭제

```
[vagrant@master ~]$ kubectl delete rs replicaset-nginx
replicaset.extensions "replicaset-nginx" deleted

[vagrant@master ~]$ kubectl get replicaset
No resources found.
```

하지만 라벨이 삭제된 pod는 위 명령어에 의해 삭제되지 않는다.

```
[vagrant@master ~]$ kubectl get pods --show-labels
NAME                     READY   STATUS    RESTARTS   AGE   LABELS
replicaset-nginx-7xw5w   1/1     Running   0          14m   <none>
```

<br>

<br>

# Deployment

Replica Set, pod의 배포 및 업데이트를 관리한다.

<br>

### 디플로이먼트 생성 및 삭제

1. 디플로이먼트 정의, 생성, 확인

```
[vagrant@master ~]$ vi deployment-nginx.yaml
```

```yaml
# deployment-nginx.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-nginx
  template:
    metadata:
      name: my-nginx-pod
      labels:
        app: my-nginx
    spec:
      containers:
        - name: nginx
          image: nginx:1.10
          ports:
          - containerPort: 80
```

```
[vagrant@master ~]$ kubectl apply -f deployment-nginx.yaml
deployment.apps/my-nginx-deployment created
```

```
[vagrant@master ~]$ kubectl get deployment,replicasets,pods
NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/my-nginx-deployment   3/3     3            3           61s

NAME                                                 DESIRED   CURRENT   READY   AGE
replicaset.extensions/my-nginx-deployment-9b5988dd   3         3         3       61s

NAME                                     READY   STATUS    RESTARTS   AGE
pod/my-nginx-deployment-9b5988dd-4hzwm   1/1     Running   0          61s
pod/my-nginx-deployment-9b5988dd-cj7q5   1/1     Running   0          61s
pod/my-nginx-deployment-9b5988dd-w7jgs   1/1     Running   0          61s
```

2. 디플로이먼트 삭제 (레플리카셋, pod도 함께 삭제된다)

```
[vagrant@master ~]$ kubectl delete deployment my-nginx-deployment
deployment.extensions "my-nginx-deployment" deleted

[vagrant@master ~]$ kubectl get deployment,replicasets,pods

No resources found.
```

### 디플로이먼트 사용 이유 

디플로이먼트를 통해 애플리케이션의 업데이트 및 배포를 용이하기 만들기 위해 사용한다. 

1. --record 옵션을 추가해 디플로이먼트 생성한다.

```
[vagrant@master ~]$ kubectl apply -f deployment-nginx.yaml --record

[vagrant@master ~]$ kubectl get pods
NAME                                 READY   STATUS    RESTARTS   AGE
my-nginx-deployment-9b5988dd-88bx7   1/1     Running   0          15s
my-nginx-deployment-9b5988dd-964pt   1/1     Running   0          15s
my-nginx-deployment-9b5988dd-m58r2   1/1     Running   0          15s
```

2. pod의 이미지 변경

```
[vagrant@master ~]$ kubectl set image deployment my-nginx-deployment nginx=nginx:1.11 --record
deployment.extensions/my-nginx-deployment image updated
```

이미지를 변경하면 기존의 pod는 종료되며 새로운 pod가 자동으로 생성된다.

```
[vagrant@master ~]$ kubectl get pods
NAME                                  READY   STATUS    RESTARTS   AGE
my-nginx-deployment-d4659856c-752zr   1/1     Running   0          28s
my-nginx-deployment-d4659856c-q724x   1/1     Running   0          20s
my-nginx-deployment-d4659856c-r8cg8   1/1     Running   0          32s

[vagrant@master ~]$ kubectl get replicasets
NAME                            DESIRED   CURRENT   READY   AGE
my-nginx-deployment-9b5988dd    0         0         0       2m		//기존
my-nginx-deployment-d4659856c   3         3         3       74s		//방금 생성됨
```

3. 리버전 정보 확인

```
[vagrant@master ~]$ kubectl rollout history deployment my-nginx-deployment
deployment.extensions/my-nginx-deployment
REVISION  CHANGE-CAUSE
1         kubectl apply --filename=deployment-nginx.yaml --record=true
2         kubectl set image deployment my-nginx-deployment nginx=nginx:1.11 --record=true
```

4. 이전 버전(9b5988dd)의 레플리카셋으로 롤백  후 pod 확인
- --to-revision 옵션에 위의 결과를 참고하여 어느 상태로 돌아가고 싶은지 명시하기

```
[vagrant@master ~]$ kubectl rollout undo deployment my-nginx-deployment --to-revision=1
deployment.extensions/my-nginx-deployment rolled back

[vagrant@master ~]$ kubectl get pods
NAME                                 READY   STATUS    RESTARTS   AGE
my-nginx-deployment-9b5988dd-4782d   1/1     Running   0          40s
my-nginx-deployment-9b5988dd-4ctjl   1/1     Running   0          51s
my-nginx-deployment-9b5988dd-8wgtx   1/1     Running   0          46s

[vagrant@master ~]$ kubectl get replicasets
NAME                            DESIRED   CURRENT   READY   AGE
my-nginx-deployment-9b5988dd    3         3         3       5m11s
my-nginx-deployment-d4659856c   0         0         0       4m25s
```

5. 모든 리소스 삭제

```
[vagrant@master ~]$ kubectl delete deployment,replicaset,pod --all
```

<br>

<br>

# Service

포드를 연결하고 외부에 노출한다.

YAML 파일에 containerPort 항목을 정의했다고 해서 해당 포트가 바로 외부에 노출되는 것은 아니다. 해당 포트로 사용자가 접근하거나, 다른 디플로이먼트의 pod들이 내부적으로 접근하려면 서비스(service) 객체가 필요하다.

<br>

**서비스의 기능**

- 여러 개의 pod에 쉽게 접근할 수 있도록 고유한 도메인 이름을 부여한다. 
- 여러 개의 pod에 접근할 때, 요청을 분산하는 로드 밸런서 기능을 수행한다. 
- 클라우드 플랫폼의 로드 벨런서, 클러스터 노드의 포트 등을 통해 pod를 외부에 노출시킨다.

**서비스의 종류(type)**

1. ClusterIP 타입
- 쿠버네티스 내부에서만 pod들에 접근할 때 사용
- 외부로 pod를 노출하지 않기 때문에 쿠버네티스 클러스터 내부에서만 사용되는 pod에 적합

2. NodePort 타입
- pod에 접근할 수 있는 포트를 클러스터의 모든 노드에 동일하게 개방
- 외부에서 pod에 접근할 수 있는 서비스 타입
- 접근할 수 있는 포트는 랜덤으로 정해지지만, 특정 포트로 접근하도록 설정할 수 있음

3. LoadBalancer 타입
- 클라우드 플랫폼에서 제공하는 로드 벨러서를 동적으로 프로비저닝해 pod에 연결
- NodePort 타입과 마찬가지로 외부에서 pod에 접근할 수 있는 서비스 타입
- 일반적으로 AWS, GCP 과 같은 클라우드 플랫폼 환경에서 사용

<br>

### 디플로이먼트 생성

1. 디플로이먼트 정의, 생성, 확인

```
[vagrant@master ~]$ vi deployment-hostname.yaml
```

```yaml
# deployment-hostname.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: hostname-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webserver
  template:
    metadata:
      name: my-webserver
      labels:
        app: webserver
    spec:
      containers:
        - name: my-webserver
          image: alicek106/rr-test:echo-hostname     #pod의 호스트 이름을 반환하는 웹 서버 이미지
          ports:
          - containerPort: 80
```

```
[vagrant@master ~]$ kubectl apply -f deployment-hostname.yaml
deployment.apps/hostname-deployment created

[vagrant@master ~]$ kubectl get pods -o wide
NAME                                   READY   STATUS    RESTARTS   AGE   IP                NODE    NOMINATED NODE   READINESS GATES
hostname-deployment-6cd58767b4-4r6xk   1/1     Running   0          23s   192.168.104.57    node2   <none>           <none>
hostname-deployment-6cd58767b4-644gb   1/1     Running   0          23s   192.168.166.185   node1   <none>           <none>
hostname-deployment-6cd58767b4-7skx2   1/1     Running   0          23s   192.168.104.56    node2   <none>           <none>
```

2. 클러스터 노드 중 하나에 접속 -> curl을 이용해 pod에 접근한다.

```
[vagrant@master ~]$ kubectl run -i --tty --rm debug --image=alicek106/ubuntu:curl --restart=Never curl 192.168.104.57 | grep Hello
        <p>Hello,  hostname-deployment-6cd58767b4-4r6xk</p>     </blockquote>
```

<br>

### ClusterIP 타입의 서비스 - K8S 클러스터 내부에서만 POD에 접근

1. hostname-svc-clusterip.yaml 파일 생성 후 서비스 확인

```yaml
# hostname-svc-clusterip.yaml

apiVersion: v1
kind: Service
metadata:
  name: hostname-svc-clusterip
spec:
  ports:
  - name: web-port
    port: 8080                 # 서비스의 IP에 접근할 때 사용할 포트
    targetPort: 80             # selector 항목에서 정의한 라벨의 pod의 내부에서 사용하고 있는 포트
  selector:                    # 접근 허용할 pod의 라벨을 정의
    app: webserver
  type: ClusterIP              # 서비스 타입
```

```
[vagrant@master ~]$ kubectl apply -f hostname-svc-clusterip.yaml
[vagrant@master ~]$ kubectl get svc
NAME                     TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-service            NodePort    10.100.84.147   <none>        8080:30221/TCP   4d7h
hostname-svc-clusterip   ClusterIP   10.98.30.9      <none>        8080/TCP         7h21m
kubernetes               ClusterIP   10.96.0.1       <none>        443/TCP          4d15h
nginx-test               NodePort    10.104.64.74    <none>        80:30403/TCP     4d11h
```

2. 임시 pod 생성하여 서비스로 요청한다.

```
[vagrant@master ~]$ kubectl run -it --rm debug --image=alicek106/ubuntu:curl --restart=Never -- bash

If you don't see a command prompt, try pressing enter.
root@debug:/# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: tunl0@NONE: <NOARP> mtu 1480 qdisc noop state DOWN group default qlen 1000
    link/ipip 0.0.0.0 brd 0.0.0.0
4: eth0@if28: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1440 qdisc noqueue state UP group default
    link/ether ae:29:ed:e5:4b:1a brd ff:ff:ff:ff:ff:ff
    inet 192.168.104.58/32 scope global eth0
       valid_lft forever preferred_lft forever

# 서비스와 연결된 pod에 로드밸런싱을 수행한다.
root@debug:/# curl 10.98.30.9:8080 --silent | grep Hello
        <p>Hello,  hostname-deployment-6cd58767b4-644gb</p>     </blockquote>

root@debug:/# curl 10.98.30.9:8080 --silent | grep Hello
        <p>Hello,  hostname-deployment-6cd58767b4-4r6xk</p>     </blockquote>

root@debug:/# curl 10.98.30.9:8080 --silent | grep Hello
        <p>Hello,  hostname-deployment-6cd58767b4-644gb</p>     </blockquote>
```

4. 서비스 이름으로 접근한다.
- k8s는 애플리케이션이 서비스 혹은 pod를 쉽게 찾을 수 있도록 내부 DNS를 구동한다.


```
root@debug:/# curl hostname-svc-clusterip:8080 --silent | grep Hello
        <p>Hello,  hostname-deployment-6cd58767b4-4r6xk</p>     </blockquote>
```

5. 서비스 삭제

```
[vagrant@master ~]$ kubectl delete service hostname-svc-clusterip
service "hostname-svc-clusterip" deleted
```

