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

print(resName2openTime('lofts bar'))









