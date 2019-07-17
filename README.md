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


