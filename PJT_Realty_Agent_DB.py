from bs4 import BeautifulSoup as bs
import grequests
import pandas as pd
from selenium import webdriver
import selenium
import time
from bs4 import BeautifulSoup
import requests as rq
import csv
import re

filename = "L9DD_Realty_Agent_DB_run_4.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") 
writer = csv.writer(f)
title = ['시/도','시/군/구','동','No.','성명','상호','구분','직위','상태']
writer.writerow(title)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
url = 'http://www.nsdi.go.kr/lxportal/?menuno=4085'
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(url)
time.sleep(2)

# 중개사/보조원 선택
Specifics_search_element = driver.find_element_by_xpath('//*[@id="shSelect"]')
Specifics_search_element.click()
time.sleep(1)
Specifics_option_element = driver.find_element_by_xpath('//*[@id="shSelect"]/option[2]')
Specifics_option_element.click()
time.sleep(1)

# 출력 개수 선택
Print_quantity_search_element = driver.find_element_by_xpath('//*[@id="searchVO"]/div[1]/div/select')
Print_quantity_search_element.click()
time.sleep(1)
Print_quantity_option_element = driver.find_element_by_xpath('//*[@id="searchVO"]/div[1]/div/select/option[5]')
Print_quantity_option_element.click()
time.sleep(1)

#######################################################

i = 2
first_run = 1

#일원동 13

try :
    while True :
        # 시/도 선택
        ShiDo_search_element = driver.find_element_by_xpath('//*[@id="shSido"]')
        ShiDo_search_element.click()
        time.sleep(1)
        i += 1
        ShiDo_option_element = driver.find_element_by_xpath('//*[@id="shSido"]/option[{}]'.format(i)) # 여기서 option 2부터 18까지
        ShiDo = ShiDo_option_element.text
        ShiDo_option_element.click()
        time.sleep(1)
        j = 1
        try :
            while True :
                # 시/군/구 선택
                Sigungu_search_element = driver.find_element_by_xpath('//*[@id="shSigungu"]')
                Sigungu_search_element.click()
                time.sleep(1)
                j += 1
                Sigungu_option_element = driver.find_element_by_xpath('//*[@id="shSigungu"]/option[{}]'.format(j)) # option 2부터 존재하는 끝까지
                Sigungu = Sigungu_option_element.text
                Sigungu_option_element.click()
                time.sleep(1)
                t = 1
                try :
                    while True :
                        if first_run == 1:
                            t = 10
                        # 동 선택
                        Dong_search_element = driver.find_element_by_xpath('//*[@id="shDong"]')
                        #Dong_search_element.click()
                        driver.execute_script("arguments[0].click();", Dong_search_element) 
                        time.sleep(1)
                        t += 1
                        Dong_option_element = driver.find_element_by_xpath('//*[@id="shDong"]/option[{}]'.format(t))
                        Dong = Dong_option_element.text
                        Dong_option_element.click()
                        time.sleep(1)

                        Search_button_element = driver.find_element_by_xpath('//*[@id="icon_btn_write"]')
                        Search_button_element.click()
                        time.sleep(4)
                        print(i,',',j,',',t)
                        # 페이지 넘기기

                        # 페이지 끝까지 가기
                        page_len_element = driver.find_element_by_xpath('//*[@id="searchVO"]/div[2]/div[1]/p/span').text
                        print(page_len_element)

                        if page_len_element == '':
                            first_run += 1
                            continue
                        else:
                            page_length = int(page_len_element)
                        print(page_length)

                        if page_length < 51:
                            Last_page = driver.current_url
                        else :
                            try :
                                Last_page_element = driver.find_element_by_class_name('page_last')
                                Last_page_element.click()
                                time.sleep(4)
                                Last_page = driver.current_url
                                # 처음으로 오기 
                                driver.back()
                                time.sleep(4)
                            except selenium.common.exceptions.ElementClickInterceptedException1:
                                Last_page = driver.current_url
                        if page_length == 0:
                            first_run += 1
                            print('activated')
                            continue

                        # Data-Scraping

                        while True:
                            source = driver.page_source
                            soup = bs(source, "lxml")

                            data_rows = soup.find("table", attrs={"class":"bl_list"}).find("tbody").find_all("tr")
                            for row in data_rows:
                                serial_number = row.td.get_text()

                                sib = row.td.next_sibling.next_sibling.next_sibling.next_sibling
                                name = sib.get_text()

                                sib = sib.next_sibling.next_sibling
                                shop = sib.get_text()

                                sib = sib.next_sibling.next_sibling
                                job = sib.get_text()

                                sib = sib.next_sibling.next_sibling
                                rank = sib.get_text()

                                sib = sib.next_sibling.next_sibling
                                status = sib.get('title', 'No title attribute')
                                writer.writerow([ShiDo,Sigungu,Dong,serial_number,name,shop,job,rank,status])

                            if  driver.current_url != Last_page:
                                try :
                                    Next_page_element = driver.find_element_by_class_name("page_next")
                                    Next_page_element.click()
                                    first_run += 1
                                    time.sleep(4)
                                except selenium.common.exceptions.ElementClickInterceptedException:
                                    time.sleep(4)
                                    break
                            else:
                                first_run += 1
                                time.sleep(4)
                                break
                except selenium.common.exceptions.NoSuchElementException:
                    time.sleep(4)
                    first_run += 1
                    break
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(4)
            break
except selenium.common.exceptions.NoSuchElementException:    
    print("end of task")
    driver.quit()