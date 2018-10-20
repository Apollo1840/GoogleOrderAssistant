# -*- coding:utf8 -*-
# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import json

from flask import Flask, request, make_response, jsonify

from forecast import Forecast, validate_params
from bc3 import BasicCrawler
import pandas as pd
from requests.exceptions import ReadTimeout
import random
from pprint import pprint
import pickle

from selenium import webdriver
import selenium.webdriver.support.ui as ui





df = pd.read_csv("db.csv")
app = Flask(__name__)
log = app.logger

time = ""
name = ""
people = 2


with open('local_data/theatre.json') as f:
    theatreData = json.load(f)


# # selenium
# driver = webdriver.Chrome("/usr/local/bin/chromedriver")
# url = 'https://www.opentable.de/r/hookah-and-sweets-ingolstadt?p=4'
# driver.get(url)
#
# # stop here
# cookies = driver.get_cookies()
# with open('cookies.pkl','wb') as f:
#     pickle.dump(cookies, f)


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    pprint("Reached the server yo!")
    req = request.get_json(silent=True, force=True)
    # pprint(req)

    try:
        if 'knowledgeAnswers' in req.get('queryResult'):
            action = 'knowledge_base'
        else:
            action = req.get('queryResult').get('action')
        print(f'Action: {action}')
    except AttributeError:
        return 'json error'

    parameters = req['queryResult']['parameters']
    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))

    if action == 'knowledge_base':
        res = req.get('queryResult').get('knowledgeAnswers').get('answers')[
            0].get('answer')
    elif action == "restaurant":
        res = restaurant(req)
    elif action == "time_confirm":
        res = givenTime(req)
    elif action == "final_confirm":
        res = confirm(req)
    elif action == "abc":
        res = playAround(req)
    elif action == "theatre":
        res = theatre(req)

    else:
        res = 'My developers screwed up just this once. Please repeat again'
        log.error('Unexpected action.')

    print('Response: {}'.format(res))

    return make_response(jsonify({'fulfillmentText': res}))


def playAround(req):
    pprint(req)
    parameters = req['queryResult']['parameters']

    pprint(parameters)


def givenTime(req):

    try:
        parameters = req['queryResult']['parameters']

        pprint(req)

        contextParams  = req['queryResult']['outputContexts'][-1]['parameters']


        numberPeople = contextParams['num_people']
        restaurantName = contextParams['restaurantName']
        time_original = contextParams['time.original']

        # validate request parameters, return an error if there are issues
        error, forecast_params = validate_params(parameters)
        if error:
            return error
        print(time)

    except AttributeError:
        return 'I failed to comply, sorry. I am still a prototype. Try again!'

    return "So, shall I book the reservation for " + numberPeople + \
           " persons at " + restaurantName + " at " + time_original + "?"

def confirm(req):
    try:
        parameters = req['queryResult']['parameters']

        pprint(req)

        contextParams  = req['queryResult']['outputContexts'][-1]['parameters']


        numberPeople = contextParams['num_people']
        restaurantName = contextParams['restaurantName']
        time_original = contextParams['time.original']

        # validate request parameters, return an error if there are issues
        error, forecast_params = validate_params(parameters)
        if error:
            return error
        
        
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

    except AttributeError:
        return 'I failed to comply, sorry. I am still a prototype. Try again!'

    return "I made a reservation. You should get an email with detail shortly. Want to do anything else later?"

def theatre(req):
    pprint(theatreData)


def restaurant(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information

    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """
    parameters = req['queryResult']['parameters']

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(parameters)
    if error:
        return error

    global name
    name = parameters['restaurantName']
    global people
    people = parameters['num_people']

    if not name or not people:
        return

    availableTime = resName2openTime(name)


    response = "The available times are " + availableTime + ". Which time do you want me to book?"
    return response


def resName2openTime(search_string):
    restaurant = search_string.replace(' ', '+')

    covers = 2  # number of people
    date_time = '2018-10-22'  # it has to be this form
    region_id = 5706  # this is ingolstadt

    url = 'https://www.opentable.com/s/?' + 'covers=' + str(covers) \
          + '&dateTime=' + date_time + '%2019%3A00&metroId=239&' + '&term=' + restaurant + '&regionIds=' + str(
        region_id) + '&enableSimpleCuisines=true&includeticketedavailability=true&pageType=0'
    print(url)
    # search on opentable
    try:
        bc = BasicCrawler(headers='auto')

        soup = bc.get_soup(url)

        terms = soup.select('div.rest-row-header > a')
        url_restaurant = 'https://www.opentable.com' + terms[0]['href']

        print(url_restaurant)

        soup = bc.get_soup(url_restaurant)

        # res_title = soup.select('#overview-section > div.d1facb39 > div._85098b38 > h1')
        # print(res_title[0].text)


        status = soup.select('div.fe4f6429 > div')
        print(status)

        list_time = [time.text for time in status[0].find_all('span')]

        list_time_string = ' '.join(list_time)

    except ReadTimeout:
        list_time_string = random.choice(
            ['5:30 PM 6:00 PM 8:13 PM 8:30 PM',
             '4:30 PM 5:00 PM 8:10 PM 9:13 PM',
             '6:30 PM 6:13 PM'])

    return list_time_string




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
