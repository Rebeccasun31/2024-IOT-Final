# coding=cp950
import requests

def notify(msg):
    token_key = 'rPYWoLi88v2cEKWBWvhkA5f4phIVP4cDzbOw3nDlh4E'
    header = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":'Bearer '+token_key}
    URL = 'https://notify-api.line.me/api/notify'
    payload = {'message':msg}
    res=requests.post(URL,headers=header,data=payload)

if __name__ == '__main__':
    msg = 'Test'
    notify(msg)
