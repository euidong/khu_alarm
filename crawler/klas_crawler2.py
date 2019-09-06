from bs4 import BeautifulSoup
import pymysql.cursors
import requests
from pyfcm import FCMNotification

rows = []
connection = pymysql.connect(host = 'localhost', port = 3306, user='root', passwd='1879', db = 'khu_alarm', charset='utf8')
try :
    with connection.cursor() as cursor :
        # 게시물 삽입
        sql = "SELECT * FROM `myUser`"
        cursor.execute(sql)
        rows.extend(cursor.fetchall())
        print(rows)
finally :
    connection.close()
for row in rows :
    if row[1]==1:
        LOGIN_INFO = {
            'USER_ID' : row[2],
            'PASSWORD' : row[3]
        }
        print(LOGIN_INFO)
        url = "https://klas.khu.ac.kr/muser/loginUser.do"

        with requests.Session() as s :
            req = s.get(url)

            # status (int)
            status = req.status_code

            login_req = s.post(url, data=LOGIN_INFO)
            
            homework = s.get("https://klas.khu.ac.kr/mmain/viewMainList.do?pageIndex=1&gubun=activity")

            soup = BeautifulSoup(homework.text,'html.parser')


            # print(soup.find("ul", class_="ui-listview"))
            main_div = soup.body.div
            ul = main_div.find_all('ul')[1]
            print(ul.get_text())

            if ul.get_text().strip() != '':
                push_service = FCMNotification(api_key="AAAAoGJSySI:APA91bHRE9XHGAkjrCtoiZJPhbXxs7C0dgjbMzWZmZWLnRLYk3j9ZFr80whPyhrPWWYZV4-vQe3nzIw2RlltlyU__GXshnmTLx4b6ZcpPM94VAN_vllU_cLlnrHG2neXyi5n1rswaiDN")
                connection = pymysql.connect(host = 'localhost', port = 3306, user='root', passwd='1879', db = 'khu_alarm', charset='utf8')
                registration_ids = []
                try :
                    with connection.cursor() as cursor :
                        sql = "SELECT * from `push`"
                        cursor.execute(sql)
                        rows = cursor.fetchall()
                        for row in rows :
                            registration_ids.append(row[0])
                finally:
                    connection.close()
                
                print(registration_ids)
                message_title = "klaser"
                message_body = ul.get_text().strip()
                result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
                print(result)
