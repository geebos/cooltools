#-*- coding: utf-8 -*
__author__ = 'geebos'
import requests
import json


def readConfig():
    with open('config', 'r') as fp:
        return fp.readline()

def uploadImage(cookie, filepath, filename):
    upload_url = 'https://upload.qiniup.com/'
    token_url = 'https://www.jianshu.com/upload_images/token.json?filename={}'.format(filename)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Cookie': cookie,
    }

    response = requests.get(token_url, headers=headers)
    response.encoding = response.apparent_encoding
    token_and_key = json.loads(response.text)

    with open(filepath, 'rb') as file:
        files = {
            'file': (filename, file),
            'token': (None, token_and_key['token']),
            'key': (None, token_and_key['key']),
        }
        response = requests.post(upload_url, headers=headers, files=files)
        response.encoding = response.apparent_encoding
        return json.loads(response.text)

cookie = readConfig()
print(uploadImage(cookie, 'test.jpg', 'test.jpg'))