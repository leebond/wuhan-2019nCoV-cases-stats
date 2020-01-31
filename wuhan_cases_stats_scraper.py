# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 12:43:11 2020

@author: david
"""

import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

### download chrome driver from https://chromedriver.chromium.org/ 
driver = webdriver.Chrome('C:/Users/david/Documents/chromedriver/chromedriver.exe')
http = "https://bnonews.com/index.php/2020/01/the-latest-coronavirus-cases/"
driver.get(http)


def getCorrectRows(row):
    row_list = row.split(' ')
    if len(row_list) != 5:
        return
    else:
        return row_list

filename = 'wuhan.csv'
if filename not in os.listdir():
    df = pd.DataFrame(columns=['City', 'Cases', 'Deaths','Date Updated'])
else:
    df = pd.read_csv('wuhan.csv')

last_updated_datetime = driver.find_element_by_xpath('//*[@id="mvp-content-main"]/p[3]/em').text
updated_dt = re.findall('\d+ \w+ \d+', last_updated_datetime)[0]

tbls_xpath = '//*[@id="mvp-content-main"]/table[*]'
tbls = driver.find_elements_by_xpath(tbls_xpath)
print(len(tbls))
for i in range(len(tbls)): # tr
    rows_xpath = '//*[@id="mvp-content-main"]/table[' + str(i+1) + ']/tbody/tr[*]'
    rows = driver.find_elements_by_xpath(rows_xpath)
    print(len(rows))
    for j in range(len(rows)): # td
        city_xpath = '//*[@id="mvp-content-main"]/table['+str(i+1)+']/tbody/tr['+str(j+1)+']/td['+str(1)+']'
        cases_xpath = '//*[@id="mvp-content-main"]/table['+str(i+1)+']/tbody/tr['+str(j+1)+']/td['+str(2)+']'
        death_xpath = '//*[@id="mvp-content-main"]/table['+str(i+1)+']/tbody/tr['+str(j+1)+']/td['+str(3)+']'
        city = driver.find_element_by_xpath(city_xpath).text
        ncases = driver.find_element_by_xpath(cases_xpath).text
        ndeaths = driver.find_element_by_xpath(death_xpath).text
        if city not in ['MAINLAND CHINA','REGIONS', 'INTERNATIONAL', 'TOTAL']:
            df = df.append({'City': city, 'Cases': ncases, 'Deaths': ndeaths, 'Date Updated': updated_dt}, ignore_index = True)

print(df.head())
df.to_csv('wuhan.csv', index=False)
driver.close()   