import pandas as pd
import re
import requests as rq
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time
import pyperclip as pc
from selenium.webdriver.common.action_chains import ActionChains

# element = browser.find_element_by_class_name("link_login")
# element.click() # 해당 객체 클릭
# browser.back() # 뒤로가기
# browser.forward() # 앞으로가기
# browser.refresh() # F5
# elem = browser.find_element_by_tag_name("a") #a tag인거 제일 위에 것
# elem = browser.find_elements_by_tag_name("a") #a tag인것들 모두 다
# input 내보내기 :
# from selenium.webdriver.common.keys import Keys
# elem.send_keys("서예지")
# elem.send_keys("Keys.ENTER") # Enter는 반드시 All Caps
# 
# for e in elem:
#   e.get_attribute("href") #전에는 dictionary 형식이라 ["href"]로 key 입력한거랑 대비
# elem = browser.find_element_by_xpath("__여기에 입력__")
# #f12에서 우클릭해서 xpath 복사 가능, 
# 다만 xpath내의 큰 따음표는 작은 따음표로 바꿔주거나 탈출문자 처리, string표시와 겹침
# browser.close()
# browser.quit()
browser = wd.Chrome() #같은 file space에 있지 않을 경우 괄호안에 chromedirver경로 적어줘야 함

# 네이버 이동
browser.get("http://naver.com")

# 로그인 버튼 찾기
elem = browser.find_element_by_class_name("link_login")
elem.click()

# time.sleep(1)

# naver_id = browser.find_element_by_name("id")
# naver_pw = browser.find_element_by_name("pw")

# naver_id.click()
# pc.copy("sunghunsuk99")
# naver_id.send_keys(Keys.CONTROL, 'v')
# time.sleep(1)
# naver_pw.send_keys(Keys.CONTROL, 'v')
# time.sleep(1)
# login_btn = browser.find_element_by_id("log.login")
# login_btn.click()

# def clipboard_input(elem_id, user_input):
#     temp_user_input =pc.paste()

#     pc.copy(user_input)
#     browser.find_element_by_id(elem_id).click()
#     ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

#     pc.copy(temp_user_input)
#     time.sleep(1) # 창 뜰 시간, 필요할때가 있음

# login = { 
#     "id" : "sunghunsuk99",
#     "pw" : "janus0418"
# }

# clipboard_input("id", login.get("id"))
# clipboard_input("pw", login.get("pw"))
# browser.find_element_by_id("log.login").click()


# id,pw 입력 및 로그인
naver_id = "sunghunsuk99"
naver_pw = "janus0418"
time.sleep(1) # 창 뜰 시간, 필요할때가 있음
pc.copy(naver_id)
browser.find_element_by_id("id").send_keys(Keys.CONTROL, 'v')
time.sleep(1) # 창 뜰 시간, 필요할때가 있음
pc.copy(naver_pw)
browser.find_element_by_id("pw").send_keys(Keys.CONTROL, 'v')
time.sleep(1) # 창 뜰 시간, 필요할때가 있음
## browser.find_element_by_id("id").clear() # 지워주기

browser.find_element_by_id("log.login").click()

# html 정보 출력
print(browser.page_source)

# browser 종료
browser.close()
