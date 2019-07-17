import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import pymysql.cursors

# 게시물 업데이트 되는지 계속 polling
while (True) :
    # file에서 최근 값을 불러오기(db에서 불러오는 걸로 바꿔도 될 듯)
    f = open("khu_ce_file.txt", mode ="rt", encoding="utf-8")
    RECENT_POST_NUMBER = f.read()
    f.close()

    RESULT_POST_NUMBER = RECENT_POST_NUMBER
    
    # url로 html 문서 받아오기 
    with urllib.request.urlopen("http://ce.khu.ac.kr/index.php?hCode=BOARD&bo_idx=2") as r :
        soup = BeautifulSoup(r, "html.parser")

        # <tr> 안에 게시물 데이터가 담기므로 그 안에서 데이터 추출
        for post in soup.body.table.find_all("tr")[1:] :
            ID = post.contents[1].get_text()
            if ID > RECENT_POST_NUMBER :
                NAME = post.contents[3].get_text()
                DATE = post.contents[9].get_text()
                URL = "http://ce.khu.ac.kr/index.php" + post.find("a")["href"]
                # db(mysql)와 연결
                connection = pymysql.connect(host = 'localhost', port = 3306, user='root', passwd='1234', db = 'khu_alarm', charset='utf8')
                
                # 파일에 쓸 가장 최근 업로드된 데이터를 저장 
                if RESULT_POST_NUMBER < ID:
                    RESULT_POST_NUMBER = ID
                
                # 데이터 미리보기
                print(ID) #번호
                print(NAME) #게시물이름
                print(DATE) #게시일
                print(URL) #링크
                # db에 데이터 저장
                try :
                    with connection.cursor() as cursor :
                        # 게시물 삽입
                        sql = "INSERT INTO `khu_ce_notice` (`id`, `name`, `date`, `url`) VALUES (%s,%s,%s,%s)"
                        cursor.execute(sql,(ID, NAME, DATE, URL))
                        connection.commit()
                        
                        # 게시물 100개 이상이면 삭제
                        sql = "DELETE FROM `khu_ce_notice` WHERE `id` = %s"
                        cursor.execute(sql, str(int(RESULT_POST_NUMBER) - 100))
                        connection.commit()
                finally:
                    connection.close()
            
    # 변경점이 없을 경우
    if RESULT_POST_NUMBER == RECENT_POST_NUMBER :
        print("NOT Chaged")
    
    
    f = open("khu_ce_file.txt", mode ="wt", encoding ="utf-8")
    f.write(RESULT_POST_NUMBER)
    f.close()


    # 10초마다 반복
    sleep(10)