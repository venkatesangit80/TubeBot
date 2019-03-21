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
    action = data['queryResult']['action']
    response_text = ""
    if(action == "AllTubeLineStatus"):
        inputValue = inputValue.replace("and","&")
        #input
        responseValue = []
        responseText = "<Table>"
        allLineNames = ""
        resp = requests.get('https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba')
        for todo_item in resp.json():
            if todo_item['name'].upper() == inputValue.upper():
                response_text = response_text + " " + todo_item['name'] + " " + todo_item['lineStatuses'][0]['statusSeverityDescription']
    
                if "Part" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                    statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                    subResp = requests.get(statusUrl)
                    for sub_todo_item in subResp.json():
                        response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                        for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                            response_text = response_text + singleAffected['commonName'] + ","
            
                if "Closed" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                    statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                    subResp = requests.get(statusUrl)
                    for sub_todo_item in subResp.json():
                        response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                        for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                            response_text = response_text + singleAffected['commonName'] + ","        
            
                if "Minor" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                    statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                    subResp = requests.get(statusUrl)
                    for sub_todo_item in subResp.json():
                        response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                        for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                            response_text = response_text + singleAffected['commonName'] + ","      
    
            
                if "Severe" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                    statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                    subResp = requests.get(statusUrl)
                    for sub_todo_item in subResp.json():
                        response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                        for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                            response_text = response_text + singleAffected['commonName'] + ","   
    
                if "Reduced" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                    statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                    subResp = requests.get(statusUrl)
                    for sub_todo_item in subResp.json():
                        response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                        for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                            response_text = response_text + singleAffected['commonName'] + ","      
    
            allLineNames = allLineNames + todo_item['name'] + ","
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
            response_text = "Line " + inputValue + " Not Found. The available lines are : " + allLineNames
    if(action == "GetCurrentSpot"):
        subInputValue = data['queryResult']['parameters']['subinput']
        response_text = GetCurrentSpot(inputValue,subInputValue)
    reply = {
        "fulfillmentText" : response_text
    }
        
    return jsonify(reply)

@app.route('/GetAllLineStatusGet')
def GetAllLineStatusGet():
    inputValue = "London Overground"
    inputValue = inputValue.replace("and","&")
    #input
    responseValue = []
    responseText = "<Table>"
    response_text = ""
    allLineNames = ""
    resp = requests.get('https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba')
    for todo_item in resp.json():
        if todo_item['name'].upper() == inputValue.upper():
            response_text = response_text + " " + todo_item['name'] + " " + todo_item['lineStatuses'][0]['statusSeverityDescription']

            if "Part" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                subResp = requests.get(statusUrl)
                for sub_todo_item in subResp.json():
                    response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                    for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                        response_text = response_text + singleAffected['commonName'] + ","
        
            if "closed" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                subResp = requests.get(statusUrl)
                for sub_todo_item in subResp.json():
                    response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                    for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                        response_text = response_text + singleAffected['commonName'] + ","        
        
            if "minor" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                subResp = requests.get(statusUrl)
                for sub_todo_item in subResp.json():
                    response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                    for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                        response_text = response_text + singleAffected['commonName'] + ","      


            if "Reduced" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                subResp = requests.get(statusUrl)
                for sub_todo_item in subResp.json():
                    response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                    for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                        response_text = response_text + singleAffected['commonName'] + ","      


        allLineNames = allLineNames + todo_item['name'] + ","
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
        response_text = "Line " + inputValue + " Not Found. The available lines are : " + allLineNames
    reply = {
        "fulfillmentText" : response_text
    }
    #reply = {
    #    "fulfillmentText" : str(inputValue)
    #}
    #return responseText
    return jsonify(reply)


def GetCurrentSpot(lineName, stationName):
    #lineName = "waterloo-city"
    #stationName = "Waterloo"
    currentSpotUrl = "https://api.tfl.gov.uk/line/" + lineName + "/arrivals?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
    currentSpotResponse = requests.get(currentSpotUrl)
    returnValue = ""
    for singleSpot in currentSpotResponse.json():
        fullStationName = singleSpot['stationName']
        if stationName in fullStationName:
            StationName = singleSpot['stationName']
            CurrentLocation = singleSpot['currentLocation']
            ExpectedArrival = singleSpot['expectedArrival']
            PlatformName = singleSpot['platformName']
            returnValue = returnValue + "For " + StationName + " The time of arrival is " + ExpectedArrival + " At Platform " + PlatformName + " The Train is " + CurrentLocation + ","
    return returnValue
    

def GetBikePointDetails(PlaceName):
    bikePointSearchUrl = 'https://api.tfl.gov.uk/BikePoint/Search?query=' + PlaceName + '&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba'
    bikeDetailsResponse = requests.get(bikePointSearchUrl)
    bikePoints = ""
    for eachBikeStopDetail in bikeDetailsResponse.json():
        bikePoints = bikePoints + " POINT STOP : " + eachBikeStopDetail['commonName'] + "," 
    reply = { "fulfillmentText" : bikePoints }
    return jsonify(reply)

if __name__ == "__main__":
    app.run()
