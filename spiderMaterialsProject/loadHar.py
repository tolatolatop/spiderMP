import json
import os

"""
user-agent
cookies
origin
upgrade-insecure-requests
content-type
"""

def loadHar(postData,headers,filename = "www.materialsproject.org.har"):
    with open(filename,'r',encoding='utf-8') as rjson:
        orgdata = json.loads(rjson.read())
        log = orgdata['log']
        entries = log['entries']
        entry = entries[0]
        requestdata = entry["request"]
        orgheaders = requestdata["headers"]
        orgpostdata = requestdata["postData"]["params"]
        
        for org in orgheaders:
            for key in headers.keys():
                if key in org["name"]:
                    headers[key] = org["value"]
                    break
        for org in orgpostdata:
            for key in postData.keys():
                if key in org["name"]:
                    postData[key] = org["value"]
                    break
    return [postData,headers]

