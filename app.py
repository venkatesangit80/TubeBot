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
    try:
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
                        statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" & ","-").replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                        subResp = requests.get(statusUrl)
                        for sub_todo_item in subResp.json():
                            response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                            for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                                response_text = response_text + singleAffected['commonName'] + ","
                
                    if "Closed" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                        statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" & ","-").replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                        subResp = requests.get(statusUrl)
                        for sub_todo_item in subResp.json():
                            response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                            for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                                response_text = response_text + singleAffected['commonName'] + ","        
                
                    if "Minor" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                        statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" & ","-").replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                        subResp = requests.get(statusUrl)
                        for sub_todo_item in subResp.json():
                            response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                            for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                                response_text = response_text + singleAffected['commonName'] + ","      
        
                
                    if "Severe" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                        statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" & ","-").replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
                        subResp = requests.get(statusUrl)
                        for sub_todo_item in subResp.json():
                            response_text = response_text + " --- " + sub_todo_item['lineStatuses'][0]['reason'] + " ---- FOR ---- "
                            for singleAffected in sub_todo_item['lineStatuses'][0]['disruption']['affectedStops']:
                                response_text = response_text + singleAffected['commonName'] + ","   
        
                    if "Reduced" in todo_item['lineStatuses'][0]['statusSeverityDescription']:
                        statusUrl = "https://api.tfl.gov.uk/Line/" + todo_item['name'].replace(" & ","-").replace(" ", "-") + "/Status?detail=true&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
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
            return jsonify(reply)
        if(action == "GetCurrentSpot"):
            inputValue = inputValue.replace("and","-")
            inputValue = inputValue.replace("&","-")
            inputValue = inputValue.replace(" ","")
            subInputValue = data['queryResult']['parameters']['subinput']
            response_text_data = GetCurrentSpot(inputValue,subInputValue)
            response_text = GetCurrentSpotCard(inputValue,subInputValue)
            if(response_text == ""):
                response_text = "No Prediction for the " + subInputValue
            reply = {
                    "fulfillmentMessages" : response_text
                    }
            return jsonify(reply)
        if(action == "TestRich"):
            #response_text = GetCurrentSpot(inputValue,subInputValue)
            #response_text = GetCurrentSpotCard(inputValue,subInputValue)
            inputValue = inputValue.replace("and","-")
            inputValue = inputValue.replace("&","-")
            inputValue = inputValue.replace(" ","")
            subInputValue = data['queryResult']['parameters']['subinput']
            response_text_text = GetCurrentSpot(inputValue,subInputValue)
            response_text = GetCurrentSpotCard(inputValue,subInputValue)
            if(response_text == ""):
                response_text = "No Prediction for the " + subInputValue
            #reply = {
            #        "fulfillmentText" : response_text_text,
            #        "fulfillmentMessages" : response_text
            #        }
            reply = {
                    "fulfillmentText" : response_text_text
                    }
            return jsonify(reply)
        if(action == "news"):
            latestNews = LatestNews()
            #latestNews = "Test"
            reply = {
                    "fulfillmentText" : latestNews
                    }
            return jsonify(reply)
        if(action == "abcnews"):
            latestNews = ABCLatestNews()
            #latestNews = "Test"
            reply = {
                    "fulfillmentText" : latestNews
                    }
            return jsonify(reply)    
        if(action == "indianews"):
            latestNews = IndiaLatestNews()
            #latestNews = "Test"
            reply = {
                    "fulfillmentText" : latestNews
                    }
            return jsonify(reply)   
        if(action == "CrickNews"):
            latestNews = CrickNews()
            #latestNews = "Test"
            reply = {
                    "fulfillmentText" : latestNews
                    }
            return jsonify(reply)
        if(action == "TechNews"):
            latestNews = TechNews()
            #latestNews = "Test"
            reply = {
                    "fulfillmentText" : latestNews
                    }
            return jsonify(reply)
        if(action == "Dictionary"):
            wordMeaning = DictionaryInformation(inputValue)
            reply = {
                    "fulfillmentText" : wordMeaning
                    }
            return jsonify(reply)
        if(action == "hindunews"):
            latestNews = HinduNews()
            #latestNews = "Test"
            reply = {
                    "fulfillmentText" : latestNews
                    }
            return jsonify(reply)    
    except ValueError:
        reply = {
                "fulfillmentText" : "Sorry not able to process your request"
                }

@app.route('/GetAllLineStatusGet')
def GetAllLineStatusGet():
    inputValue = "Hammersmith & City"
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

#@app.route('/GetLocationCard')
#def GetCurrentSpotCard():
def GetCurrentSpotCard(lineName,stationName):
    #lineName = "bakerloo"
    #stationName = "Waterloo"
    currentSpotUrl = "https://api.tfl.gov.uk/line/" + lineName + "/arrivals?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
    currentSpotResponse = requests.get(currentSpotUrl)
    returnValue = []
    facebookReturnValue = []
    FulfilmentResponse = []
    lineNo = 0
    for singleSpot in currentSpotResponse.json():
        returnValueSingle = {}
        fullStationName = singleSpot['stationName']
        if stationName.upper() in fullStationName.upper():
            StationName = singleSpot['stationName']
            CurrentLocation = singleSpot['currentLocation']
            ExpectedArrival = singleSpot['expectedArrival']
            PlatformName = singleSpot['platformName']
            destinationName = singleSpot['destinationName']
            #returnValue = returnValue + StationName + " - " + ExpectedArrival + " At Platform " + PlatformName + " Currently " + CurrentLocation + " Destination is " + destinationName + " ----------------------------- "
            FullResponse = {}
            retData = {}
            retData["title"] = "Expected to Arrive At " + str(ExpectedArrival) + " To Station " + StationName + " Currently " + CurrentLocation + ", destination: " + destinationName
            quickReplies = []
            quickReplies.append("Happy Journey")
            retData["quickReplies"] = quickReplies
            FullResponse["quickReplies"] = retData
            if lineNo <= 4:
                FulfilmentResponse.append(FullResponse)
            lineNo = lineNo + 1
    return FulfilmentResponse
    #return jsonify(returnValue)
    

