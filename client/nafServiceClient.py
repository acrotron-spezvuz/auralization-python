# python 3

import http.client
import requests
import sys
import os
import ssl
import json
from pathlib import Path
from model.environment import Environment


class nafClient():
    def __init__(self):
        # replace value with valid endpoints
        self.__auralizationApiHost = "auralize.acrotron.com"
        #self.__auralizationApiHost = "localhost"
        self.__auralizationApiPort = "443"
        self.__auralizationApiRoot = "/api/Auralization"
        self.__defaultHeaders = {"Content-Type":"application/json", "Accept":"application/json" }
        
    # send a http request to the api endpoint
    # can be easily changed to http/https
    def __send_request(self, api_endpoint, payload, headers = None):
        print('Send data to ', api_endpoint, payload)
        # check headers
        if headers is None:
            headers = self.__defaultHeaders
        # http / https connection
        connection = http.client.HTTPSConnection(host=self.__auralizationApiHost, port = self.__auralizationApiPort, context=ssl._create_unverified_context())
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
        if response.status == 400:
            responseString = response.read().decode('utf-8')
            jsonObj = json.loads(responseString)
            print(responseString)
            #data = jsonObj['data']
            return None 
        # when nothing to return
        return None

    # auralization from source 
    def auralize_from_sources(self, data):
        payload = json.dumps(data)
        endpoint = self.__auralizationApiRoot + "/AuralizeFromSources"
        return self.__send_request(endpoint, payload)

    # auralize from url
    def auralize_from_url(self, url):
        headers = {"Content-Type":"text/palin", "Accept":"application/json"}
        endpoint = self.__auralizationApiRoot + "/AuralizeFromUrl"
        return self.__send_request(endpoint, url, headers)

    # auralize from content and file
    def auralize_from_content_and_files(self, data, filenames):
        print(filenames)
        #self.upload_files(filenames)

        url = "https://" + self.__auralizationApiHost + ":" + self.__auralizationApiPort + "/" + \
              self.__auralizationApiRoot + "/AuralizeFromContentAndFiles"

        def convert(name):
            return ("files", (os.path.basename(name), open(name, 'rb')))

        response = requests.post(url, files=list(map(convert, filenames)), data=data, verify=False)

        #wav = json.dumps(response.content)
        wav = str(response.content, 'utf-8')

        resp = json.loads(wav)["data"]
        return resp

    # auralize from content
    # workaround: to utilize AuralizeFromSources
    # until AuralizeFromContent is fixed.
    def auralize_from_content3(self, content, wav_len: float):
        # upload associated files first
        associated_files = self.extract_files(content)
        print(associated_files)
        #self.upload_files(associated_files)

        resp = self.auralize_from_content_and_files({"content":content, "wavLength": wav_len }, associated_files)
        resp = "https://" + self.__auralizationApiHost + ":" + self.__auralizationApiPort + resp[2:]
        return resp;

    # auralize from content
    def auralize_from_content(self, data):
        payload = json.dumps(data)
        endpoint = self.__auralizationApiRoot + "/AuralizeFromContent"
        
        print(endpoint)
        print(payload)
        
        return self.__send_request(endpoint, payload)

    # auralize from content
    # workaround: to utilize AuralizeFromSources
    # until AuralizeFromContent is fixed.
    def auralize_from_content2(self, content):
        # upload associated files first
        associated_files = self.extract_files(content)
        self.upload_files(associated_files)

        # read all data
        data = "[{}]"

        # parse 
        data_obj = json.loads(data)
        data_obj[0]['content'] = content
            
        resp = self.auralize_from_sources(data_obj)
        resp = "https://" + self.__auralizationApiHost + ":" + self.__auralizationApiPort + resp[2:]
        return resp;

    # auralize from environmet
    def auralize_from_environment(self, environment: Environment, wav_len: float):
        # read all data
        content = environment.toString()

        # send
        return self.auralize_from_content3(content, wav_len)


    # Foo
    def foo(self, data):
        payload = json.dumps(data)
        endpoint = self.__auralizationApiRoot + "/AuralizeFromSources"
        return self.__send_request(endpoint, payload)


    def upload_files(self, files):
        print(files)
        for f in files:
            self.upload_file(f)


    def upload_file(self, path):
        url = "https://" + self.__auralizationApiHost + ":" + self.__auralizationApiPort + "/" + \
              self.__auralizationApiRoot + "/uploadfile"

        # Suppress ssl verification
        if getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

        print("File: " + path)
        # filename = os.path.basename(path)
        # if path == filename:
        #     print("Please specify the full file path")
        #     sys.exit()

        file = open(path, 'rb')
        response = requests.post(url, files={'file': file}, verify=False)
        return response

    def extract_files(self, content: str):
        files = []

        tokens = content.split()
        for w in tokens:
            ext = w.lower()[-4:]
            if  ext in [".wav", ".csv"]:
                files.append(w)

        return files


# python can't convert objects to json
# but it can convert dictionaries to json 
def jsonDefault(OrderedDict):
    # simple and fast json-friendly collection
    return OrderedDict.__dict__


def driver():
    flow = 2
    if flow == 1:
        files = ["..\\tests\\test.csv", "..\\tests\\tset2.csv"]
        print("files: " + str(files))
        client = nafClient()
        # response = client.upload_files([file])
        response = client.auralize_from_content_and_files({"content": "test string", "wavLength": "2"}, files)
        print(response)

    if flow == 2:
        path_to_data = Path("../tests/environ_wav.txt")

        # read all data
        with Path(path_to_data).open() as f:
            content = f.read()

        files = client.extract_files(content)
        print(files)

        client = nafClient()

        response = client.auralize_from_content_and_files({"content": content, "wavLength": "50"}, files)
        print(response)

    if flow == 3:
        files = ["..\\tests\\test.csv", "..\\tests\\tset2.csv"]
        print("files: " + str(files))
        client = nafClient()
        # response = client.upload_files([file])
        response = client.auralize_from_content_and_files({"content": "test string", "wavLength": "2"}, files)
        print(response)


if __name__ == "__main__":
    driver()
