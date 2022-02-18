from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('/Users/46921/Desktop/crawl/chromedriver')
# 웹 지원 로드 시간 지정 


driver.get('https://schoolbus.ssif.or.kr/sb/index.html')
wait = WebDriverWait(driver, 10)
## 웹사이트 목록 접근
driver.implicitly_wait(15)
driver.find_element_by_xpath('/html/body/div[2]/div[4]/ul/li').click()
driver.find_element_by_xpath('//*[@id="headerWr"]/div[2]/div/ul/li[2]/a').click()
time.sleep(3)

## 리스트 조회
driver.find_element_by_xpath('//select[@name="facilities"]/option[text()="어린이집"]').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="viewList"]').click()

full_group = []
#driver.find_element_by_xpath('//*[@id="2019-0038926"]/td[3]').click()

back = '//*[@id="carinfo_view_alert"]/div[7]/a/img'
try:
    
    for page2 in range (0, 120):
        pgnum = (page2+1)*10
        driver.find_element(By.ID, 'pageNum' + str(pgnum)).click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="paging_content"]/a[13]/img').click()
        time.sleep(2)
    
    for page in range (1201, 1691):
        # 리스트 그룹 내 10개 행에 대한 iteration
        for i in range(1, 11):
            # clicking into info
            search_list_text = '//*[@id="listTable"]/tr['+str(i)+']/td[3]'
            wait.until(EC.element_to_be_clickable((By.XPATH, search_list_text)))
            driver.find_element_by_xpath(search_list_text).click()
            
            ### 시설 정보
            시설구분 = driver.find_element(By.XPATH, '//*[@id="detailTable"]/tr[1]/td[2]').text
            시설명 = driver.find_element(By.XPATH, '//*[@id="detailTable"]/tr[2]/td[2]').text
            운영자 = driver.find_element(By.XPATH,'//*[@id="detailTable"]/tr[2]/td[4]').text
            설립구분 = driver.find_element(By.XPATH,'//*[@id="detailTable"]/tr[3]/td[2]').text
            주소 = driver.find_element(By.XPATH,'//*[@id="detailTable"]/tr[4]/td[2]').text
            전화번호 = driver.find_element(By.XPATH,'//*[@id="detailTable"]/tr[4]/td[4]').text
            현정원 = driver.find_element(By.XPATH,'//*[@id="detailTable"]/tr[5]/td[4]').text
            fac_info = [시설구분, 시설명, 운영자, 설립구분, 주소, 전화번호, 현정원]
            
            rows = driver.find_elements(By.XPATH,'//*[@id="detailbusInfoList"]/tr')

            for j in range (1, len(rows) + 1):
                # clicking into car info
                car_list_text = '//*[@id="detailbusInfoList"]/tr[' + str(j) + ']/td[8]/a/img'
                wait.until(EC.element_to_be_clickable((By.XPATH, car_list_text)))
                driver.find_element(By.XPATH,car_list_text).click()
                
                # 보유 통학버스 별 정보 
                차량등록번호 = driver.find_element(By.ID, "view_detail_car_code").get_attribute("value")
                소유자_성명 = driver.find_element(By.ID, "view_detail_owner_name").get_attribute("value")
                등록일 = driver.find_element(By.ID, "view_detail_reg_date").get_attribute("value")
                차종 = driver.find_element(By.ID, "view_detail_car_type_name").get_attribute("value")
                제작연도 = driver.find_element(By.ID, "view_detail_product_date").get_attribute("value")
                정원 = driver.find_element(By.ID, "view_detail_car_capacity").get_attribute("value")
                용도 = driver.find_element(By.ID, "view_detail_use_type_name").get_attribute("value")
                제작사 = driver.find_element(By.ID, "view_detail_car_company").get_attribute("value")
                차량명 = driver.find_element(By.ID, "view_detail_car_name").get_attribute("value")
                차량소유 = driver.find_element(By.ID, "view_detail_car_owner_name").get_attribute("value")
                car_info = [차량등록번호, 소유자_성명, 등록일, 차종, 제작연도, 정원, 용도, 제작사, 차량명, 차량소유]
                full_info = fac_info + car_info
                full_group.append(full_info)
                print(full_info)
                # unclicking car info
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, back)))
                driver.find_element_by_xpath(back).click()
                print (str(page)+"/"+ str(i)+ "/"+ str(j))
            # display driver


            driver.execute_script('document.getElementById("searh_list_table").style.display="block";')
        # end of page list

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="paging_content"]/a[13]/img')))
        print ('did u click')
        driver.find_element(By.XPATH, '//*[@id="paging_content"]/a[13]/img').click()
        time.sleep(3)
    columns = ['시설구분', '시설명', '운영자', '설립구분', '주소', '전화번호', '현정원',
               '차량등록번호', '소유자_성명', '등록일', '차종', '제작연도', '정원', 
               '용도', '제작사', '차량명', '차량소유']

    full_group = [columns] + full_group
    # data frame
    df = pd.DataFrame(full_group)
    x = time.time()
    df.to_excel(str(x) + 'tester.xlsx', sheet_name="sheep")
except:

# add columns
    columns = ['시설구분', '시설명', '운영자', '설립구분', '주소', '전화번호', '현정원',
               '차량등록번호', '소유자_성명', '등록일', '차종', '제작연도', '정원', 
               '용도', '제작사', '차량명', '차량소유']

    full_group = [columns] + full_group
    # data frame
    df = pd.DataFrame(full_group)
    x = time.time()
    df.to_excel(str(x) + 'tester.xlsx', sheet_name="sheep")
    