def GetCurrentSpot(lineName, stationName):
    #lineName = "waterloo-city"
    #stationName = "Waterloo"
    currentSpotUrl = "https://api.tfl.gov.uk/line/" + lineName + "/arrivals?app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba"
    currentSpotResponse = requests.get(currentSpotUrl)
    returnValue = ""
    for singleSpot in currentSpotResponse.json():
        fullStationName = singleSpot['stationName']
        if stationName.upper() in fullStationName.upper():
            StationName = singleSpot['stationName']
            CurrentLocation = singleSpot['currentLocation']
            ExpectedArrival = singleSpot['expectedArrival']
            PlatformName = singleSpot['platformName']
            destinationName = singleSpot['destinationName']
            returnValue = returnValue + StationName + " - " + ExpectedArrival + " At Platform " + PlatformName + " Currently " + CurrentLocation + " Destination is " + destinationName + " ----------------------------- "
    return returnValue
    

def GetBikePointDetails(PlaceName):
    bikePointSearchUrl = 'https://api.tfl.gov.uk/BikePoint/Search?query=' + PlaceName + '&app_id=bd38b189&app_key=307678e9c079a6c525da5304098522ba'
    bikeDetailsResponse = requests.get(bikePointSearchUrl)
    bikePoints = ""
    for eachBikeStopDetail in bikeDetailsResponse.json():
        bikePoints = bikePoints + " POINT STOP : " + eachBikeStopDetail['commonName'] + "," 
    reply = { "fulfillmentText" : bikePoints }
    return jsonify(reply)

@app.route('/UkNews')
def LatestNews():
    newsFeed = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=8815e48b03a3457983dd976bd251aafe"
    newsFeedResponse = requests.get(newsFeed)
    newsTitles = ""
    for singleNews in newsFeedResponse.json()['articles']:
        newsTitles = newsTitles + str(singleNews['title']) + " >>>>> "
    return newsTitles

def ABCLatestNews():
    newsFeed = "https://newsapi.org/v2/top-headlines?sources=abc-news&apiKey=8815e48b03a3457983dd976bd251aafe"
    newsFeedResponse = requests.get(newsFeed)
    newsTitles = ""
    for singleNews in newsFeedResponse.json()['articles']:
        newsTitles = newsTitles + str(singleNews['title']) + " >>>>> "
    return newsTitles

@app.route('/IndiaNews')
def IndiaLatestNews():
    newsFeed = "https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey=8815e48b03a3457983dd976bd251aafe"
    newsFeedResponse = requests.get(newsFeed)
    newsTitles = ""
    for singleNews in newsFeedResponse.json()['articles']:
        newsTitles = newsTitles + str(singleNews['title']) + " >>>>> "
    return newsTitles


@app.route('/CricketNews')
def CrickNews():
    newsFeed = "https://newsapi.org/v2/top-headlines?sources=espn-cric-info&apiKey=8815e48b03a3457983dd976bd251aafe"
    newsFeedResponse = requests.get(newsFeed)
    newsTitles = ""
    for singleNews in newsFeedResponse.json()['articles']:
        newsTitles = newsTitles + str(singleNews['title']) + " <<<<< " + str(singleNews["description"]) + " >>>>> "
    return newsTitles

@app.route('/dictionary/<WordToUse>')
def DictionaryInformation(WordToUse):
    url = "https://od-api.oxforddictionaries.com:443/api/v1/entries/en/" + WordToUse
    headers = {
        "app_id" : "b8a7506b",
        "app_key" : "8445b051a6fd19d030a97ca6e48dfa40"
    }
    response = requests.get(url, headers=headers)
    returnValue = ""
    for singleResponse in response.json()['results']:
        print(singleResponse['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0])
        print("----------------------")
        print(singleResponse['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text'])
        returnValue = returnValue + " <<< Defenition : " + singleResponse['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        returnValue = returnValue + " Usage : " + singleResponse['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text'] + ">>>"
    return returnValue
        

@app.route('/TechNews')
def TechNews():
    newsFeed = "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=8815e48b03a3457983dd976bd251aafe"
    newsFeedResponse = requests.get(newsFeed)
    newsTitles = ""
    for singleNews in newsFeedResponse.json()['articles']:
        newsTitles = newsTitles + str(singleNews['title']) + " <<<<< " + str(singleNews["description"]) + " >>>>> "
    return newsTitles

@app.route('/HinduNews')
def HinduNews():
    newsFeed = "https://newsapi.org/v2/top-headlines?sources=the-hindu&apiKey=8815e48b03a3457983dd976bd251aafe"
    newsFeedResponse = requests.get(newsFeed)
    newsTitles = ""
    for singleNews in newsFeedResponse.json()['articles']:
        newsTitles = newsTitles + str(singleNews['title']) + " >>>>> "
    return newsTitles   

@app.route('/PostCode/<postCodeNumber>')
def PostalCode(postCodeNumber):
    postURL = "https://api.postcodes.io/postcodes/" + postCodeNumber
    postUrlResponse = requests.get(postURL)
    postValue = ""
    for singlePost in postUrlResponse.json()['result']:
        postValue = postValue + singlePost + " "
    return postValue
 

if __name__ == "__main__":
    app.run()
