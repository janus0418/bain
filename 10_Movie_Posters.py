import requests as rq
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
count = 0
for year in range(2015,2020):        
    url = "https://search.daum.net/search?w=tot&q={}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR".format(year)
    page = rq.get(url,headers=headers)
    soup = bs(page.text, "lxml")
    images = soup.find_all("img", attrs={"class":"thumb_img"})


    ################GIVEN#########################
    # for idx,image in enumerate(images):
    #     image_url = image["src"]
    #     if image_url.startswith("//"):
    #         image_url = "https:" + image_url
    #     print(image_url)
    #     image_res = rq.get(image_url)
    #     image_res.raise_for_status()
    #     with open("movie{}_{}.jpg".format(year,idx+1), "wb") as f:
    #         f.write(image_res.content)
    #     if idx>=4:
    #         break
    #################CREATED####################
    res=[]
    for img in images:
        link = img["src"]
        if "https" not in link:
            res.append("https:"+link)
    for idx, img_source in enumerate(res):
        image = rq.get(img_source)
        image.raise_for_status()
        with open("movie{}_{}.jpg".format(year,idx+1), "wb") as f:
            f.write(image.content)
        if idx>=4:
            break
    #     count += 1
