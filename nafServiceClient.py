# python

import http.client
import urllib.parse
import json

class nafClient():
    def __init__(self):
        self.auralizationApiEndpoint = "http://name.domain/api/Auralization"
        self.defaultHeaders = {"Content-Type":"application/json", "Accept":"application/json" }
        

    def __send_request(self, api_endpoint, payload):
        connection = http.client.HTTPConnection(self.auralizationApiEndpoint)
        connection.request("POST", api_endpoint, payload, self.defaultHeaders)
        response = connection.getresponse()
        print(response.status, response.reason)
        if response.status == 200:
            responseString = response.read().decode('utf-8')
            jsonObj = json.loads(responseString)
            data = jsonObj['data']
            return data 
        return None

    # auralization from source 
    def auralize_from_sources(self, data):
        payload = json.dumps(data)
        endpoint = "/AuralizeFromSources"
        return self.__send_request(endpoint, payload)

    # auralize from url
    def auralize_from_url(self, url):
        # quote it 
        quoted_url = urllib.parse.quote(url)
        endpoint = "/AuralizeFromUrl"
        self.__send_request(endpoint, quoted_url)
        return quoted_url

    # auralize from content
    def auralize_from_content(self, data):
        payload = json.dumps(data)
        endpoint = "/AuralizeFromContent"
        return self.__send_request(endpoint, payload)

    # auralize from environmet
    def auralize_from_environment(self, data):
        payload = json.dumps(data)
        endpoint = "/AuralizeFromEnvironment"
        return self.__send_request(endpoint, payload)

