from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver as wd
import requests as rq
import re
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as expcond

#--------------------------------------------------------------------
# Headless Chrome -- 매번 브라우저 창을 뛰우지 않고 내부적으로 수행
options = wd.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080") #화면에 안 뛰우므로 내부적으로 설정할 화면 크기 제시
#--------------------------------------------------------------------

driver = wd.Chrome(options = options)
driver.maximize_window()

# move to page
url = "https://play.google.com/store/movies/top"
driver.get(url)

# scrolling down
# 모니터(해상도) 높이인 1080 위치로 스크롤 내리기 
# driver.execute_script("window.scrollTo(0,1080)") # 1920x1080 해상도 쓸때 높이

# # 화면 가장 아래로 스크롤 내리기
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


# 새 리로드가 안나올때까지 계속 내리기
import time
interval = 2
prev_height = driver.execute_script("return document.body.scrollHeight")

while True : 
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(interval)
    current_height = driver.execute_script("return document.body.scrollHeight")
    if current_height == prev_height :
        break
    prev_height = current_height

print("스크롤 완료")



soup = bs(driver.page_source, "lxml") # 현재 페이지에서 soup 뜨기

# movies =  soup.find_all("div", attrs={"class":["ImZGtf mpg5gc", "Vpfmgd"]}) 리스트로 넣어서 여러개 or 로 검색
movies =  soup.find_all("div", attrs={"class":"Vpfmgd"})
print(len(movies))

filename = "discounted_movies_comp.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="")
writer = csv.writer(f)
categories = ["제목", "할인 전 가격", "할인 후 가격", "링크"]
writer.writerow(categories)

for movie in movies:
    title = movie.find("div",attrs={"class":"WsMG1c nnK0zc"}).get_text()

    original_price = movie.find("span", attrs={"class":"SUZt4c djCuy"})
    if original_price :
        original_price = original_price.get_text()
    else:
        #print(title, " <할인되지 않은 영화 제외>")
        continue

    # 할인된 가격
    price = movie.find("span", attrs={"class":"VfPpfd ZdBevf i5DZme"}).get_text()
    
    # 링크
    link = "https://play.google.com"+movie.find("a", attrs={"class":"JC71ub"})["href"]

    print(f"제목 : {title}")
    print(f"할인 전 금액 : {original_price}")
    print(f"할인 후 금액 : {price}")
    print(f"링크 : {link}")
    print("-"*120)
    writer.writerow([title, original_price, price, link])



driver.quit()