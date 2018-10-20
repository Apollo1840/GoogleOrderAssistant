# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 12:28:03 2018

@author: zouco
"""

# some trials on hacking opentable

from bc3 import BasicCrawler

covers = 2 # number of people
date_time = '2018-10-20' # it has to be this form
region_id = 5706 # this is ingolstadt
search_words = ['lofts', 'bar']
restaurant = '+'.join(search_words)


url = 'https://www.opentable.com/s/?' + 'covers=' + str(covers)\
+ '&dateTime=' + date_time + '%2019%3A00&metroId=239&' + '&term= '+ restaurant + '&regionIds=' + str(region_id) +'&enableSimpleCuisines=true&includeticketedavailability=true&pageType=0'


print(url)



bc = BasicCrawler(headers='auto')

soup = bc.get_soup(url)

terms = soup.select('div.rest-row-header > a')

url_restaurant = 'https://www.opentable.com' + terms[0]['href']

soup = bc.get_soup(url_restaurant)

res_title = soup.select('#overview-section > div.d1facb39 > div._85098b38 > h1')

print(res_title[0].text)

status = soup.select('div.fe4f6429 > div')

print(status)


list_time = [time.text for time in status[0].find_all('span')]
print(list_time)




# 
# div.rest-row-header > a > span.rest-row-name-text

# print(soup)
