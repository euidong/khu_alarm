from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

# 모든 팝업창 닫기
def close_all_popup(driver) :
    popups = driver.find_elements_by_tag_name('iframe')[:-2]
    for popup in popups :
        popup_src = popup.get_attribute("src")
        # '=' 이후가 popup id이다.
        popup_id = popup_src[popup_src.find('=') + 1:]
        driver.switch_to_frame(popup)
        driver.execute_script('fn_close("{}");'.format(popup_id))


    

driver = webdriver.Chrome('/Users/justi/chromedriver_win32/chromedriver')

driver.implicitly_wait(3)

driver.get('https://klas.khu.ac.kr/index.jsp?sso=ok')


main = driver.find_element_by_name('main')
driver.switch_to_frame(main)

close_all_popup(driver)

# main 화면으로 돌아가기
driver.switch_to_default_content()
driver.switch_to_frame(main)

# 로그인 하기
driver.find_element_by_name('USER_ID').send_keys("justdo")
driver.find_element_by_name('PASSWORD').send_keys("2016104163a")
driver.execute_script('login()')

main = driver.find_element_by_name('main')

driver.switch_to_frame(main)

html = driver.page_source

bs = BeautifulSoup(html, 'lxml')

alarm = bs.find('div', class_='log_ex_sec_cont')

if alarm.find('dl').get_text() == '' :
    print("알림이 없습니다.")
else :
    for warning in alarm.find_all('dl') :
        warning.find('dt').get_text() # 강좌 이름
        warning.find('dd').get_text()[:-12] # 과제 이름
        warning.find('dd').get_text()[-12:] # 마감 기한


