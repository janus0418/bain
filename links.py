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

links = ["https://comic.naver.com/genre/bestChallenge.nhn"]

#f = open("demoday_comp_info_summary.csv", "w", encoding="utf-8-sig", newline="") 

#writer = csv.writer(f)
title = ("기업명", "대표자", "설립년도", "임직원수", "카테고리", "사업분야", "홈페이지", "페이스북", "트위터", "블로그", "링크")
#writer.writerow(title)

headers = {"Usser-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
for link in links:
    source = rq.get(link, headers=headers)
    source.raise_for_status
    soup = bs(source.text, "lxml")
    company_name = link.split("/")[4]
    row_vals = soup.find_all("span", attrs={"class":"Ntxt_webtoon"})
    #row = [company_name]
    #row_vals = soup.find("span", attrs={"class":"title"})
    # for val in row_vals:
    #     row.append(val.get_text())
    #row.append(link)
    #writer.writerow(row)

print(row_vals)