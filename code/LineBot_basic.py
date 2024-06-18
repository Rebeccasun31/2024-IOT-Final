# -*- coding: UTF-8 -*-

#Python module requirement: line-bot-sdk, flask
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError 
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import time, random, threading
import DAN

ServerURL = 'https://2.iottalk.tw' #with SSL connection
Reg_addr = "AABB3388" + str( random.randint(200,299)) #if None, Reg_addr = MAC address

DAN.profile['dm_name']='LineBot'
DAN.profile['df_list']=['Msg-I', 'Msg-O',]
DAN.profile['d_name']= "SCR."+ str( random.randint(300,599 ) ) +"_LineBot" # None

line_bot_api = LineBotApi('token')  #LineBot's Channel access token
handler = WebhookHandler('secret')  #LineBot's Channel secret
user_id_set=set()                                         #LineBot's Friend's user id 
app = Flask(__name__)
DAN.device_registration_with_retry(ServerURL, Reg_addr)

interval = 88
allDead = gone = False

def doODF( ):
    global allDead, gone
    sleepTime = 1.0 * interval / 1000.0
    while True:
        try:
            idList = loadUserId()
            if idList: user_id_set = set(idList)

            ODF_data=DAN.pull('Msg-O')
            if ODF_data != None:    # 不等於 None 表示有抓到資料
                for userId in user_id_set:
                    line_bot_api.push_message(userId, TextSendMessage(text=ODF_data[0]))
                
            time.sleep(0.5)
        except KeyboardInterrupt:
            allDead = True
            break
        except Exception as e:
            print(e)
            if str(e).find('mac_addr not found:') != -1:
                print('Reg_addr is not found. Try to re-register...')
                DAN.device_registration_with_retry(ServerURL, Reg_addr)
            else:
                print('Connection failed due to unknow reasons.')
                time.sleep(1)    
        try:
            start_time = time.monotonic()
            ggyy=0
            while time.monotonic() - start_time < sleepTime:
                ggyy+=1
                pass; 
        except:
            allDead = True
            break

def loadUserId():
    try:
        idFile = open('idfile', 'r')
        idList = idFile.readlines()
        idFile.close()
        idList = idList[0].split(';')
        idList.pop()
        return idList
    except Exception as e:
        print(e)
        return None


def saveUserId(userId):
        idFile = open('idfile', 'a')
        idFile.write(userId+';')
        idFile.close()


@app.route("/", methods=['GET'])
def hello():
    return "HTTPS Test OK."

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']    # get X-Line-Signature header value
    body = request.get_data(as_text=True)              # get request body as text
    # print("Request body: " + body, "Signature: " + signature)
    try:
        handler.handle(body, signature)                # handle webhook body
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    Msg = event.message.text
    print('GotMsg:{}'.format(Msg))
    
    userId = event.source.user_id
    if not userId in user_id_set:
        user_id_set.add(userId)
        saveUserId(userId)

    if ("解除" in Msg):
        DAN.push('Msg-I', [0])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="成功解除警報！"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="若要解除警報請輸入「解除」。"))
    

   
if __name__ == "__main__":
    thready = threading.Thread(target=doODF)
    thready.daemon = True
    thready.start()

    idList = loadUserId()
    if idList: user_id_set = set(idList)

    try:
        for userId in user_id_set:
            line_bot_api.push_message(userId, TextSendMessage(text="這是一個跌倒警報系統！若要解除警報請輸入「解除」。"))
    except Exception as e:
        print(e)
    
    app.run('127.0.0.1', port=32768, threaded=True, use_reloader=False)
    DAN.deregister()
