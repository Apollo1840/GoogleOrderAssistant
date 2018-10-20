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
import requests
from requests.exceptions import ReadTimeout
import random

df = pd.read_csv("db.csv")
app = Flask(__name__)
log = app.logger


@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook

    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    req = request.get_json(silent=True, force=True)
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
    else:
        res = 'My developers screwed up just this once. Please repeat again'
        log.error('Unexpected action.')

    print('Response: {}'.format(res))

    return make_response(jsonify({'fulfillmentText': res}))


def givenTime(req):
    pass


def confirm(req):
    pass

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

    name = parameters['restaurantName']
    people = parameters['num_people']

    if not name or not people:
        return

    time = resName2openTime(name)


    response = "The available times are " + time + ". Which time do you want me to book?"
    return response


def resName2openTime(search_string):
    restaurant = search_string.replace(' ', '+')

    covers = 2  # number of people
    date_time = '2018-10-20'  # it has to be this form
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


def weather(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information

    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """
    parameters = req['queryResult']['parameters']

    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(parameters)
    if error:
        return error

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    # If the user requests a datetime period (a date/time range), get the
    # response
    if forecast.datetime_start and forecast.datetime_end:
        response = forecast.get_datetime_period_response()
    # If the user requests a specific datetime, get the response
    elif forecast.datetime_start:
        response = forecast.get_datetime_response()
    # If the user doesn't request a date in the request get current conditions
    else:
        response = forecast.get_current_response()

    return response


def weather_activity(req):
    """Returns a string containing text with a response to the user
    with a indication if the activity provided is appropriate for the
    current weather or a prompt for more information

    Takes a city, activity and (optional) dates
    uses the template responses found in weather_responses.py as templates
    and the activities listed in weather_entities.py
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # Check to make sure there is a activity, if not return an error
    if not forecast_params['activity']:
        return 'What activity were you thinking of doing?'

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    # get the response
    return forecast.get_activity_response()


def weather_condition(req):
    """Returns a string containing a human-readable response to the user
    with the probability of the provided weather condition occurring
    or a prompt for more information

    Takes a city, condition and (optional) dates
    uses the template responses found in weather_responses.py as templates
    and the conditions listed in weather_entities.py
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # Check to make sure there is a activity, if not return an error
    if not forecast_params['condition']:
        return 'What weather condition would you like to check?'

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    # get the response
    return forecast.get_condition_response()


def weather_outfit(req):
    """Returns a string containing text with a response to the user
    with a indication if the outfit provided is appropriate for the
    current weather or a prompt for more information

    Takes a city, outfit and (optional) dates
    uses the template responses found in weather_responses.py as templates
    and the outfits listed in weather_entities.py
    """

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(req['queryResult']['parameters'])
    if error:
        return error

    # Validate that there are the required parameters to retrieve a forecast
    if not forecast_params['outfit']:
        return 'What are you planning on wearing?'

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    return forecast.get_outfit_response()


def weather_temperature(req):
    """Returns a string containing text with a response to the user
    with a indication if temperature provided is consisting with the
    current weather or a prompt for more information

    Takes a city, temperature and (optional) dates.  Temperature ranges for
    hot, cold, chilly and warm can be configured in config.py
    uses the template responses found in weather_responses.py as templates
    """

    parameters = req['queryResult']['parameters']

    # validate request parameters, return an error if there are issues
    error, forecast_params = validate_params(parameters)
    if error:
        return error

    # If the user didn't specify a temperature, get the weather for them
    if not forecast_params.get('temperature'):
        return weather(req)

    # create a forecast object which retrieves the forecast from a external API
    try:
        forecast = Forecast(forecast_params)
    # return an error if there is an error getting the forecast
    except (ValueError, IOError) as error:
        return error

    return forecast.get_temperature_response()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
