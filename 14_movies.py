from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver as wd
import requests as rq
import re
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as expcond

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Accpet-Language":"ko-KR,ko"
    }

url = "https://play.google.com/store/movies?utm_source=apac_med&utm_medium=hasem&utm_content=Apr0121&utm_campaign=Evergreen&pcampaignid=MKT-EDR-apac-kr-1003227-med-hasem-mo-Evergreen-Apr0121-Text_Search_BKWS-BKWS%7cONSEM_kwid_43700059433343124_creativeid_485711575917_device_c&gclid=CjwKCAjwg4-EBhBwEiwAzYAlsiH_qAallsOB6ZJbzGJxt09StwZ5qXGqkrmvfiYhignjmvkwU5wC1hoC6RwQAvD_BwE&gclsrc=aw.ds"
page = rq.get(url, headers = headers)
page.raise_for_status()
soup = bs(page.text, "lxml")

movies = soup.find_all("div", attrs={"class":"WHE7ib mpg5gc"})

# with open("movie.html", "w", encoding = "utf8") as f:
#     f.write(page.text)
#     f.write(soup.prettify()) # soup.prettify() --> html 문서를 예쁘게 출력

for movie in movies:
    title = movie.find("div", attrs={"class":"WsMG1c nnK0zc"})
    print(title.text)


