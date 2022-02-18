from bs4 import BeautifulSoup as bs
import csv
import selenium
from selenium import webdriver as wd
import requests as rq
import re
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as expcond


#--------------------------------------------------------------------
# Headless Chrome 
options = wd.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080") #화면에 안 뛰우므로 내부적으로 설정할 화면 크기 제시
driver = wd.Chrome(options = options)
driver.maximize_window()
#--------------------------------------------------------------------

# Parameter
objectives =["commerce", "mobile", "web-service", "consumer-goods"]
# objectives =["design"]


# Result --- a list of all links to each company of every category given as a parameter
links = []


# Display all content -- continuously press more button 
for objective in objectives:
    # move to page
    url = "http://www.demoday.co.kr/companies/category/{}".format(objective)
    driver.get(url)

    import time
    #----------------------------------------------------------------------
    interval = 1
    #----------------------------------------------------------------------
    prev_height = driver.execute_script("return document.body.scrollHeight")

    while True : 
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        more_button = driver.find_element_by_xpath("/html/body/div[3]/div/a")
        try:
            element = driver.find_element_by_xpath("/html/body/div[3]/div/a")
            element.click()
        except selenium.common.exceptions.ElementNotInteractableException:
            print("Cannot find more; end of list")
        time.sleep(interval)
        current_height = driver.execute_script("return document.body.scrollHeight")
        if current_height == prev_height :
            break
        prev_height = current_height

    #print("스크롤 완료")

    # scrape links

    soup = bs(driver.page_source, "lxml")

    company_titles =  soup.find_all("h3", attrs={"class":"title"})

    for title in company_titles:
        link = "http://www.demoday.co.kr"+title.a["href"]
        links.append(link)

    #print(links)


#---part2------------------------------------------------

f = open("demoday_comp_info_summary.csv", "w", encoding="utf-8-sig", newline="") 

writer = csv.writer(f)
title = ("기업명", "대표자", "설립년도", "임직원수", "카테고리", "사업분야", "홈페이지", "페이스북", "트위터", "블로그", "링크")
writer.writerow(title)

headers = {"Usser-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

for link in links:
    source = rq.get(link, headers=headers)
    source.raise_for_status
    soup = bs(source.text, "lxml")
    company_name = link.split("/")[4]
    row = [company_name]
    #  --- error ---
    row_vals = soup.find_all("span", attrs={"class":"value"})
    for val in row_vals:
        row.append(val.get_text())
    #  --- error ---
    row.append(link)
    writer.writerow(row)

print(row_vals)