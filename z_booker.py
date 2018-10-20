# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 20:22:18 2018

@author: zouco
"""

# booker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pickle

# train the cookie
driver = webdriver.Chrome("D://origin app//chromedriver.exe")
url = 'https://www.opentable.com/r/hookah-and-sweets-ingolstadt?p=4'
driver.get(url)

# stop here
cookies = driver.get_cookies()
with open('cookies.pkl','wb') as f:
   pickle.dump(cookies, f)



#---------------------------------- 

# start the driver
driver = webdriver.Chrome("D://origin app//chromedriver.exe")

# enable cookie injuction
url = 'https://www.google.com'
driver.get(url)

# insert cookies   
with open('cookies.pkl','rb') as f:
   cookies = pickle.load(f)

for cookie in cookies:
    driver.add_cookie(cookie)

# know go
url = 'https://www.opentable.com/r/hookah-and-sweets-ingolstadt?p=4'
driver.get(url)
driver.find_element_by_css_selector('div._92fe4c24 > div._5a483512 > div.af5c29c4 > button').click()    

time_css = 'div.fe4f6429 > div > div:nth-child(1) > div > div._2aa6a1c2._093cb900 > span'
driver.find_element_by_css_selector(time_css).click()

driver.find_element_by_xpath('//*[@id="firstName"]').sendKeys('max')
driver.find_element_by_xpath('//*[@id="lastName"]').sendKeys('musterman')



# ....





# old code
# ---------------------------------------------------------------------



url = 'https://www.opentable.com/the-grill-im-kunstlerhaus'
url = 'https://www.opentable.com/book/details?rid=92667&d=2018-10-20%2021%3A15&sd=2018-10-20%2021%3A15&p=2&pt=100&pofids=&hash=2330406103&st=Standard&dateTime=&iid=2&rai=false'

url = 'https://www.opentable.com/r/hookah-and-sweets-ingolstadt?p=4'
driver.get(url)
driver.find_element_by_css_selector('div._92fe4c24 > div._5a483512 > div.af5c29c4 > button').click()


url = 'https://www.google.com'
driver.get(url)
driver.add_cookie({'name': 'notice_preferences', 'value': '2:', 'domain' : '.opentable.de'})
driver.add_cookie({'name': 'notice_gdpr_prefs', 'value': '0,1,2:', 'domain' : '.opentable.de'})


driver.get("https://www.tripadvisor.de/Restaurants-g198440-Ingolstadt_Upper_Bavaria_Bavaria.html#EATERY_OVERVIEW_BOX")
driver.get('https://www.opentable.com/book/details?rid=141093&d=2018-10-20%2018%3A45&sd=2018-10-20%2018%3A45&p=4&pt=100&pofids=&hash=32177600&st=Standard&dateTime=&iid=1&rai=false')
driver.find_element_by_css_selector('a.pageNum.taLnk').click()
WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.pageNum.taLnk")))





#  

url = 'https://www.opentable.com/r/hookah-and-sweets-ingolstadt?p=4&sd=2018-10-20+19%3A00'
driver.get(url)

'''
bc = BasicCrawler(headers='auto')
soup = bc.get_soup(url)
opentimes = soup.find('div', class_='fe4f6429')

print(opentimes)

def is_right_div(div):
    return len(div.find_all('span')) == 1

[item_.get('class') for item_ in opentimes.div.find_all('div') if is_right_div(item_)]
[item_ for item_ in opentimes.div.find_all('span')]
'''

driver.find_element_by_css_selector('div > div._2aa6a1c2._093cb900 > span').click()