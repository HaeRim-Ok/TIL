프로비저닝** : 사용자의 요구에 맞게 시스템 자원을 할당, 배치, 배포해 두었다가 필요 시 시스템을 즉시 사용할 수 있는 상태로 미리 준비해 두는 것<br>
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

**실습 환경 구성**

![image](https://user-images.githubusercontent.com/77096463/112567523-515dca00-8e24-11eb-840e-07aff46b2586.png)

<br>

**ansible 활용하여 할 수 있는일 :**

- 설치 : apt-get, yum, homebrew 등
- 환경 설정 파일 및 스크립트 배포 : copy, template 등
- 다운로드 : get_url, git, subversion 등
- 실행 : shell, task

**ansible 결과** : ok / failed/ changed / unreachable

<br>

### 1. vagrant 기본 환경 설정

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

### 2. 필요 모듈 설치 & 자동화 작업

net-tools 설치

```
[vagrant@ansible-server ~]$ sudo yum install -y net-tools
```

<br>

리눅스 확장 패키지 설치

```
[vagrant@ansible-server ~]$ sudo yum install -y epel-release
```

<br>

Ansible Core 설치 & 설치 후 버전 확인

```
[vagrant@ansible-server ~]$ sudo yum install -y ansible

[vagrant@ansible-server ~]$ ansible --version
ansible 2.9.18
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/vagrant/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.5 (default, Apr  2 2020, 13:16:51) [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)]
```

<br>

만일 새로운 리눅스를 또 설치하려면 ansible, 리눅스 확장 패키지를 재설치해야하므로 이 절차를 간소화하기 위해 **자동화 작업**

- 만일 vagrant 실행 중이라면 `vagrant halt`

- Vagrantfile의 `cfg.vm.provision "shell", path: "bootstrap.sh"` 주석 해제 > **vagrant가 linux를 실행할 때 bootstrap.sh 파일을 자동 실행하여 필요한 패키지 설치**

```
#Vagrantfile
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
    cfg.vm.provision "shell", path: "bootstrap.sh"  
    # cfg.vm.provision "file", source: "Ansible_env_ready.yml", destination: "Ansible_env_ready.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_env_ready.yml"
    # cfg.vm.provision "shell", path: "add_ssh_auth.sh", privileged: false

    # cfg.vm.provision "file", source: "Ansible_ssh_conf_4_CentOS.yml", destination: "Ansible_ssh_conf_4_CentOS.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_ssh_conf_4_CentOS.yml"
  end
end
```

```sh
#bootstrap.sh

# ! /usr/bin/env bash

yum install -y epel-release
yum install -y ansible
```

<br>

이후 다시 ansible-server 실행

```
PS C:\cloud\ansible> vagrant up
PS C:\cloud\ansible> vagrant ssh ansible-server
```

<br>

### 3. ansible-node 구축

Vagrantfile에 ansible-node01 코드 추가

- bash_ssh_conf_4_CentOs.sh 파일 생성

```
Vagrant.configure("2") do |config|
  config.vm.define:"ansible-node01" do |cfg|
    cfg.vm.box = "centos/7"
    cfg.vm.provider:virtualbox do |vb|
        vb.name="Ansible-Node01"
        vb.customize ["modifyvm", :id, "--cpus", 1]
        vb.customize ["modifyvm", :id, "--memory", 1024]
    end
    cfg.vm.host_name="ansible-node01"
    cfg.vm.synced_folder ".", "/vagrant", disabled: false
    cfg.vm.network "public_network", ip: "172.20.10.11"
    cfg.vm.network "forwarded_port", guest: 22, host: 19211, auto_correct: false, id: "ssh"
    cfg.vm.network "forwarded_port", guest: 80, host: 10080
    cfg.vm.provision "shell", path: "bash_ssh_conf_4_CentOs.sh"
  end

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
    cfg.vm.provision "shell", path: "bootstrap.sh"  
    # cfg.vm.provision "file", source: "Ansible_env_ready.yml", destination: "Ansible_env_ready.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_env_ready.yml"
    # cfg.vm.provision "shell", path: "add_ssh_auth.sh", privileged: false

    # cfg.vm.provision "file", source: "Ansible_ssh_conf_4_CentOS.yml", destination: "Ansible_ssh_conf_4_CentOS.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_ssh_conf_4_CentOS.yml"
  end
end
```

```sh
#bash_ssh_conf_4_CentOs.sh

#! /usr/bin/env bash

now=$(date +"%m_%d_%Y")
cp /etc/ssh/sshd_config /etc/ssh/sshd_config_$now.backup
sed -i -e 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
systemctl restart sshd
```

<br>

ansible-node01 프로비저닝 진행

```
PS C:\cloud\ansible> vagrant up ansible-node01
Current machine states:

ansible-node01            running (virtualbox)
ansible-server            running (virtualbox)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```

<br>

서로의 ip에 ping 테스트

![image](https://user-images.githubusercontent.com/77096463/112570302-23c74f80-8e29-11eb-987b-facdb5896f57.png)

<br>

ansible-server 호스트에서 /etc/ansible/hosts 파일 하위에 아래 내용 추가

```
[vagrant@ansible-server ~]$ sudo vi /etc/ansible/hosts
```

```
[nginx]
172.20.10.11
```

<br>

마찬가지로 Vagrantfile에 ansible-node02 코드 추가

```
Vagrant.configure("2") do |config|
  config.vm.define:"ansible-node01" do |cfg|
    cfg.vm.box = "centos/7"
    cfg.vm.provider:virtualbox do |vb|
        vb.name="Ansible-Node01"
        vb.customize ["modifyvm", :id, "--cpus", 1]
        vb.customize ["modifyvm", :id, "--memory", 1024]
    end
    cfg.vm.host_name="ansible-node01"
    cfg.vm.synced_folder ".", "/vagrant", disabled: false
    cfg.vm.network "public_network", ip: "172.20.10.11"
    cfg.vm.network "forwarded_port", guest: 22, host: 19211, auto_correct: false, id: "ssh"
    cfg.vm.network "forwarded_port", guest: 80, host: 10080
    cfg.vm.provision "shell", path: "bash_ssh_conf_4_CentOs.sh"
  end

  config.vm.define:"ansible-node02" do |cfg|
    cfg.vm.box = "centos/7"
    cfg.vm.provider:virtualbox do |vb|
        vb.name="Ansible-Node02"
        vb.customize ["modifyvm", :id, "--cpus", 1]
        vb.customize ["modifyvm", :id, "--memory", 1024]
    end
    cfg.vm.host_name="ansible-node02"
    cfg.vm.synced_folder ".", "/vagrant", disabled: false
    cfg.vm.network "public_network", ip: "172.20.10.12"
    cfg.vm.network "forwarded_port", guest: 22, host: 19212, auto_correct: false, id: "ssh"
    cfg.vm.network "forwarded_port", guest: 80, host: 20080
    cfg.vm.provision "shell", path: "bash_ssh_conf_4_CentOs.sh"
  end

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
    cfg.vm.provision "shell", path: "bootstrap.sh"  
    # cfg.vm.provision "file", source: "Ansible_env_ready.yml", destination: "Ansible_env_ready.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_env_ready.yml"
    # cfg.vm.provision "shell", path: "add_ssh_auth.sh", privileged: false

    # cfg.vm.provision "file", source: "Ansible_ssh_conf_4_CentOS.yml", destination: "Ansible_ssh_conf_4_CentOS.yml"
    # cfg.vm.provision "shell", inline: "ansible-playbook Ansible_ssh_conf_4_CentOS.yml"
  end
end
```

<br>

ansible-node02 프로비저닝 진행

```
PS C:\cloud\ansible> vagrant up ansible-node02

PS C:\cloud\ansible> vagrant status
Current machine states:

ansible-node01            running (virtualbox)
ansible-node02            running (virtualbox)
ansible-server            running (virtualbox)

This environment represents multiple VMs. The VMs are all listed
above with their current state. For more information about a specific
VM, run `vagrant status NAME`.
```

<br>

**:rotating_light: xshell로 ansible-server, ansible-node 접속 방법**

1. [연결 탭] 이름 : ansible-node01 / 호스트 : 127.0.0.1 / 포트 번호 : vagrant에 지정된 포트 입력 (19211)

![image](https://user-images.githubusercontent.com/77096463/112576232-3fd0ee00-8e35-11eb-8756-2020a373f74d.png)

<br>

2. [사용자 인증 탭] 사용자 이름 : vagrant / 방법 : Public Key 

-> C:\cloud\ansible\.vagrant\machines\ansible-node01\virtualbox 경로의 private_key 선택

![image](https://user-images.githubusercontent.com/77096463/112576315-642cca80-8e35-11eb-8533-eca414831d02.png)

<br>

### 4. 