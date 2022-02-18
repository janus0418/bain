from bs4 import BeautifulSoup as bs
import csv
import selenium
from selenium import webdriver as wd
import requests as rq
import re
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.common.by import By as by
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as expcond
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip as pc
import time
import re
#---------------------Parameter Input-------------------------------

# Start, End date value; 8 digit of form yyyymmdd
start_date = '20110101'
end_date = '20110103'

#--------------------------------------------------------------------

# #--------------------------------------------------------------------
# # Headless Chrome 
# options = wd.ChromeOptions()
# options.headless = True
# options.add_argument("window-size=1920x1080") #화면에 안 뛰우므로 내부적으로 설정할 화면 크기 제시
# driver = wd.Chrome(options = options)
# driver.maximize_window()
# #--------------------------------------------------------------------


# Get list page
driver = wd.Chrome()
driver.maximize_window()
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

# due to restrictions in bot approach, approach through sitemap
url =  "https://ebid.ex.co.kr/ebid/jsps/bbs/sitemap.jsp"
driver.get(url)

# 공개 계약 현황 page 접속
element = driver.find_element_by_xpath('//*[@id="menu2"]/strong/a')
element.click()

# Enter date and search

## Start Date Input
start_date_input = driver.find_element_by_xpath('//*[@id="GGIlJaFR"]')
start_date_input.click()
start_date_input.send_keys(keys.CONTROL, 'a')
pc.copy(start_date)
start_date_input.send_keys(keys.CONTROL, 'v')

time.sleep(1)

## End Date Input
end_date_input = driver.find_element_by_xpath('//*[@id="GGIlJaTO"]')
end_date_input.click()
end_date_input.send_keys(keys.CONTROL, 'a')
pc.copy(end_date)
end_date_input.send_keys(keys.CONTROL, 'v')

## Search Results
search_button = driver.find_element_by_xpath('//*[@id="contents"]/div[3]/form/div/div[11]/button')
search_button.click()

# Retrieve Links in List


count = 0
page_count = 0

#--------------------------------------------------------------------------
# search text through xpath
from lxml import html
def find_by_xpath(element_source,xpath_expression):
    root = html.fromstring(element_source)
    res = root.xpath(xpath_expression+'//text()')
    return res
#--------------------------------------------------------------------------

filename = "contracts.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") 
writer = csv.writer(f)
title = ['발주 구분','공고 번호','계약 명','계약 방법','계약 업체','게약 금액','체결 일자','발주 처','계약 업체 주소지','계약 기간']
writer.writerow(title)

while True:
    try:
        soup_origin = bs(driver.page_source, "lxml")
        accessible_pages = soup_origin.find_all("a", attrs={"title":"페이지 이동"})
        num_of_pages = len(accessible_pages)

        for page in range(0,num_of_pages):
            contracts = []
            next_page_buttons = driver.find_elements_by_xpath("//a[@title='페이지 이동']")
            next_page_button =  next_page_buttons[page]
            time.sleep(1)
            next_page_button.click()

            soup_next = bs(driver.page_source, "lxml") # iteration for safety

            accessible_contracts = soup_next.find_all("td", attrs={"class":"text_r"})
            num_of_accessible_contracts = len(accessible_contracts)
            
            for accessible_contract in range(0, num_of_accessible_contracts):

                category = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[7]/div[1]/table/tbody/tr[{}]/td[1]'.format(accessible_contract+1))
                contract_num = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[7]/div[1]/table/tbody/tr[{}]/td[2]'.format(accessible_contract+1))
                contract_method = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[7]/div[1]/table/tbody/tr[{}]/td[4]'.format(accessible_contract+1))
                contractee = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[7]/div[1]/table/tbody/tr[{}]/td[5]'.format(accessible_contract+1))
                price = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[7]/div[1]/table/tbody/tr[{}]/td[6]'.format(accessible_contract+1))

                #--------------------------Scrape Individual Page------------------------------
                contract = driver.find_element_by_xpath('//*[@id="contents"]/div[7]/div[1]/table/tbody/tr[{}]/td[3]/a'.format(accessible_contract+1))
                contract.click()

                soup_target_page = bs(driver.page_source, "lxml") # target page with raw info
                
                employer = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[1]/h3')
                contract_name = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[2]/table/tbody/tr[10]/td')
                date = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[2]/table/tbody/tr[12]/td')
                contractee_address = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[2]/table/tbody/tr[11]/td/text()[3]')
                contract_period = find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[2]/table/tbody/tr[14]/td/label/text()')+find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[2]/table/tbody/tr[14]/td/label/label/text()')+find_by_xpath(driver.page_source,'//*[@id="contents"]/div[3]/form/div[2]/table/tbody/tr[14]/td/label/label/label')

                # print(find_by_xpath(driver.page_source,'/html/body/div[3]/div[5]/div[2]/div[3]/form/div[2]/table/tbody/tr[14]/td/label/label/text()'))
                driver.back()
                #------------------------------------------------------------------------------
                
                res_temp = [category,contract_num,contract_name,contract_method,contractee,price,date,employer,contractee_address,contract_period]
                writer.writerow(res_temp)

        # print("Cleared Page Set")
        
        if num_of_pages < 10:
            break
        else:
            next_page_set_button = driver.find_element_by_xpath("//a[@title='다음페이지 이동']")
            time.sleep(1)
            next_page_set_button.click()
            page_count = page_count+1
    except AttributeError:
        # print(page_count)
        print("all pages scraped")
        break

print("end of session")
print(page_count)
print(count)

#  soup = bs(driver.page_source, "lxml")

#     company_titles =  soup.find_all("h3", attrs={"class":"title"})
