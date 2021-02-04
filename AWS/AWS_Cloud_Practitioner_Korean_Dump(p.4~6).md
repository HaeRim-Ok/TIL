# AWS Cloud Practitioner Dump (p.4~6)

31. AWS는 Identity and Access Management (IAM) 사용자에게 보안을 추가하기 위해 다음 방법 중 어떤 것을 지원합니까? (2 개 선택)

    A. Amazon Rekognition 구현

    B. AWS Shield 보호 리소스 사용

    C. 보안 그룹으로 액세스 차단

    **D. MFA (Multi-Factor Authentication) 사용**

    **E. 암호 강도 및 만료 적용**

 IAM 모범 사례 
-사용자를위한 강력한 암호 정책 구성-사용자가 자신의 암호를 변경할 수 있도록 허용하는 경우 강력한 암호를 생성하고 정기적으로 암호를 교체하도록 요구합니다. 
-MFA 참조 활성화 : https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

<br/>

32. 지속적으로 변화하는 데이터의 읽기 / 쓰기에 어떤 AWS 서비스를 사용해야합니까? (2 개 선택)

    A. Amazon Glacier

    **B. Amazon RDS**

    C. AWS Snowball

    D. Amazon Redshift

    **E. Amazon EFS**

매우 자주 업데이트해야하는 데이터는 Amazon EBS 볼륨, Amazon RDS, Amazon DynamoDB, Amazon EFS 또는 Amazon EC2에서 실행되는 관계형 데이터베이스와 같은 읽기 및 쓰기 지연 시간을 고려하는 스토리지 솔루션에서 더 잘 제공 될 수 있습니다. 

<br/>

33. Amazon Relational Database Service (Amazon RDS)의 장점 중 하나는 무엇입니까?

    **A. 관계형 데이터베이스 관리 작업을 단순화합니다.**

    B. 99.99999999999 %의 신뢰성과 내구성을 제공합니다.

    C. 로드를 위해 데이터베이스를 자동으로 확장합니다.

    D. 사용자가 CPU 및 RAM 리소스를 동적으로 조정할 수 있습니다.

RDS를 사용하면 클라우드에서 관계형 데이터베이스를 쉽게 설정, 운영 및 확장 할 수 있습니다. 비용 효율적이고 크기 조정이 가능한 용량을 제공하는 동시에 시간을 자동화합니다. 

<br/>

34. 고객은 쉽게 확장 할 수있는 MySQL 데이터베이스를 실행해야합니다.
    어떤 AWS 서비스를 사용해야합니까?

    **A. Amazon Aurora**

    B. Amazon Redshift

    C. Amazon DynamoDB

    D. Amazon ElastiCache

Amazon Aurora는 클라우드 용으로 구축 된 MySQL 및 PostgreSQL 호환 관계형 데이터베이스로, 기존 엔터프라이즈 데이터베이스의 성능 및 가용성과 오픈 소스 데이터베이스의 단순성 및 비용 효율성을 결합합니다.

<br/>

35. 지연 시간이 짧은 링크를 통해 상호 연결된 하나 이상의 개별 데이터 센터로 구성된 AWS 글로벌 인프라의 다음 구성 요소는 무엇입니까?

    **A. 가용 영역**

    B. 가장자리 위치

    C. 지역

    D. 사설 네트워킹

가용 영역 (AZ)은 AWS 리전에서 중복 전원, 네트워킹 및 연결이있는 하나 이상의 개별 데이터 센터입니다. 각 가용 영역은 격리되어 있지만 한 리전의 가용 영역은 지연 시간이 짧은 링크를 통해 연결됩니다.

<br/>

36. 다음 중 고객과 AWS 간의 공유 제어는 무엇입니까?

    A. Amazon S3 클라이언트 측 암호화를 위한 키 제공

    B. Amazon EC2 인스턴스 구성

    C. 물리적 AWS 데이터 센터의 환경 제어

    **D. 인식 및 훈련**

