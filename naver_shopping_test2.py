from selenium import webdriver
import selenium
import time
from bs4 import BeautifulSoup
import re
import csv
import requests as rq
import grequests

filename = "naver_shopping_test2run_results.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") 
writer = csv.writer(f)
title = ['SKU Name','Brand_name','Price','Price Pre-DC','SKU Weight','Reviews', 'Delivery Cost', 'URL']
writer.writerow(title)

url = "https://search.shopping.naver.com/search/category?catId=50006630&origQuery&pagingIndex=1&pagingSize=80&productSet=window&query&sort=rel&timestamp=&viewType=list&window=pet"
driver = webdriver.Chrome()   # 빈 브라우저 띄움
driver.get(url)
time.sleep(3)


HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
########
page = 0   
########

last_meta = []

while True:
    # 스크롤 끝까지 내리기
    while True :
        SCROLL_PAUSE_TIME = 1
        # 화면 최하단으로 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 페이지 로드를 기다림
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        last_height = new_height

        # 새로운 높이가 이전 높이와 변하지 않았을 경우 스크롤 종료
        if new_height == last_height:
            break
        
        # 스크롤 다운이 된다면 스크롤 다운이 된 후의 창 높이를 새로운 높이로 갱신
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'lxml')
    metadata = soup.find_all('div', class_='basicList_title__3P9Q7')
    if last_meta == []:
        pass
    elif last_meta[0].a.get('title') == metadata[0].a.get('title'):
        break
    last_meta = metadata
    metadata2 = soup.find_all('div', class_='basicList_price_area__1UXXR')
    reviews = soup.find_all("em", class_='basicList_num__1yXM9')
    cnt = len(metadata)
    # goes through each product

    titles = []
    product_weights = []
    prices = []
    review_nums = []
    spec_links = []
    original_prices = []

    print(cnt)
    for i in range(0,cnt) :
        # title
        title = metadata[i].a.get('title')
        if title != None :
            title = metadata[i].a.get('title')
        elif title == None :
            title = metadata[i].a.get_text()
        else:
            title = "NA"
        titles.append(title)

        # 판매중량 weight
        try :
            product_weight = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[{}]/li/div/div[2]/div[4]/div[1]'.format(i+1))
        except selenium.common.exceptions.NoSuchElementException:
            product_weight = None
        

        if product_weight != None:
            product_weight = product_weight.text
            if re.search(r'(중량 : )', product_weight):
                product_weight = re.findall(r'(중량 : \d+.\d+kg)|(중량 : \d+kg)|(중량 : \d+g)', product_weight)
                if product_weight != []:
                    for weight in product_weight[0]:
                        if weight != '':
                            product_weight = weight[5:]
                else :
                    product_weight = "NA"
            else :
                product_weight = "NA"
        else:
            product_weight = "NA"
        product_weights.append(product_weight)

        # price
        price = metadata2[i].find('span', class_='price_num__2WUXn')
        if price != None : 
            price = price.text[0:-1]
        elif price == None :
            price = metadata2[i].strong.get_text()[0:-1]
        else:
            price = "NA"   
        prices.append(price)

        # review num
        review = reviews[i]
        if review != None:
            review = review.get_text()
            if (review == None) or (review == ''):
                review = "NA"
        else:
            review = "NA"
        review_nums.append(review)

        # goes to spec page
        spec_link = metadata[i].a.get('href')
        spec_links.append(spec_link)

    print(len(titles))
    print(len(spec_links))

    for i in range(0,cnt):
        writer.writerow([titles[i], prices[i], product_weights[i], reviews[i], spec_links[i]])

    page += 1
    print("page = ", page, "크롤링 완료")  # 결과 확인 위한 출력

    # moving on to next page
    try :
        next_btn = driver.find_element_by_class_name('pagination_next__1ITTf')
    except selenium.common.exceptions.NoSuchElementException:
        break
    next_btn.click()

    # soup_next = BeautifulSoup(driver.page_source, 'lxml')
    # metadata_next = soup_next.find_all('div', class_='basicList_title__3P9Q7')
    # # page_data = wait(driver,10).until(expcond.presence_of_element_located((by.CLASS_NAME, 'basicList_title__3P9Q7')))
    # print(metadata[0].a.get('title'))
    # print(metadata_next[0].a.get('title'))
    # if (metadata_next == metadata) or (metadata_next== None) :
    #     break

print("\nend of task")