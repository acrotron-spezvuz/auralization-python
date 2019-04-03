# python 3

import http.client
import urllib.parse
import json

class nafClient():
    def __init__(self):
        self.__auralizationApiEndpoint = "http://name.domain/api/Auralization"
        self.__defaultHeaders = {"Content-Type":"application/json", "Accept":"application/json" }
        
    # send a http request to the api endpoint
    # can be easily changed to http/https
    def __send_request(self, api_endpoint, payload, headers = None):
        print('Send data to ', api_endpoint, payload)
        # check headers
        if headers is None:
            headers = self.__defaultHeaders
        # http / https connection
        connection = http.client.HTTPConnection(self.__auralizationApiEndpoint)        
        # send data
        connection.request("POST", api_endpoint, payload, self.__defaultHeaders)
        # get a response
        response = connection.getresponse()
        # print result        
        print(response.status, response.reason)
        if response.status == 200:
            responseString = response.read().decode('utf-8')
            jsonObj = json.loads(responseString)
            data = jsonObj['data']
            return data 
        # when nothing to return
        return None

    # auralization from source 
    def auralize_from_sources(self, data):
        payload = json.dumps(data)
        endpoint = "/AuralizeFromSources"
        return self.__send_request(endpoint, payload)

    # auralize from url
    def auralize_from_url(self, url):
        headers = {"Content-Type":"application/json", "Accept":"text/palin" }
        endpoint = "/AuralizeFromUrl"
        return self.__send_request(endpoint, url, headers)

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


