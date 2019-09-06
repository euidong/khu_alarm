import requests
from bs4 import BeautifulSoup
import pymysql.cursors
from pyfcm import FCMNotification

def update_db(number, name, date, url, minus):
    connection = pymysql.connect(host = 'localhost', port = 3306, user='root', passwd='1879', db = 'khu_alarm', charset='utf8')
    registration_ids = []
    try :
        with connection.cursor() as cursor :
            # 게시물 삽입
            sql = "INSERT INTO `khu_sw_notice` (`id`, `name`, `date`, `url`) VALUES (%s,%s,%s,%s)"
            cursor.execute(sql,(number, name, date, url))
            connection.commit()

            if minus:
                sql = "DELETE FROM `khu_sw_notice` WHERE `id` > %s AND `id` < 0"
                cursor.execute(sql, str(-int(url[-3:]) + 100))
                connection.commit()
            else :
                sql = "DELETE FROM `khu_sw_notice` WHERE `id` < %s AND `id` > 0"
                cursor.execute(sql, str(int(number) - 100))
                connection.commit()

            
            sql = "SELECT * from `push`"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            for row in rows :
                registration_ids.append(row[0])
            print(registration_ids)           
    finally:
        connection.close()
    push_service = FCMNotification(api_key="AAAAoGJSySI:APA91bHRE9XHGAkjrCtoiZJPhbXxs7C0dgjbMzWZmZWLnRLYk3j9ZFr80whPyhrPWWYZV4-vQe3nzIw2RlltlyU__GXshnmTLx4b6ZcpPM94VAN_vllU_cLlnrHG2neXyi5n1rswaiDN")
    message_title = "klaser"
    message_body = name
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    print(result)

if __name__=="__main__":
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
        
        post_number = url[-3:]
        if post_number > RECENT_POST_NUMBER:
            print(number)
            print(name)
            print(date)
            print(url)
            if RESULT_POST_NUMBER < post_number :
                RESULT_POST_NUMBER = post_number

            if number == '공지' :
                number = '-' + post_number
                update_db(number, name, date, url, True)
            
            else :
                    update_db(number, name, date, url, False)
            

    if RESULT_POST_NUMBER == RECENT_POST_NUMBER:
        print("NOT Changed")

    with open('khu_sw_file.txt', 'w') as result:
        result.write(RESULT_POST_NUMBER)
    


