# python

#import urllib.request
import http.client
import urllib.parse
import json

class nafClient():
    def __init__(self):
        self.auralizationApiEndpoint = "http://name.domain/api"
        self.defaultHeaders = {"Content-Type":"application/json", "Accept":"application/json" }
        

    def auralize(self):
        connection = http.client.HTTPConnection(self.auralizationApiEndpoint)
        requestPayload = {}
        connection.request("POST", "/Auralization", requestPayload, self.defaultHeaders)
        response = connection.getresponse()
        print(response.status, response.reason)
        


