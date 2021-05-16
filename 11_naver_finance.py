import requests as rq
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import csv

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

filename = "시가총액1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") 
#new row마다 엔터가 한번 더 눌리는 것을 막기 위해 newline=""을 추가
#보통은 utf8로 인코딩 하지만 엑셀에서 열때 한글이 깨진다면 utf-8-sig 사용
writer = csv.writer(f)
title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE".split("\t")
print(type(title))
writer.writerow(title)
for page in range(1,5):
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page={}".format(page)
    source = rq.get(url, headers=headers)
    source.raise_for_status
    soup = bs(source.text, "lxml")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1:
            continue

        data = [column.get_text().strip() for column in columns] 
        #한줄 for 쓰는 방법, strip은 맨 앞과 맨 뒤의 whitespace제거
        writer.writerow(data)
        # print(data)

# permission denied 가 뜰때는 해당 csv 파일이 다른 프로그램에서 열려 있기 때문