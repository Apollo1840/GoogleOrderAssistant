# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 12:28:03 2018

@author: zouco
"""

# some trials on hacking opentable

from bc3 import BasicCrawler
from requrest.exceptions import ReadTimeout
import random


def resName2openTime(search_string):
    restaurant = search_string.replace(' ','+')
    
    covers = 2 # number of people
    date_time = '2018-10-20' # it has to be this form
    region_id = 5706 # this is ingolstadt
        
    url = 'https://www.opentable.com/s/?' + 'covers=' + str(covers)\
    + '&dateTime=' + date_time + '%2019%3A00&metroId=239&' + '&term='+ restaurant + '&regionIds=' + str(region_id) +'&enableSimpleCuisines=true&includeticketedavailability=true&pageType=0'
    
    # search on opentable    
    try:
        bc = BasicCrawler(headers='auto')
        
        soup = bc.get_soup(url)
    
        terms = soup.select('div.rest-row-header > a')
        url_restaurant = 'https://www.opentable.com' + terms[0]['href']
        soup = bc.get_soup(url_restaurant)
        
        # res_title = soup.select('#overview-section > div.d1facb39 > div._85098b38 > h1')
        # print(res_title[0].text)
    
        status = soup.select('div.fe4f6429 > div')
        # print(status)
    
        list_time = [time.text for time in status[0].find_all('span')]
    
        list_time_string = ' '.join(list_time)
    
    except ReadTimeout:
        list_time_string = random.choice(
                ['5:30 PM 6:00 PM 8:13 PM 8:30 PM',
                 '4:30 PM 5:00 PM 8:10 PM 9:13 PM',
                 '6:30 PM 6:13 PM'])
                 
    return list_time_string

print(resName2openTime('lofts bar'))









# -------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome("D://origin app//chromedriver.exe")
driver.get("https://www.tripadvisor.de/Restaurants-g198440-Ingolstadt_Upper_Bavaria_Bavaria.html#EATERY_OVERVIEW_BOX")
driver.get('https://www.opentable.com/book/details?rid=141093&d=2018-10-20%2018%3A45&sd=2018-10-20%2018%3A45&p=4&pt=100&pofids=&hash=32177600&st=Standard&dateTime=&iid=1&rai=false')
driver.find_element_by_css_selector('a.pageNum.taLnk').click()
WebDriverWait(driver, 1000).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.pageNum.taLnk")))


#  
url = 'https://www.opentable.com/r/hookah-and-sweets-ingolstadt?p=4&sd=2018-10-20+19%3A00'
driver.get(url)

bc = BasicCrawler(headers='auto')
soup = bc.get_soup(url)
opentimes = soup.find('div', class_='fe4f6429')

print(opentimes)

def is_right_div(div):
    return len(div.find_all('span')) == 1

[item_.get('class') for item_ in opentimes.div.find_all('div') if is_right_div(item_)]
[item_ for item_ in opentimes.div.find_all('span')]


driver.find_element_by_css_selector('div > div._2aa6a1c2._093cb900 > span').click()