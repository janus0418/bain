import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import re


url = "https://www.coupang.com/np/search?component=&q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
page = rq.get(url, headers=headers)
page.raise_for_status()

soup = bs(page.text, "lxml")

items = soup.find_all("li", attrs={"class":re.compile("^search-product")})
#title = items[0].find("div", attrs={"class":"name"}).get_text()
res = []
count = 0
for item in items:
    
    ######################################################
    # 광고 제품은 제외
    ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
    if ad_badge:
        continue
    ######################################################

    ######################################################
    # 레노버 제품 제외
    title = item.find("div", attrs={"class":"name"}).get_text()
    if "레노버" in title:
        continue
    ######################################################

    price = item.find("strong", attrs={"class":"price-value"}).get_text()
    rating = item.find("em", attrs={"class":"rating"})
    rating_num = item.find("span", attrs={"class":"rating-total-count"})


    if rating:
        rating = float(rating.get_text())
    else:
        rate = "평점 없음"

    if rating_num:
        rating_num = float(rating_num.get_text()[1:-1])
    else:
        rating_num = " 평점 카운트 없음 "
    
    res_temp = {"title":title, "price":price, "rating":rating, "rating count":rating_num}
    res.append(res_temp)
    #print(res_temp)
    count += 1

print(count)

over_rate_5 = []
for i in res:
    if i["title"]=="레노버":
        over_rate_5.append(i)

print(over_rate_5)
print(len(over_rate_5))


# print(res[0])
# print(res[0][0],"\n",res[0][1],"\n",res[0][2])

