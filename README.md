# khu_alarm
<STRONG>(2019 여름방학 개인 플젝)경희대 알라미 구현하기 </STRONG>

# 최종 목표

1. 공지사항 crwaling하여 db에 저장하기.
2. 공지사항 관리하기.
3. 웹서버 구축하기.
4. 앱을 통한 최신 공지사항 알림.

# 계획

## 1. 공지사항 crwaling하여 db에 저장하기.
목표 : 각종 공지사항 사이트를 crwaling하여 정보를 db에 저장하기.

- [x] [경희대 컴공과 공식 홈페이지](http://ce.khu.ac.kr/index.php?hCode=BOARD&bo_idx=2) 
- [x] [경희대 소프트웨어 융합학과 공식 홈페이지](http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01)
- [ ] [klas](www.klas.khu.ac.kr)
- [ ] [경희대 개인 메일함](https://mail.khu.ac.kr/) 

## 2. 관심 사이트 공지사항 몰아보기.

- [x] 전체 공지사항을 보여주는 DB 생성하기.
- [ ] CSS로 좀 꾸미기.
- [x] DB 데이터 역순으로 정렬하기.
- [x] DB에서 100개 이상의 데이터는 삭제
- [x] authentication 구현하기.(login, logout, sign up 기능 구현)
- [x] 개인 notice DB를 만들고, 이를 통해 사용자와 notice를 mapping한다.
- [x] user 개인을 위한 DB 생성하기 (전체 공지사항에서 선택해서 삽입)(자기 DB에서 삭제)
- [ ] settings.py에서 db 정보 감추기 구현하기. 
- [ ] 후에 db를 postgre로 바꾸기(현재 MYSQL) https://nachwon.github.io/database-mysql/

## 3. 웹서버 구축하기.

동방 server computer

- crwaling수행과 db제공

aws cloud

- 웹서버 역할을 수행

## 4. 앱을 통한 최신 공지사항 알림.
1) 웹을 통한 알림 기능 (html5 notification api)
2) 모바일 앱을 통한 알림 기능 (android notification api, cordoba <= html css js를 통해 모바일 앱 가능)


## 5. aws를 이용한 배포
### 1) ec2 운영체제 우분투 16.0.4

(sudo su 해주기 - sudo 안써도됨)

### 2) python3 버전 체크
python3 --version

### 3) pip3 설치

sudo apt-get update

sudo apt-get python3-pip

### 4) mysql 설치

sudo apt-get install mysql-server-5.7

비밀번호 설정할 때 : 1879

### 5) mysql 들어가서 database 만들기 

1) mysql 시작 : /etc/init.d/mysql start

2) mysql -p하고 비밀번호 입력

3) create database `khu_alarm`;

4) show databases;

5) exit;

### 6) mysql 한글 입력 설정 하기

my.cnf 파일 수정
client 부분밑에 추가
[client]
default-character-set = utf8
 
mysqld 부분밑에 추가
[mysqld]
init_connect = SET collation_connection = utf8_general_ci
init_connect = SET NAMES utf8
character-set-server = utf8
collation-server = utf8_general_ci
 
mysqldump 부분밑에 추가
[mysqldump]
default-character-set = utf8
 
mysql 부분밑에 추가
[mysql]
default-character-set = utf8

### 7) 가상환경 설치

pip3 install virtualenv

### 8) clone하기

git clone http://github.com/euidong/khu_alarm.git

### 9) 가상환경 실행

1) cd khu_alarm
2) virtualenv venv
3) source venv/bin/activate

### 10) 각종 모듈 설치
------서버용
pip3 install django
pip3 install djangorestframework
sudo apt-get install python3-dev libmysqlclient-dev gcc
pip3 install mysqlclient

-------크롤링용
pip3 install requests
pip3 install beautifulsoup4
pip3 install pymysql
pip3 install lxml

### 11) migration 적용하기 (db에 table만들기)
python3 manage.py migrate

### 12) crawling 실시 (추후에 람다로 전환하면 좋을 듯)

1) cd crawler
2) python3 khu_sw_crawler.py
3) python3 khu_ce_crawler.py

### 13) 서버 구동 (후에 아파치 연동으로 변경)

1) sudo apt-get install apache2
2) sudo apt-get install libapache2-mod-wsgi-py3 
3) wsgi.py  
import os, sys
from django.core.wsgi import get_wsgi_application
 
path = os.path.abspath(__file__+'/../..')
if path not in sys.path:
    sys.path.append(path)
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_letter.settings")
application = get_wsgi_application()
4) settings.py의 local host를 []에서 ['*']로 변환
5) 000-default.conf 수정
	
	(1) sudo vi /etc/apache2/sites-available/000-default.conf
	
	(2)아래 내용으로 수정 및 삽입

<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /home/ubuntu/khu_alarm

        WSGIDaemonProcess khu_alarm python-path=/home/ubuntu/khu_alarm/venv/lib/python3.5/site-packages
        WSGIProcessGroup khu_alarm
        WSGIScriptAlias / /home/ubuntu/khu_alarm/khu_alarm/wsgi.py
        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf

        Alias /static /home/ubuntu/khu_alarm/template
        <Directory /home/ubuntu/khu_alarm/template>
                Require all granted
        </Directory>
        Alias /khu_alarm /home/ubuntu/khu_alarm/khu_alarm
        <Directory /home/ubuntu/khu_alarm/khu_alarm>
                Require all granted
        </Directory>

        <Directory /home/ubuntu/khu_alarm/notice>
                Require all granted
        </Directory>


</VirtualHost>
