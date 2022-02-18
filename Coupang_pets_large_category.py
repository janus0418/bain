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
from selenium.webdriver import Edge
import pyperclip as pc
import time
import re
from msedge.selenium_tools import EdgeOptions


# make Edge headless
# edge_options = EdgeOptions()
# edge_options.use_chromium = True  # if we miss this line, we can't make Edge headless
# # A little different from Chrome cause we don't need two lines before 'headless' and 'disable-gpu'
# edge_options.add_argument('headless')
# edge_options.add_argument('disable-gpu')
driver = Edge("C:/Users/hp/Desktop/석승훈/Coding/.vscode/msedgedriver.exe")
#--------------------------------------------------------------------
# Headless Chrome 
# options = wd.ChromeOptions()
# options.headless = True
# options.add_argument("window-size=1920x1080") #화면에 안 뛰우므로 내부적으로 설정할 화면 크기 제시
# driver = wd.Chrome(options = options)
# driver.maximize_window()
#--------------------------------------------------------------------
url = "https://catpre.com/"
driver.get(url)

# //*[@id="__next"]/div[1]/div[1]/ul/li[1]
# //*[@id="__next"]/div[1]/div[1]/ul/li[2]

# element = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/ul/li[4]')
element = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/header/div[2]/div/div/div/div/nav/div[1]/div/div/a[1]')
element.click()

# for category_index in range(1,11):
#     element = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div[1]/ul/li[{}]'.format(category_index))
#     element.click()
#     current_url = driver.page_source
#     # print(current_url)

# def page_url(page_num):
#     return driver.page_source+"?page="+page_num

# for category_index in range(1,11):
#     element = driver.find_element_by_xpath('//*[@id="searchCategoryComponent"]/ul/li[{}]/label'.format(category_index))
#     element.click()
#     page_num=0
#     while True:
#         page_num+=1
#         driver.get(page_url(page_num), headers=headers)