import requests as rq
from bs4 import BeautifulSoup as bs
import re
import csv
import re
from lxml import etree
from lxml.html import HtmlElement
from io import StringIO

filename = "catpre_raw_data.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") 
writer = csv.writer(f)
title = ["제품유형","브랜드명", "상품명", "현재가격", "할인전가격", "리뷰수", "별점", "재고상태", "배송유형", "배송비용"]
writer.writerow(title)

# categories = ["053","054","055","056","057","058","059","060","061","063","064","069","065","070"]
categories =["059"]
#product_category = ["사료","간식","건강관리","모래","화장실/위생","미용/목욕","급식기/급수기","스크래쳐/캣타워","하우스","이동장","의류/악세서리","목줄/가슴줄","장난감","생활/가전"]
product_category =["급식기/급수기"]
exceptions =[]

category_index = 0
for category in categories:
    page_index = 0
    while True:
        URL = "https://catpre.com/category/059?page={}&sortBy=CATEGORY_RANKING_SCORE_DESC".format(page_index)
               
        #URL = "https://catpre.com/category/{}?page={}&sortBy=CATEGORY_RANKING_SCORE_DESC".format(category,page_index)
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
        res = rq.get(URL, headers=HEADERS)
        res.raise_for_status()
        soup = bs(res.text, "lxml")

        # Stop when no more content is available 
        if not soup.find("div", attrs = {"class":"MuiCardContent-root jss250"}):
            break
        
        # 상품 카드 정보
        content_product = soup.find_all("div", attrs = {"class":"MuiCardContent-root jss250"})
        print(content_product)

        # 상품 카드 정보 중 별 int 정보
        content_star = soup.find_all("span", attrs = {"aria-label": re.compile(r"([-+]?\d*\.\d+|\d+)\s(Stars|Star)")})
        
        #-----------------------------Storage--------------------------------------
        star_score = []
        name = []
        price = []
        review_num = []
        inventory_status = []
        delivery_type =[]
        delivery_cost = []
        brand_name = []
        price_before_discount = []
        #--------------------------------------------------------------------------
        
        # Counter
        row_num = 0
        
        # Loop
        for item in content_product:
            row_num += 1
            # 제품명
            item_name =  item.h3.get_text()
            name.append(item_name)

            # 제품가격
            item_price = item.strong.get_text()[0:-1]
            price.append(item_price)

            # 제품 리뷰수
            item_review_num = item.div.next_sibling.span.next_sibling.text[1:-1]
            review_num.append(item_review_num)

            # # 제품 세부사항
            product_page = "https://catpre.com"+item.parent.parent.a["href"]
            product_res = rq.get(product_page, headers=HEADERS).text

            parser = etree.HTMLParser()
            tree = etree.parse(StringIO(product_res), parser)
            result = etree.tostring(tree.getroot(),pretty_print=True, method="html")

            # 재고상태 - 재고유무
            inventory_status_per_item = ''.join(tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/span/text()'))
            inventory_status.append(inventory_status_per_item)

            # 배송방법 - 대통령 배송 여부
            delivery_type_per_item = ''.join(tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/span/text()'))
            delivery_type.append(delivery_type_per_item)

            # 배송비용 - 무료 배송 여부
            delivery_cost_per_item = ''.join(tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[3]/span/text()'))
            delivery_cost.append(delivery_cost_per_item)

            # 브랜드명
            brand_name_per_item = ''.join(tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/a/text()'))
            brand_name.append(brand_name_per_item)

            # 할인전 가격
            price_before_discount_per_item = ''.join(tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[5]/div[1]/dl/dd/s/text()'))[0:-1]

            if price_before_discount_per_item == '':
                irregular = ''.join(tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/dl/dd/s/text()'))[0:-1]
                price_before_discount_per_item = irregular
            
            if price_before_discount_per_item == '':
                irregular2 = tree.xpath('//div[@id="__next"]/div[1]/div[1]/div[2]/div[1]//div[1]/div[2]/div[1]/div[5]/div[1]/dl/dd/span/span/text()')
                if irregular2 == []: 
                    price_before_discount_per_item = "NA"
                else:
                    price_before_discount_per_item = irregular2[0]

            price_before_discount.append(price_before_discount_per_item)

        # 별점
        for star in content_star:
            res = re.findall(r"[-+]?\d*\.\d+|\d+", star["aria-label"])
            if res == '':
                res = "NA"
            star_score.append(res)

        # Write into csv 
        for row in range(0,row_num):
            writer.writerow([
                product_category[category_index],
                brand_name[row], 
                name[row], 
                price[row], 
                price_before_discount[row],
                review_num[row], 
                star_score[row][0], 
                inventory_status[row], 
                delivery_type[row], 
                delivery_cost[row]])
        page_index = page_index + 1
    category_index = category_index + 1

print("\nend of task")
