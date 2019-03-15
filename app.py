#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 22:29:59 2019

@author: venkatesansubramanian
"""

from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello Tube"
@app.route('/Hello')
def Hello():
    return "Oh boy"
@app.route('/GetAllLineStatus')
def GetAllLineStatus():
    responseValue = ""
    resp = requests.get('https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba')
    for todo_item in resp.json():
        trainName = todo_item['name']
        modelName = todo_item['modeName']
        statusDescription = todo_item['lineStatuses'][0]['statusSeverityDescription']
        responseValue = " " + responseValue + " " + trainName + " " + modelName + " " + statusDescription
    return "Done"
if __name__ == "__main__":
    app.run()
