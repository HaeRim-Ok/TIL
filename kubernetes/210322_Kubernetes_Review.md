2024~2025년 기점으로 클라우드를 전면적으로 사용할 예정<br>
-> 로컬에 사용하고 있던 미들웨어나 운영체제 등을 클라우드로 이전할 계획<br>
-> 외산 브랜드보다는 국산 브랜드 위주<br>
-> 이유 : 비용, 속도 측면에서 유리 / 수작업의 한계 / 시스템 재사용 가능
<br>
운영체제, 데이터베이스, 미들웨어 등의 리소스를 클라우드를 이용해 재분할<br>
네이버, LG 등이 클라우드 컴퓨팅이 가능하게끔 컴퓨팅 파워를 할당시켜줌<br>

도커, K8S -> 가상화 솔루션으로 미들웨어 성격을 가짐<br>
클라우드 서비스라기 보다는 클라우드에서 운영할 수 있는 가상화 기술을 관리하는 역할<br>
도커 : 컨테이너 가상화의 한 종류 -> 유료화될 가능성<br>
- crio-o<br>
- containerd<br>
- AWS, Naver, LG, KT(public cloud) 에서도 도커 서비스 제공 가능<br>
	- Database<br>
	- IaaS : 가상의 HW 구축<br>
	- PaaS : 플랫폼<br>
	- SaaS : SW (Gmail, ERP, Office365, Adobe Photoshop..)<br>
	- PreaaS ...<br>

쿠버네티스 : 도커, crio-o, containerd를 관리 (컨테이너 가상화를 관리)<br>
- pod : 컨테이너가 포함되어 있는데, 이는 도커, crio-o, containerd로 만들 수 있음<br>
- 즉, 쿠버네티스가 없어도 도커를 사용할 수 있음<br>
- 쿠버네티스는 도커, crio-o, containerd 중 하나가 있어야 사용 가능<br>

오픈스택 : 하이브리드 클라우드, 프라이빗 클라우드 구축 시 사용될 수 있는 솔루션<br>

VPC : Virtual Private Cloud(Network) > aws에서 구축하는 네트워크 <br>
- 서브넷 : 같은 네트워크에 묶여져 있음 > 통신할 때 제약이 없음<br>
- IPv4<br>
    - 0~255.0~255.0~255.0~255<br>
    - 256*256*256*256<br>
    - 가상 네트워크 private network<br>
    - 내부적으로 통신이 가능<br>
    - 외부와 통신하기 위해서는 Gateway 필요 <br>

-------------

<br>

# k8s 실습

pod 생성 
```
[root@master vagrant]# vi my_hello_pod.yml 

[root@master vagrant]# kubectl apply -f my_hello_pod.yml 
pod/hello-pod created
```
```
[root@master vagrant]# cat my_hello_pod.yml
apiVersion: v1
kind: Pod
metadata:
 name: hello-pod
 labels:
  app: hello
spec:
 containers:
 - name: hello-container
   image: edowon0623/hello:2.0 
   ports:
   - containerPort: 8000
```

pod 상세 정보 확인

```
[root@master vagrant]# kubectl get pods -o wide
NAME                                   READY   STATUS      RESTARTS   AGE    IP                NODE    NOMINATED NODE   READINESS GATES
hello-pod                              1/1     Running     0          2m8s   192.168.104.47    node2   <none>           <none>
```

hello-pod가 실행 중인 node2로 가서 정보 확인

```
[root@node2 vagrant]# docker ps | grep hello-pod
60a5e71d5c9d   edowon0623/hello       "docker-entrypoint.s…"   About a minute ago   Up About a minute             k8s_hello-container_hello-pod_default_6bd3f9cf-8645-4bab-b8b2-8cc1a3c086f0_0
5f771298912f   k8s.gcr.io/pause:3.1   "/pause"                 2 minutes ago        Up 2 minutes                  k8s_POD_hello-pod_default_6bd3f9cf-8645-4bab-b8b2-8cc1a3c086f0_0
```

hello-pod가 잘 실행 중인지 확인 (내부 클러스터)

```
[root@master vagrant]# curl 192.168.104.47:8000
Hello, World (on K8S)!
```

<br>

service 생성 (외부에서도 접근하고 사용할 수 있게끔)

