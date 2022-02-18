from lxml import etree
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import csv
import re
from lxml import etree
from lxml.html import HtmlElement
from io import StringIO

URL = "https://catpre.com/category/060?page=6&sortBy=CATEGORY_RANKING_SCORE_DESC"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
res = rq.get(URL, headers=HEADERS)
res.raise_for_status()
soup = bs(res.text, "lxml")

# 상품 카드 정보
content_product = soup.find_all("div", attrs = {"class":"MuiCardContent-root jss250"})

# 상품 카드 정보 중 별 int 정보
content_star = soup.find_all("span", attrs = {"aria-label": re.compile(r"([-+]?\d*\.\d+|\d+)\sStars")})
index = 0
for star in content_star:
    res = re.findall(r"[-+]?\d*\.\d+|\d+", star["aria-label"])
    print(index, res)
    index += 1
#res = re.findall(r"[-+]?\d*\.\d+|\d+", content_star[19]["aria-label"])