Amazon Elastic Compute Cloud (Amazon EC2)와 같은 서비스는 IaaS (Infrastructure as a Service)로 분류되므로 고객이 필요한 모든 보안 구성 및 관리 작업을 수행해야합니다. Amazon EC2 인스턴스를 배포하는 고객은 게스트 운영 체제 (업데이트 및 보안 패치 포함), 인스턴스에 고객이 설치 한 애플리케이션 소프트웨어 또는 유틸리티, AWS 제공 방화벽 구성 (보안이라고 함)을 관리 할 책임이 있습니다.

인식 및 교육 - AWS는 AWS 직원을 교육하지만 고객은 자신의 직원을 교육해야합니다. 

<br/>

37. 고 가용성을 달성하기 위해 컴퓨팅 리소스를 프로비저닝해야하는 가용 영역은 몇 개입니까?

    A. 최소 1 개

    **B. 최소 2 개**

    C. 최소 3 개

    D. 최소 4 개 이상

<br/>

38. 온 프레미스 데이터 센터에서 AWS 클라우드로 인프라를 이동할 때의 이점 중 하나는 다음과 같습니다.

    A. 기업은 IT 비용을 없앨 수 있습니다.

    B. 기업은 각 고객의 데이터 센터에 서버를 배치 할 수 있습니다.

    **C. 비즈니스가 비즈니스 활동에 집중할 수 있습니다.**

    D. 기업이 서버를 패치하지 않은 상태로 둘 수 있습니다.

기업은 IT 비용을 없애는 것이 아닌, 감소시킬 수 있다.

<br/>

39. 즉각적인 검색을 위해 데이터베이스 백업을 보관하기위한 가장 저렴하고 내구성있는 스토리지 옵션은 무엇입니까?

    **A. Amazon S3**

    B. Amazon Glacier

    C. Amazon EBS

    D. Amazon EC2 인스턴스 스토어

Glacier는 즉각적인 검색이 아니라 다양한 검색 시간을 가지고 있습니다. 신속 3-5 분 표준 3-5 시간, 벌크 5-12 시간

<br/>

40. 개발자가 AWS CLI를 통해 AWS 서비스에 액세스 할 수있는 AWS IAM 기능은 무엇입니까?

    A. API 키

    **B. 액세스 키**

    C. 사용자 이름 / 암호

    D. SSH 키

액세스 키를 사용하여 AWS API 작업을 프로그래밍 방식으로 호출하거나 AWS CLI 명령을 사용합니다.

<br/>

41. 다음 중 빠르고 안정적인 NoSQL 데이터베이스 서비스는 무엇입니까?

    A. Amazon Redshift

    B. Amazon RDS

    **C. Amazon DynamoDB**

    D. Amazon S3

<br/>

42. AWS 클라우드에서 민첩성의 예는 무엇입니까?

    A. 여러 인스턴스 유형에 대한 액세스

    B. 관리 서비스에 대한 액세스

    C. 통합 결제를 사용하여 하나의 청구서 생성

    **D. 새로운 컴퓨팅 리소스에 대한 획득 시간 감소**

민첩성은 신속하고 저렴하게 변경할 수있는 능력을 "구축"하는 관행입니다. 클라우드는 이러한 다른 관행을 실용적으로 만들뿐만 아니라 자체적으로 민첩성을 제공합니다. 인프라는 몇 달이 아닌 몇 분 만에 프로비저닝 할 수 있으며 프로비저닝을 해제하거나 빠르게 변경할 수 있습니다.

<br/>

43. 고객이 여러 AWS 계정을 통합하고 중앙에서 관리하려면 어떤 서비스를 사용해야합니까?

    A. AWS IAM

    **B. AWS 조직**

    C. AWS 스키마 변환 도구

    D. AWS 구성

<br/>

44. AWS 아키텍처 원칙을 준수하는 많은 수의 개별 비디오 파일을 트랜스 코딩하는 방법은 무엇입니까?

    **A. 여러 인스턴스를 병렬로 사용**

    B. 사용량이 적은 시간에 하나의 대규모 인스턴스 사용

    C. 전용 하드웨어 사용

    D. 대형 GPU 인스턴스 유형 사용