```
[root@master vagrant]# cat my_hello_svc.yml 
apiVersion: v1
kind: Service
metadata:
 name: hello-service
spec:
 selector:
  app: hello
 ports:
  - port: 8001
    targetPort: 8000
 type: NodePort
```

service 등록 및 확인

- 외부에서 사용할 때는 31827번으로 접근

```
[root@master vagrant]# kubectl apply -f my_hello_svc.yml
service/hello-service configured

[root@master vagrant]# kubectl get svc
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-service           NodePort    10.100.84.147   <none>        8001:31827/TCP   30d
```

service 테스트 

```
//서비스 접속
[root@master vagrant]# curl 127.0.0.1:31827
Hello, World (on K8S)!
```

service 상세 정보 확인

```
[root@master vagrant]# kubectl describe svc hello-service
Name:                     hello-service
Namespace:                default
Labels:                   <none>
Annotations:              kubectl.kubernetes.io/last-applied-configuration:
                            {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"name":"hello-service","namespace":"default"},"spec":{"ports":[{"port":80...
Selector:                 app=hello
Type:                     NodePort
IP:                       10.100.84.147
Port:                     <unset>  8001/TCP
TargetPort:               8000/TCP
NodePort:                 <unset>  31827/TCP
Endpoints:                192.168.104.47:8000
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```

service 내용 변경

```
[root@master vagrant]# kubectl edit svc hello-service
```

윈도우에서 127.0.0.1:31827를 통해 접속하고 싶을 때 vagrant에 포트 포워딩 필요

```
C:\Users\Lenovo>cd C:\cloud\vagrant
C:\cloud\vagrant>code Vagrantfile
```

vagrantFile을 보면 30403포트가 열려있기 때문에 svc의 포트를 변경할 예정

- hello-pod가 실행 중인 노드를 확인 후 해당 노드의 포트포워딩 확인 및 설정

```
   # Node2
  config.vm.define:"node-2" do |cfg|
    cfg.vm.box = "centos/7"
    cfg.vm.provider:virtualbox do |vb|
        vb.name="node-2"
        vb.customize ["modifyvm", :id, "--cpus", 1]
        vb.customize ["modifyvm", :id, "--memory", 1024]
    end
    cfg.vm.host_name="node2"
    # cfg.vm.synced_folder ".", "/vagrant", type: "nfs"
    cfg.vm.network "private_network", ip: "192.168.56.12"
    cfg.vm.network "forwarded_port", guest: 22, host: 19212, auto_correct: false, id: "ssh"
    cfg.vm.network "forwarded_port", guest: 8080, host: 28080
    cfg.vm.network "forwarded_port", guest: 30403, host: 30403
    cfg.vm.network "forwarded_port", guest: 30404, host: 30404
    cfg.vm.provision "shell", path: "bash_ssh_conf_4_CentOS.sh"
  end
```
```
[root@master vagrant]# kubectl edit svc hello-service
```

![image](https://user-images.githubusercontent.com/77096463/111943247-67177a80-8b18-11eb-8346-6a886fd8aa80.png)

<br>

이후 127.0.0.1:30403 접속 시 윈도우에서 접속 가능

![image](https://user-images.githubusercontent.com/77096463/111943203-4c450600-8b18-11eb-8dae-d0648e0e6380.png)


<br>





# 클라우드에 k8s 설치

AWS : EKS / 구글 : kops (기존 AWS의 EC2에 설치 가능)

- Minikube : 운영환경에서 적합하지 않음 
- Master와 작업 진행하는 Worker 노드 사용 권장

<br>

### 1. 작업환경 구축

**가상머신** : ubuntu 18.04 준비 (t2.micro) ->US리전

**kops 설치**

```
$ wget -O kops https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest)
```

**kubectl 설치**

**IAM - Group 생성 -> User 생성**



**AWS CLI 설치**

**AWS CLI 설정**

```
$ aws configure
```

**S3 버킷 생성**

**환경 변수 설정**

**SSH Key Pair 생성**

**사용 가능한 AZ 확인**

### 클러스터 생성

**클러스터 생성을 위한 AZ 지정**

**마스터 노드 확인, 노드 수를 조절**

**클러스터 생성**