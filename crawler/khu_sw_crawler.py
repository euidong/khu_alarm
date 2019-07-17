import requests
from bs4 import BeautifulSoup
from time import sleep
import pymysql.cursors

if __name__=="__main__":
    connection = pymysql.connect(host = 'localhost', port = 3306, user='root', passwd='1879', db = 'khu_alarm', charset='utf8')
    
    while True :
        f = open("khu_sw_file.txt", mode ="rt", encoding="utf-8")
        RECENT_POST_NUMBER = f.read()
        f.close()
        RESULT_POST_NUMBER = RECENT_POST_NUMBER

        html = requests.get('http://swedu.khu.ac.kr/board5/bbs/board.php?bo_table=06_01')
        bs = BeautifulSoup(html.text,'lxml')
        div = bs.find('div',class_='tbl_head01 tbl_wrap')
        trs = div.find_all('tr')
        

        for tr in trs[1:]:
            number = tr.find('td',class_='td_num2').get_text().strip()
            name = tr.find('div',class_='bo_tit').a.get_text().strip()
            date = tr.find('td',class_='td_datetime').get_text().strip()
            url = tr.find('div', class_='bo_tit').a["href"]

            print(number)
            print(name)
            print(date)
            print(url)
            # if number == '공지' :
            
            # else :
            #     if RECENT_POST_NUMBER < number :
            #         if RESULT_POST_NUMBER < number :
            #             RESULT_POST_NUMBER = number
            #     try :
            #         with connection.cursor() as cursor :
            #             # 게시물 삽입
            #             sql = "INSERT INTO `khu_sw_notice` (`id`, `name`, `date`, `url`) VALUES (%s,%s,%s,%s)"
            #             cursor.execute(sql,(number, name, date, url))
            #             connection.commit()

            #             # 게시물 100개 이상이면 삭제
            #             sql = "DELETE FROM `khu_sw_notice` WHERE `id` = %s"
            #             cursor.execute(sql, str(NUMBER - 100))
            #             connection.commit()
            #     finally:
            #         connection.close()
        # sleep(10)
