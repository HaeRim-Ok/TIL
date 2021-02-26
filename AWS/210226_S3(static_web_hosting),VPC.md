# Configuring Amazon S3 Buckets to Host a Static Website with a Custom Domain

![image-20210226091453817](210226_.assets/image-20210226091453817.png)

**Amazon S3**

- 객체 기반의 무제한 파일 저장 스토리지
- 99.999999999% 내구성
- 사용한 만큼만 지불 (GB 당 과금)
- 객체 URL을 통해 쉽게 파일 공유
- **정적 웹 사이트 호스팅** 가능 -> 즉 고정된 형태의 데이터가 담겨있어서 사용자에게 항상 동일한 내용을 반환한다. (HTML, CSS, JavaScript, fonts, and images)
<br>

**Amazon Glacier**

- 99.999999999% 내구성
- 아카이브 및 백업 용도
- S3 대비 1/5 비용
- 리전에 따라 가격이 상이함
<br>



### Lab 구성도

![image](https://user-images.githubusercontent.com/77096463/109244019-4ca3f700-7821-11eb-875a-83e08e8095e8.png)

<br>

### S3 bucket 생성

1. Route 53 > 호스팅 영역 클릭 (이미 할당되어진 도메인이 있다)

- 도메인 이름을 복사 : cmcloudlab613.info
<br>
2. 깃허브링크에서 html 파일들을 다운로드

- https://github.com/ACloudGuru-Resources/aws-s3-route53-static-website/tree/main
<br>
3. S3 > 버킷 만들기 클릭 > 아래 처럼 설정한 뒤 버킷 생성

- 버킷 이름 : 1번에서 복사한 도메인 이름 입력 (**연동할 도메인 이름으로 버킷 생성**)
- 리전 : us-east-1 (버지니아 북부)
- 모든 퍼블릭 액세스 차단 체크 해제하기

![image-20210226093352896](210226_.assets/image-20210226093352896.png)
<br>

4. 생성한 버킷 클릭 > 객체 탭 > 업로드 클릭

- 깃허브에서 다운받은 penguinsite 폴더를 업로드한다.

![image-20210226093626248](210226_.assets/image-20210226093626248.png)
<br><br>

### 정적 웹사이트 생성
1. 생성한 버킷 클릭 > 속성 탭 > 정적 웹 사이트 호스팅 > 편집 클릭 > 아래 처럼 설정한 뒤 변경 사항 저장 클릭

- 정적 웹 사이트 호스팅 : 활성화
- 호스팅 유형 : 정적 웹 사이트 호스팅
- 인덱스 문서 (기본 문서) : index.html
- 오류 문서 : error.html

![image-20210226094006493](210226_.assets/image-20210226094006493.png)
<br>
2. 버킷 웹 사이트 엔드포인트 링크 (웹서버 역할) 클릭 > 403 Forbidden 에러가 나야 한다.

- 해당 페이지가 외부로 노출되어 있지 않기 때문 -> 따라서 웹서버에 접속하기 위해 public으로 접근을 허용해야 한다.

![image-20210226094127834](210226_.assets/image-20210226094127834.png)

![image-20210226094149768](210226_.assets/image-20210226094149768.png)
<br>
3. 객체 탭 > 모든 html 파일을 퍼블릭으로 설정 (버킷에 등록된 객체에 퍼블릭 접근이 가능하도록)

![image-20210226094306818](210226_.assets/image-20210226094306818.png)
<br>
다시 버킷 웹 사이트 엔드포인트 링크 클릭 > 엔드포인트 링크 접속 가능 확인

![image-20210226102406564](210226_.assets/image-20210226102406564.png)
<br><br>
### S3 Bucket을 위한 DNS 레코드 구성

> **DNS 레코드**
>
> - DNS 서버 명령
> - 도메인에 연계된 IP주소와 해당 도메인에 대한 요청의 처리 방법에 대한 정보 제공
> - A 레코드 : 도메인의 ip 주소를 가지고 있는 레코드
>
> 버킷 웹 사이트 엔드포인트 (http://cmcloudlab912.info.s3-website-us-east-1.amazonaws.com/)는 이용하기에 복잡하고 불편함
> <br>
>
> 1. route 53 > 호스팅 영역 > 레코드 생성  > 마법사로 전환 클릭

- 라우팅 정책 : 단순 라우팅
- 단순 레코드 정의 클릭
- 값/트래픽 라우팅 대상 : s3 웹 사이트 엔드포인트에 대한 별칭
- 리전 : 미국 동부 (버지니아 북부) us-east-1
- 버킷 : 생성한 버킷 자동 선택 

![image-20210226100006066](210226_.assets/image-20210226100006066.png)
<br>
모든 과정이 끝나면 레코드 생성 버튼 눌러 최종적으로 레코드가 생성되었는지 확인한다.

![image-20210226100138511](210226_.assets/image-20210226100138511.png)
<br>
2. 버킷 이름으로도 웹서버 접속이 가능한지 확인

![image-20210226102701853](210226_.assets/image-20210226102701853.png)
<br><br>
### Redirect S3 Bucket (www) 생성
1. S3 > 버킷 > 버킷 만들기 클릭 

- 버킷 이름 : www.cmcloudlab912.info (www.[버킷이름])
- 리전 : 미국 동부 (버지니아 북부) us-east-1
- 모든 퍼브릭 액세스 차단 체크 해제

![image-20210226102832390](210226_.assets/image-20210226102832390.png)
<br>
2. S3 > 버킷 > 방금 생성한 버킷 클릭 > 속성 탭 > 정적 웹 사이트 호스팅 편집 

- 정적 웹 사이트 호스팅 : 활성화
- 호스팅 유형 : **객체에 대한 리디렉션**
- 호스트 이름 : 버킷 이름

![image-20210226103033474](210226_.assets/image-20210226103033474.png)
<br><br>
### Redirect S3 Bucket을 위한 DNS 레코드 구성
1. Route 53 > 호스팅 영역 > 레코드 생성 > 단순 라우팅 > 단순 레코드 정의 클릭

- 레코드 이름 : www 추가
- 값/트래픽 라우팅 대상은 기존과 동일하게 적용

![image-20210226103409104](210226_.assets/image-20210226103409104.png)
<br>

2. www.cmcloudlab912.info 주소로도 접속 가능 확인 (**cmcloudlab912.info 로 리다이렉트** 된다)

![image-20210226103716116](210226_.assets/image-20210226103716116.png)

<br>

<br>

# Creating Amazon S3 Buckets, Managing Objects, and Enabling Versioning

### Create Public Bucket

1. S3 > 버킷 만들기

- 버킷 이름 : lapublic13
- 모든 퍼블릭 액세스 차단 체크 해제

![image-20210226131855879](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226131855879.png)

### Create Private Bucket

1. S3 > 버킷 만들기

- 버킷 이름 : laprivate13
- 모든 퍼블랙 액세스 차단 체크

![image-20210226132049416](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226132049416.png)

### Create a Folder and Upload File in Public Bucket

### Upload File to Private Bucket



# Creating a basic VPC and Associated Components

### 개념정리

**Region**

- AWS 서비스가 운영되는 지역
- 복수 개의 데이터 센터들의 집합

**가용 영역 (AZ)**

- 리전 내에 위치한 데이터센터
- 물리적으로 분리되어 있음 -> 고가용성 보장하기 위해

**VPC (Virtual Private Cloud)**

- AWS 계정 전용 가상 네트워크
- 한 AWS 리전 안에서만 존재할 수 있고, 한 리전에 만든 VPC는 다른 리전에서 보이지 않음

- 연속적인 IP 주소 범위로 구성 -> CIDR 블록으로 표시
  - 10.0.0.0/8 		-> 10.0.0.0 ~ 10.255.255.255 
  - 172.16.0.0/12  -> 172.16.0.0 ~ 172.31.255.255
  - 192.168.0.0/16 -> 192.168.0.0 ~ 192.168.255.255

**서브넷 (Subnet)**

- VPC 내 논리적으로 묶인 컨테이너
- EC2 인스턴스를 배치하는 장소 -> 인스턴스는 서브넷 안에 위치해야 한다
  - 서브넷에 인스턴스를 생성하면 다른 서브넷으로 이동 불가
  - 인스턴스를 종료하고 다른 서브넷에 새 인스턴스 생성
- 인스턴스를 서로 격리하고, 인스턴스 간의 트래픽 흐름을 제어하고, 인스턴스를 기능 별로 묶을 수 있음
- 서브넷 CIDR 블록 
  - VPC의 일부, VPC 내에서는 유일(unique)해야 함
  - 모든 서브넷에서 처음 4개의 IP와 마지막 1개는 예약되어 있으므로 인스턴스에 할당 불가
    - 서브넷 CIDR : 171.16.100.0/24인 경우 -> 172.16.100.0 ~ 172.16.100.3과 172.16.100.255 사용 불가
- **서브넷은 하나의 가용 영역 내에서만 존재**

**ENI (Elastic Network Interface)**

- 물리 서버의 NIC (Network Interface Controller)와 같은 기능 수행
- 모든 인스턴스에는 기본 ENI가 존재, 이 인터페이스는 하나의 서브넷에만 연결

**IGW (Internet Gateway)**

- 게이트웨이 : 다른 네트워크로 나가는 통로
- 퍼블릭 IP 주소를 할당받은 인스턴스가 인터넷과 연결되어서 인터넷으로부터 요청을 수신할 수 있도록 해주는 서비스
- 처음 VPC를 생성하더라도 IGW가 연결되지는 않음 -> 즉, 직접 IGW를 생성하고 VPC와 연결해야 함
- VPC는 하나의 IGW만 연결 가능 -> VPC내의 인스턴스는 하나의 IGW를 통해서만 통신

**라우팅 테이블**

- VPC는 소프트웨어 함수로 IP 라우팅을 구현한 라우터를 제공 -> 즉, 사용자는 라우팅 테이블만 관리하면 된다.
- 라우팅 테이블은 하나 이상의 라우팅과 하나 이상의 서브넷 연결로 구성되어 있다.
- VPC를 생성하면 기본 라우팅 테이블을 자동으로 만들고 해당 VPC에 모든 서브넷과 연결

**라우팅**

- 라우팅 테이블과 연결된 서브넷 내 인스턴스에서 트래픽을 전달하는 방법을 결정
- 라우팅 테이블에는 같은 VPC에 있는 인스턴스 간에 통신할 수 있게 하는 **로컬 라우팅**이 필수적으로 포함
- **기본 라우팅** 
  - 인스턴스가 인터넷에 액세스하게 하려면 IGW를 가리키는 기본 라우팅을 생성해야 함
    - 대상(target) 주소: 0.0.0.0/0	-> 인터넷 상의 모든 호스트 IP 주소
    - 대상 : igw-xxxx....
- **퍼블릿 서브넷** : IGW를 가리키는 기본 라우팅이 포함된 라우팅 테이블과 연결된 서브넷

- **프라이빗 서브넷 ** : 기본 라우팅이 포함되어 있지 않음

- 라우팅을 결정할 때는 가장 근접하게 일치하는 항목을 기반으로 라우팅 

  - 대상 주소: 172.31.0.0/16		대상: LOCAL

  - 대상 주소 : 0.0.0.0/0               대상 : igx-xxxx....

    위와 같은 상황이라면, 198.51.100.50으로 패킷을 보내려고 하면 가장 근접한 igx-xxxx...로 패킷 전달

    마찬가지로, 172.31.0.10으로 패킷을 보내려고 하면 가장 근접한 172.31.0.10 으로 패킷 전달

**보안 그룹 (Security Group)**

- 방화벽과 같은 기능 제공
  - 상태 저장 방화벽 역할
  - 보안 그룹이 트래픽을 한 방향으로 전달되도록 허용할 때 반대 방향의 응답 트래픽을 지능적으로 허용

- 인스턴스의 ENI에서 송수신되는 트래픽을 허가해서 인스턴스를 오가는 트래픽을 제어
- 모든 ENI는 최소 하나 이상의 보안 그룹과 연결되어야 함
  - 보안 그룹과 ENI는 N:N 관계 
- 보안 그룹 생성 시 보안 그룹 이름, 설명, 포함될 VPC 지정하며 보안 그룹 생성 후 인바운드 및 아웃바운드 규칙 생성하여 트래픽 통제

**NACL (Network Access Control List)**

- 보안 그룹과 유사
  - 원본(source) / 대상(target) 주소 CIDR, 프로토콜, 포트를 기반으로 트래픽 허용하는 아웃바운드, 인바운드 규칙 포함 -> 방화벽 기능
  - VPC에는 삭제할 수 없는 기본 NACL 존재
- NACL은 ENI가 아닌 서브넷에 연결, 해당 서브넷과 송수신하는 트래픽 제어
  - 서브넷 내의 인스턴스 간 트래픽 제어할 때는 NACL 사용 불가 -> 보안 그룹
- NACL은 상태 저장 안함 -> NACL은 통과하는 연결 상태를 추적하지 않음
  - 모든 인바운드, 아웃바운드 트래픽의 허용 규칙을 별도로 작성해야 함

- NACL 규칙은 **규칙 번호**의 오름차순으로 처리

<br>

### Lab 구성도

![image-20210226154153747](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226154153747.png){:width="200" height="400"}

<br>

### Create a VPC

1. VPC -> VPC 생성 

- 이름 : VPC1
- IPv4 CIDR : 172.16.0.0/16

![image-20210226142944039](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226142944039.png)

<br>

### Create Public Subnet

1. VPC -> 서브넷  -> 서브넷 생성

- VPC ID : VPC1
- 서브넷 이름 : Public1
-  가용 영역 : us-east-1a
- IPv4 CIDR : 172.16.1.0/24

![image-20210226143120014](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143120014.png)

<br>

### Create Private Subnet

1. VPC -> 서브넷  -> 서브넷 생성

- VPC ID : VPC1
- 서브넷 이름 : Private1
-  가용 영역 : us-east-1b
- IPv4 CIDR : 172.16.2.0/24

![image-20210226150525614](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226150525614.png)

<br>

### Create and Configure Public NACL

1. VPC > 네트워크 ACL > 네트워크 ACL 생성

- 이름 : Public_NACL
- VPC : VPC1

![image-20210226143420213](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143420213.png)
<br>
2. 생성한 NACL 선택 > 인바운드 규칙 편집 

![image-20210226143548406](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143548406.png)
<br>
생성한 NACL 선택 > 아웃바운드 규칙 편집

![image-20210226143627628](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143627628.png)
<br>
3. 서브넷 연결 편집 > Public1 서브넷을 선택하여 변경 사항 저장 클릭

![image-20210226143716700](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143716700.png)
<br>
### Create and Configure Private NACL

1. VPC > 네트워크 ACL > 네트워크 ACL 생성

- 이름 : Private_NACL
- VPC : VPC1

![image-20210226143828750](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143828750.png)
<br>
2. 생성한 NACL 선택 > 인바운드 규칙 편집 

![image-20210226143932472](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226143932472.png)
<br>
생성한 NACL 선택 > 아웃바운드 규칙 편집

![image-20210226144010128](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144010128.png) 
<br>
3. 서브넷 연결 편집 > Private1 서브넷을 선택하여 변경 사항 저장 클릭

![image-20210226144107650](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144107650.png)
<br>

### Create an Internet Gateway, and Connect It to the VPC

1. VPC > 인터넷 게이트웨이 > 인터넷 게이트웨이 생성

- 이름 : IGW

![image-20210226144232500](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144232500.png)
<br>

2. 작업 > VPC에 연결 > VPC1 선택

![image-20210226144332045](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144332045.png)
<br>
### Create and Configure Public Route Table

1. 라우팅 테이블 > 라우팅 테이블 생성

- 이름 : PublicRT
- VPC : VPC1

![image-20210226144441732](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144441732.png)
<br>

2. 라우팅 탭 > 라우팅 편집 > 라우팅 저장

- Destination : 0.0.0.0/0 (불특정 호스트로 )
- Target : IGW

![image-20210226144613500](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144613500.png)
<br>
3. 서브넷 연결 탭 > 서브넷 연결 편집 > Public1 서브넷 선택
<br>
### Create and Configure Private Route Table

1. 라우팅 테이블 > 라우팅 테이블 생성

- 이름 : PrivateRT
- VPC : VPC1

![image-20210226144816796](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144816796.png)
<br>

2. 서브넷 연결 탭 > 서브넷 연결 편집 > Private1 서브넷 선택

![image-20210226144921562](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226144921562.png)



<br>

<br>

# Building a Three-Tier Network VPC from Scratch in AWS

### Lab 구성도

![image-20210226163904221](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163904221.png){: width="200" height="400"}

<br>

### Build and Configure a VPC, Subnets, and Internet Gateway

1. VPC 생성

![image-20210226161842519](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226161842519.png)
<br>
2. Subnet (DMZ layer) 생성 -> **가용성 보장을 위해 레이어 별로 서브넷 생성**

- x.x.**1/2**.x : DMZ layer
- x.x.**10~19**.x : App layer
- x.x.**20~29**.x : DB layer

![image-20210226161943281](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226161943281.png)

![image-20210226162017064](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162017064.png)
<br>
3. Subnet (app layer) 생성

![image-20210226162126855](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162126855.png)

![image-20210226162213298](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162213298.png)
<br>
4. Subnet (database layer) 생성

![image-20210226162258575](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162258575.png)

![image-20210226162327059](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162327059.png)
<br>
5. 인터넷 게이트웨이 생성

![image-20210226162456820](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162456820.png)
<br>
IGW 인터넷 게이트웨이를 앞서 생성한 SysOps VPC에 연결한다.

![image-20210226162528821](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162528821.png)

<br>

### Build and Configure a NAT Gateway, Route Tables, and NACLs

1. NAT 게이트웨이 생성

- 서브넷 : DMZ2public (**아직 라우팅 테이블에 연결하지 않아 퍼블릿 서브넷이 아니지만, 곧 연결할 예정이므로 일단 연결해준다**)
- 탄력적 IP 할당 버튼 클릭하여 **새로운 EIP 할당 받기** (NAT Gateway는 EIP를 필요로 함)

![image-20210226162739129](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162739129.png)
<br>
2. 라우팅 테이블 생성 (퍼블릭, 프라이빗)

![image-20210226162854864](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162854864.png)

![image-20210226162912358](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226162912358.png)
<br>
3. PublicRT 선택 > 라우팅 편집 (아래처럼)

- target : local -> VPC 내의 모든 서브넷과 통신 가능
- 모든 요청에 대해 IGW로 갈 수 있도록 라우팅 추가해주기

![image-20210226163042053](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163042053.png)
<br>
4. PrivateRT 선택 > 라우팅 편집

- 외부로 나가도 되지 않기 때문에 IGW 라우팅 추가 안함

![image-20210226163141197](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163141197.png)
<br>
5. PublicRT 선택 > 서브넷 연결 편집 (DMZ1, DMZ2 선택)

![image-20210226163234319](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163234319.png)
<br>
6. PrivateRT 선택 > 서브넷 연결 편집 (4개의 private 서브넷 선택)

![image-20210226163343017](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163343017.png)
<br>
7. NACL 생성

![image-20210226163447613](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163447613.png)

![image-20210226163510306](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163510306.png)

![image-20210226163525891](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163525891.png)
<br>
8. DMZNACL 선택 > 서브넷 연결 편집 (DMZ layer 서브넷 연결)

![image-20210226163620943](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163620943.png)
<br>
AppZNACL 선택 > 서브넷 연결 편집 (App layer 서브넷 연결)

![image-20210226163711647](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163711647.png)
<br>
DBNACL 선택 > 서브넷 연결 편집 (DBlayer 서브넷 연결)

![image-20210226163747062](210226_S3_Static_Web_Hosting, Create_VPC.assets/image-20210226163747062.png)

<br>

### NACL에 인바운드, 아웃바운드 규칙 추가 ->해당 서브넷에서 제공하는 서비스와 관리를 위한 서비스 (SSH, 22) 고려

DMZ*public ⇒ 웹 서버 (80) 

AppLayer*private ⇒ express.js (3000)

DBLayer*private ⇒ MySQL (3306)

