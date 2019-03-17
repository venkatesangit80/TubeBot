#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:29:59 2019

@author: venkatesansubramanian
"""

from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Tube"
@app.route('/Hello')
def Hello():
    return "Oh boy"
@app.route('/GetAllLineStatus', methods = ['POST'])
def GetAllLineStatus():
    data = request.get_json(silent=True)
    inputValue = data['queryResult']['parameters']['input']
    #input
    responseValue = []
    responseText = "<Table>"
    response_text = ""
    resp = requests.get('https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba')
    for todo_item in resp.json():
        if todo_item['name'] == inputValue:
            response_text = response_text + " Line " + todo_item['name'] + " Status Is - " + todo_item['lineStatuses'][0]['statusSeverityDescription'] + " , "
        responseText = responseText + "<tr>"
        trainLineDetails = {}
        trainLineDetails['LineName'] = todo_item['name']
        responseText = responseText + "<td>" + todo_item['name'] + "</td>"
        trainLineDetails['ModelName'] = todo_item['modeName']
        responseText = responseText + "<td>" + todo_item['modeName'] + "</td>"
        trainLineDetails['StatusDescription'] = todo_item['lineStatuses'][0]['statusSeverityDescription']
        responseText = responseText + "<td>" + todo_item['lineStatuses'][0]['statusSeverityDescription'] + "</td>"
        responseValue.append(trainLineDetails)
        responseText = responseText + "</tr>"
        #response_text = response_text + " Line " + todo_item['name'] + " Status Is - " + todo_item['lineStatuses'][0]['statusSeverityDescription'] + " , "
    responseText = responseText + "</table>"
    if response_text == "":
        response_text = "Line " + inputValue + " Not Found"
    reply = {
        "fulfillmentText" : response_text
    }
    #reply = {
    #    "fulfillmentText" : str(inputValue)
    #}
    #return responseText
    return jsonify(reply)

if __name__ == "__main__":
    app.run()
