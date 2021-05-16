from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import requests as rq
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as expcond

import time
import csv


driver = wd.Chrome()
url = "https://flight.naver.com/flights/?trip=RT&scity1=ICN&scity2=&ecity1=&ecity2=ICN&adult=1&child=0&infant=0&fareType=YC&airlineCode=&nxQuery=%ED%95%AD%EA%B3%B5%EA%B6%8C"


driver.maximize_window()
driver.get(url)

# 가는 날 선택 후 클릭
driver.find_element_by_link_text("가는날 선택").click()

# 이번달, 다음달 27일, 28일 선택
driver.find_elements_by_link_text("27")[0].click() # [0] --> 이번달
driver.find_elements_by_link_text("28")[1].click() # [1] --> 다음달

# 제주도 설정
driver.find_element_by_xpath('//*[@id="recommendationList"]/ul/li[1]').click()

# 인원 추가

adult_num = 5
child_num = 2
baby_num = 1

passenger_types = ["adult", "child", "baby"]
passengers = { "adult": {"id": 0, "count": adult_num-1}, "child": {"id": 1, "count": child_num}, "baby": {"id": 2, "count": baby_num}}

driver.find_element_by_xpath('//*[@id="l_8"]/div[2]/div[1]/a').click()

for passenger_type in passenger_types:
    for rep in range(0,passengers[passenger_type]["count"]):
        driver.find_elements_by_link_text("인원 추가")[passengers[passenger_type]["id"]].click()

driver.find_element_by_xpath('//*[@id="l_8"]/div[2]/div[1]/a').click()

# 항공권 검색 클릭

driver.find_element_by_link_text("항공권 검색").click()

# 첫번째 결과 출력

try:
    elem = wait(driver, 10).until(expcond.presence_of_element_located((by.XPATH, '//*[@id="content"]/div[2]/div/div[4]/ul/li[1]')))
    print("\npage load successful")
finally:
    driver.close


filename = "flight_options.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)

for i in range(1,21):
    elem = driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div[4]/ul/li[{}]'.format(i)).text
    writer.writerow(elem)






# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
# page = rq.get(rq.Response.url, headers=headers)
# page.raise_for_status()
# soup = bs(page.text, "lxml")



# print(elem.text)
# 최대 10초까지 저 결과가 나올때까지 기다린다. 안 될시 종료



# test finish sequence
# time.sleep(5)
# driver.close()

