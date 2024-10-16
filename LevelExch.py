#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : github@limoruirui https://github.com/limoruirui
# @Time : 2022/9/12 16:10
# cron "0 9,10,14 * * *" script-path=xxx.py,tag=匹配cron用
# const $ = new Env('电信并发多账号签到');
# -------------------------------

"""
1. 电信签到 不需要抓包 脚本仅供学习交流使用, 请在下载后24h内删除
2. cron说明 默认10点14点执行一次(用于兑换话费)
2. 环境变量说明:
    必须  TELECOM : 电信手机号@电信服务密码@宠物喂食次数(默认0,最大10)&手机号2@密码2@喂食数2
    # TELECOM       13311111111@111111@0&13322222222@222222@10
    并发命令：task WWJqingcheng_dx/china_telecom.py conc TELECOM
             task 后边是脚本所在目录/china_telecom.py conc TELECOM
3. 必须登录过 电信营业厅 app的账号才能正常运行
"""
import json

"""
update:
    2022.10.25 参考大佬 github@QGCliveDavis https://github.com/QGCliveDavis 的 loginAuthCipherAsymmertric 参数解密 新增app登录获取token 完成星播客系列任务 感谢大佬
    2022.11.11 增加分享任务
"""
from datetime import date, datetime

import time

import requests
from requests import get, post
from base64 import b64encode

from tools.rsa_encrypt import RSA_Encrypt
from tools.tool import timestamp, get_environ, print_now
from login.telecom_login import TelecomLogin



data = {}
dirsize = 0
try:
    with open('权益id.log') as fr:
        data1 = fr.read()
        dirsize = len(data1)
        data = eval(data1)
except:
    with open('权益id.log', 'w') as f:
        pass

yf = datetime.now().strftime("%Y%m")
dd = datetime.now().strftime("%d")
# dd = '01'



class ChinaTelecom:
    def __init__(self, account, pwd, checkin=True):
        self.phone = account
        self.ticket = ""
        self.token = ""
        if pwd != "" and checkin:
            userLoginInfo = TelecomLogin(account, pwd).main()
            self.ticket = userLoginInfo[0]
            self.token = userLoginInfo[1]

    def getSign(self, tick):
        url = "https://wapside.189.cn:9001/jt-sign/ssoHomLogin"

        data = {'ticket': f'{tick}'}
        resp = get(url=url, params=data).json()
        sign = resp["sign"]
        # print(sign)
        return sign

    def init(self):
        self.msg = ""
        self.ua = f"CtClient;9.6.1;Android;12;SM-G9860;{b64encode(self.phone[5:11].encode()).decode().strip('=+')}!#!{b64encode(self.phone[0:5].encode()).decode().strip('=+')}"
        self.sign = self.getSign(self.ticket)
        self.headers = {
            "Host": "wapside.189.cn:9001",
            "Referer": "https://wapside.189.cn:9001/resources/dist/signInActivity.html",
            "User-Agent": self.ua,
            "sign": self.sign
        }
        self.key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+ugG5A8cZ3FqUKDwM57GM4io6\nJGcStivT8UdGt67PEOihLZTw3P7371+N47PrmsCpnTRzbTgcupKtUv8ImZalYk65\ndU8rjC/ridwhw9ffW2LBwvkEnDkkKKRi2liWIItDftJVBiWOh17o6gfbPoNrWORc\nAdcbpk2L+udld5kZNwIDAQAB\n-----END PUBLIC KEY-----"

    def req(self, url, method, data=None):
        if method == "GET":
            data = get(url, headers=self.headers).json()
            return data
        elif method.upper() == "POST":
            data = post(url, headers=self.headers, json=data).json()
            return data
        else:
            print_now("您当前使用的请求方式有误,请检查")

    # 长明文分段rsa加密
    def telecom_encrypt(self, text):
        if len(text) <= 32:
            return RSA_Encrypt(self.key).encrypt(text)
        else:
            encrypt_text = ""
            for i in range(int(len(text) / 32) + 1):
                split_text = text[(32 * i):(32 * (i + 1))]
                encrypt_text += RSA_Encrypt(self.key).encrypt(split_text)
            return encrypt_text


    def get_level(self):

        url = "https://wapside.189.cn:9001/jt-sign/paradise/getLevelRightsList"
        body = {
            "para": self.telecom_encrypt(f'{{"phone":{self.phone}}}')
        }


        rightsId = ''
        levelStr = ['V4','V5','V6']
        for str in levelStr:
            right_list = self.req(url, "POST", body)[f"{str}"]
            for data in right_list:
                # print(dumps(data, indent=2, ensure_ascii=0))
                if "话费" in data["righstName"]:
                    rightsId += f'{data["id"]}#'

        print(rightsId)
        return rightsId
            # print(f'等级返回：{data}')

        # print(self.rightsId)



    # 每月领取等级金豆
    def level_ex(self, rightsId):
        # self.get_level()
        now = datetime.now().strftime('%H:%M:%S.%f')
        url = "https://wapside.189.cn:9001/jt-sign/paradise/conversionRights"
        data = {
            "para": self.telecom_encrypt(f'{{"phone":{self.phone},"rightsId":"{rightsId}"}},"receiveCount":1')
        }

        resp = self.req(url, "POST", data)
        print_now(f'{now}--Phone:{self.phone}--{resp}')


    def getId(self):
        # global data
        if yf not in data:
            data[yf] = {}

            str1 = self.get_level()
            str2 = str1.split('#')
            # print(str2)
            for i in range(0, 3):
                data[yf][f'{i + 4}'] = str2[i]







    def main(self,level):
        global data
        global dirsize
        self.init()
        if dd == '01' or dirsize == 0:
            self.getId()
            with open('权益id.log', 'w') as f:
                f.write(json.dumps(data))
            print('再跑一次脚本')
        rightsId = data[yf][level]
        print(rightsId)
        start_time = time.time()
        while 1 == 1:
            current_time = time.time()
            try:
                data = self.level_ex(rightsId)
            except Exception as e:
                print(f"请求发送失败: " + str(e))
                #     # sleep(6)
                continue
            elapsed_time = current_time - start_time
            if elapsed_time >= 200:  # 5分钟是300秒
                break

        print('========================================================')
        print('============================分隔符=======================')
        print('========================================================')


# 主方法与源文件不同；增加了多账号的判断；变量格式如下
# TELECOM       13311111111@111111@10&13322222222@222222@10
if __name__ == "__main__":
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    # TELECOM = get_environ("chinaTelecomAccount")
    TELECOM = '18888888888#398104#5'
    users = TELECOM.split("&")
    for i in range(len(users)):
        user = users[i].split("#")
        phone = user[0]
        password = user[1]
        levelid = user[2]

        print(phone, password)
        if phone == "":
            exit(0)
        if password == "":
            print_now("电信服务密码未提供 只执行部分任务")

        else:
            telecom = ChinaTelecom(phone, password)
            telecom.main(levelid)
