from lxml import etree
import requests as rq
from bs4 import BeautifulSoup as bs
import re
import csv
import re
from lxml.html import fromstring
import lxml.html
from lxml.html import HtmlElement
from io import StringIO

# # html_element = lxml.html.parse(
# # 	"https://blog.live2skull.kr/python/lxml/python-lxml/"
# # ) # type: HtmlElement
# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
# product_page = "https://catpre.com/product/214"
# product_res = rq.get(product_page, headers=HEADERS)
# etree.XML(product_res.text)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
product_page = "https://catpre.com/category/059?page=0&sortBy=CATEGORY_RANKING_SCORE_DESC"
product_res = rq.get(product_page, headers=HEADERS).text

parser = etree.HTMLParser()
tree = etree.parse(StringIO(product_res), parser)
result = etree.tostring(tree.getroot(),pretty_print=True, method="html")
res = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[3]/div[1]/div[1]/main/div[1]/div[2]/div[1]')
#//*[@id="__next"]/div[1]/div[1]/div[3]/div/div/main/div/div[2]/div/div/div[1]/div/a/div[2]
print(res[0].attrib)
# inventory_status = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/span/text()')
# delivery_type = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/span/text()')
# delivery_cost = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/span/text()')
# brand_name = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/a/text()')
# price_before_discount = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/dl/dd/span/span/text()')
#                                 #('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/dl/dd/s/text()')
# print(''.join(inventory_status))
# # 재고 없음은 1개단어 재고 있음은 2개 -> 그냥 list에 있는거 다 엮어서 뱉는거 만들기
# print(''.join(delivery_type))
# print(''.join(delivery_cost))
# print(''.join(brand_name))
# print(price_before_discount)
#/html/body/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span
# https://blog.live2skull.kr/python/lxml/python-lxml/
#//*[@id="__next"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]/div[1]/span/text()[1]
#//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/span/text()
# # 제품 세부사항
# HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
# product_page = "https://catpre.com/product/214"
# product_res = rq.get(product_page, headers=HEADERS)
# root = fromstring(product_res.text)
# test = root.xpath('//*[@id="__next"]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/h2')[0]
# print(test)



# # # svg xmlns = http://www.w3.org/2000/svg -> 하트 
# # root = soup.find_all("div", attrs={"class" : "MuiCollapse-container gnbWrap MuiCollapse-entered"})
# # print(root[0])

# # document.querySelector("#__next > div.jss1 > div.MuiContainer-root.jss148.MuiContainer-disableGutters > div.jss2341 > div.jss2343 > div.jss2351 > div.jss2353 > div.jss2355 > div > div.jss2481 > div:nth-child(1) > span")
# # #__next > div.jss1 > div.MuiContainer-root.jss148.MuiContainer-disableGutters > div.jss2341 > div.jss2343 > div.jss2351 > div.jss2353 > div.jss2355 > div > div.jss2481 > div:nth-child(1) > span