스케일의 디자인 원칙과 수평으로 정렬되기 때문에 정확합니다.

<br/>

45. AWS는 어떤 감사 프로세스에 대해 단독 책임을지고 있습니까?

    A. AWS IAM 정책

    **B. 물리적 보안**

    C. Amazon S3 버킷 정책

    D. AWS CloudTrail 로그

AWS의 책임 "클라우드 보안"- AWS는 AWS 클라우드에서 제공되는 모든 서비스를 실행하는 인프라를 보호 할 책임이 있습니다. 이 인프라는 AWS 클라우드 서비스를 실행하는 하드웨어, 소프트웨어, 네트워킹 및 시설로 구성됩니다.

<br/>

46. AWS 클라우드의 어떤 기능이 모든 고객에게 짧은 지연 시간에 대한 국제 기업의 요구 사항을 지원합니까?

    A. 내결함성

    **B. 글로벌 범위**

    C. 종량제 가격

    D. 고 가용성

Global Reach는 Cloud-Front를 사용하는 다국적 기업을 지원할 것입니다.

<br/>

47. 다음 중 AWS 책임 분담 모델에서 고객의 책임은 무엇입니까?

    A. 기본 인프라 패치

    B. 물리적 보안

    **C. Amazon EC2 인스턴스 패치**

    D. 네트워크 인프라 패치

<br/>

48. 고객이 별도의 결제로 여러 AWS 계정을 사용하고 있습니다.
    고객은 AWS 리소스에 미치는 영향을 최소화하면서 볼륨 할인을 어떻게 활용할 수 있습니까?

    A. 하나의 글로벌 AWS 계정을 만들고 모든 AWS 리소스를 해당 계정으로 이동합니다.

    B. 3 년 예약 인스턴스 요금을 선불로 등록합니다.

    **C. AWS Organizations의 통합 결제 기능을 사용합니다.**

    D. 볼륨 할인을 받으려면 AWS Enterprise 지원 플랜에 가입하십시오.

<br/>

49. 다음 중 Amazon CloudWatch Logs의 기능은 무엇입니까? (2 개 선택)

    A. Amazon Simple Notification Service (Amazon SNS) 별 요약

    B. 무료 Amazon Elasticsearch Service 분석

    C. 무료 제공

    **D. 실시간 모니터링**

    **E. 조정 가능한 유지**

각 로그 그룹에 대한 보존 정책을 조정하거나 무기한 보존을 유지하거나 보존 기간을 선택할 수 있습니다. (10 년에서 하루 사이) 

구독을 사용하여 로그 이벤트의 실시간 피드에 액세스 할 수 있습니다.

<br/>

50. 다음 중 AWS 관리 형 DNS (Domain Name System) 웹 서비스는 무엇입니까?

    **A. Amazon Route 53**

    B. Amazon Neptune

    C. Amazon SageMaker

    D. Amazon Lightsail

<br/>

51. 고객이 새 애플리케이션을 배포 중이며 AWS 리전을 선택해야합니다.
    다음 중 고객의 결정에 영향을 미칠 수있는 요소는 무엇입니까? (2 개 선택)

    **A. 사용자에 대한 지연 시간 감소**

    B. 현지 언어로 된 애플리케이션 프레젠테이션

    **C. 데이터 주권 준수**

    D. 더운 기후에서의 냉각 비용

    E. 현장 방문을위한 고객 사무실까지의 거리

데이터 주권 준수를 통해 특정 지역을 선택해야한다는 점에서 C가 E보다 훨씬 더 정확합니다. 데이터 주권 준수는 A 국가 사람들의 데이터가 해당 국가에서 저장 및 관리되어야 함을 의미합니다. 이 경우 서비스를 제공 할 지역 이외의 지역에 대한 옵션이 없습니다.

