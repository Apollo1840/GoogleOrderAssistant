# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 22:43:43 2018

@author: zouco
"""

from requests.exceptions import ReadTimeout
import random
from bc3 import BasicCrawler

from selenium import webdriver
import selenium.webdriver.support.ui as ui
import pickle

def resName2openTime(search_string):
    restaurant = search_string.replace(' ','+')
    
    covers = 2 # number of people
    date_time = '2018-10-20' # it has to be this form
    region_id = 5706 # this is ingolstadt
        
    url = 'https://www.opentable.com/s/?' + 'covers=' + str(covers)\
    + '&dateTime=' + date_time + '%2019%3A00&metroId=239&' + '&term='+ restaurant + '&regionIds=' + str(region_id) +'&enableSimpleCuisines=true&includeticketedavailability=true&pageType=0'
    
    # search on opentable
    list_time_string = '5:30 PM 6:00 PM 8:13 PM 8:30 PM' 
    try:
        bc = BasicCrawler(headers='auto')
        
        soup = bc.get_soup(url)
    
        terms = soup.select('div.rest-row-header > a')
        url_restaurant = 'https://www.opentable.com' + terms[0]['href']
        # print(url_restaurant)
        
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

def GOA_booker(restaurantName, numberPeople, time_original):
    
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
        
        print(1, restaurantName)
        restaurantName = '-'.join(restaurantName)
        print(2, restaurantName)
        
        print(1, numberPeople)
        numberPeople = numberPeople.split(' ')[0]
        print(2, numberPeople)
        
        print(1, time_original)
        time_original= time_original.split('T')[0]
        print(2,time_original)
        
        url = 'https://www.opentable.de/r/{}?p={}&sd={}'.format(restaurantName,numberPeople,time_original)
        print(url)
        
        driver.get(url)
        
        # to do : check the time
        
        time_btn_css = 'div.fe4f6429 > div > div:nth-child(1) > div > div._2aa6a1c2._093cb900 > span'
        wait = ui.WebDriverWait(driver,10)
        wait.until(lambda driver: driver.find_element_by_css_selector(time_btn_css))
        driver.find_element_by_css_selector(time_btn_css).click()
        
        wait = ui.WebDriverWait(driver,10)
        wait.until(lambda driver: driver.find_element_by_xpath('//*[@id="firstName"]'))
        
        
        first_name = 'max'
        last_name = 'musterman'
        phone_number = '15234723254'
        email = 'c.vlaicu17@gmail.com'
        
        driver.find_element_by_xpath('//*[@id="firstName"]').send_keys(first_name)
        driver.find_element_by_xpath('//*[@id="lastName"]').send_keys(last_name)
        driver.find_element_by_xpath('//*[@id="phone-country-input"]/div/div[2]/input').send_keys(phone_number)
        driver.find_element_by_xpath('//*[@id="form-details"]/fieldset/div[2]/div[2]/input').send_keys(email)
                
        # driver.find_element_by_xpath('//*[@id="btn-complete"]').click()


def train_cookies():
    driver = webdriver.Chrome("D://origin app//chromedriver.exe")
    url = 'https://www.opentable.de/r/hookah-and-sweets-ingolstadt?p=4'
    driver.get(url)
    
    # stop here
    cookies = driver.get_cookies()
    with open('cookies.pkl','wb') as f:
       pickle.dump(cookies, f)


def get_top_n_tags(soup, n):

	top_tags = [e.text for e in soup.find('ul', class_ ='oc-reviews-0cfa0da3').find_all('li')]
	return top_tags[:3] + top_tags[4:n+1]


def get_additional(soup, tags=[]):
	res = {t : "" for t in tags}
	for e in soup.find_all('div', class_='_1e864f49'):
		attribute = e.find('span')
		if attribute.text in tags:
			attribute_val = e.find('div', class_='_16c8fd5e _1f1541e1')
			if attribute_val != None:
				res[attribute.text] = attribute_val.text
	return res



if __name__ == '__main__':
    print(resName2openTime('lofts bar'))