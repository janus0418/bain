import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
import re


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
res = []
for i in range(1,6):
    url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={}&rocketAll=false&searchIndexingToken=1=4&backgroundColor=".format(i)
    page = rq.get(url, headers=headers)
    page.raise_for_status
    soup = bs(page.text, "lxml")

    items = soup.find_all("li", attrs={"class":re.compile("^search-product")})
    #title = items[0].find("div", attrs={"class":"name"}).get_text()
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

        # 가격
        price = item.find("strong", attrs={"class":"price-value"}).get_text()
        
        # 평점
        rating = item.find("em", attrs={"class":"rating"})
        if rating:
            rating = float(rating.get_text())
        else:
            rate = "평점 없음"

        # 평점 갯수
        rating_num = item.find("span", attrs={"class":"rating-total-count"})
        if rating_num:
            rating_num = float(rating_num.get_text()[1:-1])
        else:
            rating_num = " 평점 카운트 없음 "
        
        # 링크
        link = "https://www.coupang.com/"+item.find("a", attrs={'class':"search-product-link"})["href"]

        res_temp = {"title":title, "price":price, "rating":rating, "rating count":rating_num, "link":link}
        res.append(res_temp)
        #print(res_temp)

print(len(res))
print(res[0]["link"])
print("run terminated")
print("-"*100)