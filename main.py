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





from flask import Flask, request, make_response, jsonify

from GOA_tools import resName2openTime, GOA_booker

import json
from pprint import pprint



app = Flask(__name__)
# log = app.logger


with open('01_data/local_data/theatre.json') as f:
    theatreData = json.load(f)
    
# df = pd.read_csv("01_data/db.csv")

@app.route('/', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhookt
    
       every enabled cover will send post to back-end, we use the name of action to activiate funtion
    """
    
    # print("Reached the server yo!")
    
    req = request.get_json(silent=True, force=True)
    # pprint(req)

    try:
        if 'knowledgeAnswers' in req.get('queryResult'):
            action = 'knowledge_base'
        else:
            action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'
    
    # debug: show me the parameters
    print(f'Action: {action}')
    parameters = req['queryResult']['parameters']
    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))

    if action == 'knowledge_base':
        res = req.get('queryResult').get('knowledgeAnswers').get('answers')[
            0].get('answer')
    elif action == "restaurant":
        res = restaurant(req)
    elif action == "time_confirm":
        res = time_confirm(req)
    elif action == "final_confirm":
        res = final_confirm(req)
    elif action == "theatre":
        res = theatre(req)

    else:
        res = 'My developers screwed up just this once. Please repeat again'
        # log.error('Unexpected action.')

    print('Response: {}'.format(res))

    return make_response(jsonify({'fulfillmentText': res}))


def restaurant(req):
    """
    set the conversation under structural context, the parameters will always be here
    """
    
    parameters = req['queryResult']['parameters']
    name = parameters['restaurantName']

    availableTime = resName2openTime(name)
    
    print('working')

    response = "The available times are " + availableTime + ". Which time do you want me to book?"
    return response


def time_confirm(req):

    try:
        contextParams  = req['queryResult']['outputContexts'][-1]['parameters']
        
        numberPeople = contextParams['num_people']
        restaurantName = contextParams['restaurantName']
        time_original = contextParams['time.original']

    except AttributeError:
        return 'I failed to comply, sorry. I am still a prototype. Try again!'

    return "So, shall I book the reservation for " + numberPeople + \
           " persons at " + restaurantName + " at " + time_original + "?"

def final_confirm(req):
    try:
        contextParams  = req['queryResult']['outputContexts'][-1]['parameters']

        numberPeople = contextParams['num_people']
        restaurantName = contextParams['restaurantName']
        time_original = contextParams['time.original']
        
        GOA_booker(restaurantName, numberPeople, time_original)
       

    except AttributeError:
        return 'I failed to comply, sorry. I am still a prototype. Try again!'

    return "I made a reservation. You should get an email with detail shortly. Want to do anything else later?"


def theatre(req):
    pprint(theatreData)






if __name__ == '__main__':
    app.run(debug=True, port=80)
