### git command

> git을 사용하기 위한 기본 명령어





#### 설정

###### 1. init

- `git init`
- 현재 폴더를 `git`으로 관리 하겠다는 의미 > `.git` 폴더를 생성한다.
- 최초에 한 번만 실행하는 명령어



###### 2. config

- `git config --global user.email "username@email"`
- `--global`옵션과 `--local` 둘 중 하나 선택해서 사용
  - 일반적으로 global 설정을 해놓으면 내 컴퓨터에서 추가적으로 변경할 일이 없다.



###### 3. status

- `git status`
- 현재 git의 상태를 출력해주는 명령어



###### 4. diff

- `git diff`
- **마지막 commit**과 **현재 폴더** 상태를 비교해서 차이점을 출력해준다.



###### 5. log

- `git log`
- Commit History를 출력해준다.



###### 6. remote add

- `git remote add origin <url>`
- 원격저장소를 추가하는데 별명은 'origin'이고 실제주소는 <url>이다.

- 원격저장소 주소를 저장한다.





#### 저장

###### 1. add

- `git add <추가하려고 하는 파일>`
  - `git add .` : 한 번에 모든 파일과 폴더를 add 할 수 있다.
- `working directory`에서 변경점을 `staging area`로 이동한다.



###### 2. commit

- `git commit -m "메세지"` : 한 번에 메세지까지 남김



###### 3. push

- `git push origin master`
- 원격저장소에 master 브랜치의 데이터를 전송



