**프로비저닝** : 사용자의 요구에 맞게 시스템 자원을 할당, 배치, 배포해 두었다가 필요 시 시스템을 즉시 사용할 수 있는 상태로 미리 준비해 두는 것<br>
: 서버 자원 프로비저닝, OS 프로비저닝(Vagrant), SW 프로비저닝, 스토리지 프로비저닝 등이 있으며 Kops 도 프로비저닝 툴이라고 볼 수 있다.<br>

**IoC** : Infrastructure of Code > 코드를 기반으로 인프라 관리

**Microservice**: 하나의 큰 덩어리로 만들었던 애플리케이션을 작은 단위의 서비스로 나누어 관리

---------

# Ansible

**Configuration Management Tools**

- Linux 설치 시 Python 2.7 버전이 자동으로 설치되는데, python을 기본으로 하는 Ansible은 linux 사용 시 별도로 설치할 필요가 없다.
- 하지만 Windows에는 linux가 없기 때문에 python 별도로 설치 필요
- DSL (Domain Specific Language) : 도메인에 특화되어 있는 언어
- Agent 필요 : 마스터 노드가 다른 노드에 어떤 명령을 내릴 때 Agent를 통해 작업하는 경우 

![image](https://user-images.githubusercontent.com/77096463/112560910-7b5cbf80-8e17-11eb-84e3-2914427c5294.png)

<br>

### 1. vagrant로 ansible 실행 - 기본 환경 설정

새로운 디렉터리 생성 후 vagrant 프로비저닝 예제 스크립트 실행

```
PS C:\cloud> mkdir ansible
PS C:\cloud> cd .\ansible\

PS C:\cloud\ansible> vagrant init
A `Vagrantfile` has been placed in this directory. You are now
ready to `vagrant up` your first virtual environment! Please read
the comments in the Vagrantfile as well as documentation on
`vagrantup.com` for more information on using Vagrant.
```

 <br>

Vagrantfile 파일 내용 변경 & Vagrantfile 반영하여 프로비저닝 진행

- 만일 기존 vagrant 삭제하려면 `vagrant destroy`

```
Vagrant.configure("2") do |config|
  config.vm.define:"ansible-server" do |cfg|
    cfg.vm.box = "centos/7"
    cfg.vm.provider:virtualbox do |vb|
        vb.name="Ansible-Server"
        vb.customize ["modifyvm", :id, "--cpus", 2]
        vb.customize ["modifyvm", :id, "--memory", 2048]
    end
    cfg.vm.host_name="ansible-server"
    cfg.vm.synced_folder ".", "/vagrant", disabled: true
    cfg.vm.network "public_network", ip: "172.20.10.10"
    cfg.vm.network "forwarded_port", guest: 22, host: 19210, auto_correct: false, id: "ssh"
    cfg.vm.network "forwarded_port", guest: 8080, host: 58080
    # cfg.vm.network "forwarded_port", guest: 9000, host: 59000
    # cfg.vm.provision "shell", path: "bootstrap.sh"  
    # cfg.vm.provision "file", source: "Ansible_env_ready.yml", destination: "Ansible_env_ready.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_env_ready.yml"
    # cfg.vm.provision "shell", path: "add_ssh_auth.sh", privileged: false

    # cfg.vm.provision "file", source: "Ansible_ssh_conf_4_CentOS.yml", destination: "Ansible_ssh_conf_4_CentOS.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_ssh_conf_4_CentOS.yml"
  end
end
```

```
PS C:\cloud\ansible> vagrant up
...
1) Intel(R) Wireless-AC 9560 160MHz
2) Hyper-V Virtual Ethernet Adapter
==> ansible-server: When choosing an interface, it is usually the one that is
==> ansible-server: being used to connect to the internet.
==> ansible-server:
    ansible-server: Which interface should the network bridge to? 1
    ...
```

<br>

vagrant 상태 확인

```
PS C:\cloud\ansible> vagrant status
Current machine states:

ansible-server            running (virtualbox)
```

<br>

ansible-server 리눅스로 접속

- [vagrant@**ansible-server** ~] : Vagrantfile에서 도메인 이름은 ansible-server로 설정함

```
PS C:\cloud\ansible> vagrant ssh ansible-server
[vagrant@ansible-server ~]$
```

<br>

### 2. 필요 모듈 설치

net-tools 설치

```
[vagrant@ansible-server ~]$ sudo yum install -y net-tools
```

