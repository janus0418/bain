from selenium import webdriver
import selenium
import time
from bs4 import BeautifulSoup
import csv
import grequests

HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
filename = "naver_shopping_testrun_results_3.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") 
writer = csv.writer(f)
title = ['SKU Name','Brand_name','Price','Price Pre-DC','SKU Weight','Reviews', 'Delivery Cost', 'URL']
writer.writerow(title)


url = "https://search.shopping.naver.com/search/category?catId=50006630&origQuery&pagingIndex=1&pagingSize=80&productSet=window&query&sort=rel&timestamp=&viewType=list&window=pet"
driver = webdriver.Chrome()   # 빈 브라우저 띄움
driver.get(url)
time.sleep(3)

def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    resp = grequests.map(reqs)
    return resp

def url_details(resps,lst):
    i = 0
    for resp in resps:
        res = []
        # print(resp)
        page = resp.text
        soup_spec = BeautifulSoup(page, "lxml")

        # original price
        original_price = soup_spec.find("del", class_='Xdhdpm0BD9')
        if original_price:
            original_price = original_price.span.next_sibling.get_text()
        else : 
            original_price = "NA"
        
        res.append(original_price)

        # brand name 
        brand_name = soup_spec.find_all("td", class_="jvlKiI0U_y")
        if brand_name :
            brand_name = brand_name[3].get_text()
            if (brand_name == '') or (brand_name == None) :
                brand_name = "NA"
        else:
            brand_name = "NA"
        res.append(brand_name)
        # delivery cost
        delivery_cost = soup_spec.find("span", class_="_1_wrVRMvuL")
        if delivery_cost:
            delivery_cost = delivery_cost.get_text()
            if delivery_cost == '':
                delivery_cost = "NA"
        else:
            delivery_cost = "NA"
        res.append(delivery_cost)
        lst[i]=res
        i += 1



########
page = 0   
########

# for each page until no page
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
    else:
        last_meta = metadata
    metadata2 = soup.find_all('div', class_='basicList_price_area__1UXXR')
    reviews = soup.find_all("em", class_='basicList_num__1yXM9')
    cnt = len(metadata)
    # goes through each product

    #---------------------------------
    # title = ['SKU Name','Brand_name','Price','Price Pre-DC','SKU Weight','Review Nums', 'Delivery Cost', 'Product Links']
    sku_names = []
    prices = []
    sku_weights = []
    review_nums = []
    product_links = []
    spec_infos = {}
    for i in range(0,cnt) :
        
        # title
        title = metadata[i].a.get('title')
        if title != None :
            title = metadata[i].a.get('title')
        elif title == None :
            title = metadata[i].a.get_text()
        else:
            title = "NA"
        sku_names.append(title)

        # # 판매중량 weight
        # try :
        #     product_weight = driver.find_element_by_xpath('//*[@id="__next"]/div/div[2]/div/div[3]/div[1]/ul/div/div[{}]/li/div/div[2]/div[4]/div[1]'.format(i+1))
        # except selenium.common.exceptions.NoSuchElementException:
        #     product_weight = None
        

        # if product_weight != None:
        #     product_weight = product_weight.text
        #     if re.search(r'(중량 : )', product_weight):
        #         product_weight = re.findall(r'(중량 : \d+.\d+kg)|(중량 : \d+kg)|(중량 : \d+g)', product_weight)
        #         if product_weight != []:
        #             for weight in product_weight[0]:
        #                 if weight != '':
        #                     product_weight = weight[5:]
        #         else :
        #             product_weight = "NA"
        #     else :
        #         product_weight = "NA"
        # else:
        #     product_weight = "NA"
        # sku_weights.append(product_weight)

        # # price
        # price = metadata2[i].find('span', class_='price_num__2WUXn')
        # if price != None : 
        #     price = price.text[0:-1]
        # elif price == None :
        #     price = metadata2[i].strong.get_text()[0:-1]
        # else:
        #     price = "NA"   
        # prices.append(price)

        # # review num
        # review = reviews[i]
        # if review != None:
        #     review = review.get_text()
        #     if (review == None) or (review == ''):
        #         review = "NA"
        # else:
        #     review = "NA"
        # review_nums.append(review)

        # goes to spec page
        spec_link = metadata[i].a.get('href')
        product_links.append(spec_link)

        # page_source = rq.get(spec_link, headers=HEADERS).text
        # soup_spec = BeautifulSoup(page_source, "lxml")

        # # original price
        # original_price = soup_spec.find("del", class_='Xdhdpm0BD9')
        # if original_price:
        #     original_price = original_price.span.next_sibling.get_text()
        # else : 
        #     original_price = "NA"

        # # brand name 
        # brand_name = soup_spec.find_all("td", class_="jvlKiI0U_y")
        # if brand_name :
        #     brand_name = brand_name[3].get_text()
        #     if (brand_name == '') or (brand_name == None) :
        #         brand_name = "NA"
        # else:
        #     brand_name = "NA"

        # # delivery cost
        # delivery_cost = soup_spec.find("span", class_="_1_wrVRMvuL")
        # if delivery_cost:
        #     delivery_cost = delivery_cost.get_text()
        #     if delivery_cost == '':
        #         delivery_cost = "NA"
        # else:
        #     delivery_cost = "NA"

        # # writes into file
        # writer.writerow([title, brand_name, price, original_price, product_weight, review, delivery_cost, spec_link])
    print(len(product_links))
    responses = get_data(product_links)
    url_details(responses, spec_infos)
    print(spec_infos)
    # writing title = ['SKU Name','Brand_name','Price','Price Pre-DC','SKU Weight','Reviews', 'Delivery Cost', 'URL']
    # for i in range(0,cnt):
    #     writer.writerow(
    #         [
    #             sku_names[i],
    #             spec_infos[i][1],
    #             prices[i], 
    #             spec_infos[i][0],
    #             sku_weights[i],
    #             review_nums[i],
    #             spec_infos[i][2],
    #             product_links[i]
    #         ]
    #     )


    page += 1
    print("page = ", page, "크롤링 완료")  # 결과 확인 위한 출력

    # moving on to next page
    try :
        next_btn = driver.find_element_by_class_name('pagination_next__1ITTf')
    except selenium.common.exceptions.NoSuchElementException:
        break
    next_btn.click()
    
    # page_data = wait(driver,10).until(expcond.presence_of_element_located((by.CLASS_NAME, 'basicList_title__3P9Q7')))
    # # try:
    # #     elem = wait(driver, 10).until(expcond.presence_of_element_located((by.XPATH, '//*[@id="content"]/div[2]/div/div[4]/ul/li[1]')))
    # #     print("\npage load successful")
    # # finally:
    # #     driver.close
    # if (page_data == metadata) or (page_data == None) :
    #     break

driver.close()

print("\nend of task")