<br/>

52. 정적 웹 사이트를 호스팅하기위한 저렴한 옵션으로 사용할 수있는 스토리지 서비스는 무엇입니까?

    A. Amazon Glacier

    B. Amazon DynamoDB

    C. Amazon Elastic File System (Amazon EFS)

    **D. Amazon Simple Storage Service (Amazon S3)**

<br/>

53. 최대 90 % 할인을 제공 할 수있는 Amazon EC2 인스턴스 요금 모델은 무엇입니까?

    A. 예약 인스턴스

    B. 주문형

    C. 전용 호스트

    **D. 스팟 인스턴스**

스팟 인스턴스 - 최대 90 % / 예약 인스턴스 - 최대 75 %

<br/>

54. AWS 공동 책임 모델에 따라 AWS 고객의 책임은 무엇입니까?

    A. 물리적 액세스 제어

    **B. 데이터 암호화**

    C. 저장 장치의 안전한 폐기

    D. 환경 위험 관리

<br/>

55. 다음 AWS 클라우드 서비스 중 고객 관리 형 관계형 데이터베이스를 실행하는 데 사용할 수있는 것은 무엇입니까?

    **A. Amazon EC2**

    B. 아마존 루트 53

    C. Amazon ElastiCache

    D. Amazon DynamoDB

Dynamo DB는 관계형 데이터베이스가 아닙니다.

<br/>

56. 한 회사에서 확장 가능한 데이터웨어 하우스 솔루션을 찾고 있습니다.
    다음 중 회사의 요구 사항을 충족하는 AWS 솔루션은 무엇입니까?

    A. Amazon Simple Storage Service (Amazon S3)

    B. Amazon DynamoDB

    C. Amazon Kinesis

    **D. Amazon Redshift**

<br/>

57. Elastic Load Balancing을 가장 잘 설명하는 문은 무엇입니까?

    A. DNS를 사용하여 도메인 이름을 IP 주소로 변환합니다.

    **B. 수신 애플리케이션 트래픽을 하나 이상의 Amazon EC2 인스턴스에 분산합니다.**

    C. 연결된 Amazon EC2 인스턴스에 대한 지표를 수집합니다.

    D. 수신 트래픽을 지원하기 위해 Amazon EC2 인스턴스 수를 자동으로 조정합니다.

ELB (Elastic Load Balancing)는 수신되는 애플리케이션 트래픽을 Amazon EC2 인스턴스, 컨테이너 및 IP 주소와 같은 여러 대상에 자동으로 분산합니다.

옵션 D는 로드 밸런싱이 아니라 AutoScaling과 관련이 있습니다.

<br/>

58. 다음 중 고객이 AWS 서비스와 상호 작용할 수있는 유효한 방법은 무엇입니까? (2 개 선택)

    **A. 명령 줄 인터페이스**

    B. 온-프레미스

    **C. 소프트웨어 개발 키트**

    D. SaaS (Software-as-a-Service)

    E. 하이브리드

<br/>

59. AWS 클라우드의 여러 리전은 다음과 같은 예입니다.

    A. 민첩성.

    **B. 글로벌 인프라.**

    C. 탄력성.

    D. 종량제 가격.

참조 문서는 다중 지역으로 진행할 때 민첩성에 대한 잠재적인 영향과 장애만을 언급합니다.

<br/>

60. 다음 중 지연 시간을 최소화하면서 대량의 온라인 비디오 콘텐츠를 제공하는 데 사용할 수있는 AWS 서비스는 무엇입니까? (2 개 선택)

    A. AWS 스토리지 게이트웨이

    **B. Amazon S3**

    C. Amazon Elastic File System (EFS)

    D. Amazon Glacier

    **E. Amazom CloudFront**

콘텐츠 호스팅에 S3를 사용하고 콘텐츠 전송 네트워크로 CloudFront를 사용합니다.

<br/>

<br/>

출처 : https://www.examtopics.com/exams

https://blog.naver.com/kroa/222224853064