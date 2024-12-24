import requests
import re
import time
import json
import random
import datetime
import base64
import threading
import ssl
import execjs
import os
import sys

from bs4 import BeautifulSoup

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.strxor import strxor
from Crypto.Cipher import AES
from http import cookiejar  # Python 2: import cookielib as cookiejar
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
from tools.notify import send


class BlockAll(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


def printn(m):
    print(f'\n{m}')


ORIGIN_CIPHERS = ('DEFAULT@SECLEVEL=1')

ip_list = []


class DESAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        """
        A TransportAdapter that re-enables 3DES support in Requests.
        """
        CIPHERS = ORIGIN_CIPHERS.split(':')
        random.shuffle(CIPHERS)
        CIPHERS = ':'.join(CIPHERS)
        self.CIPHERS = CIPHERS + ':!aNULL:!eNULL:!MD5'
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=self.CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


requests.packages.urllib3.disable_warnings()
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.set_ciphers('DEFAULT@SECLEVEL=0')
ss = requests.session()
ss.ssl = ssl_context
ss.headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; 22081212C Build/TKQ1.220829.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.97 Mobile Safari/537.36",
    "Referer": "https://wapact.189.cn:9001/JinDouMall/JinDouMall_independentDetails.html"}
ss.mount('https://', DESAdapter())
yc = 0.1
wt = 0
kswt = -3
yf = datetime.datetime.now().strftime("%Y%m")

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

yf = datetime.datetime.now().strftime("%Y%m")
dd = datetime.datetime.now().strftime("%d")


# dd = '01'


def getId(phone, ck):
    # global data
    if yf not in data:
        data[yf] = {}

        str1 = get_level(phone, ck)
        str2 = str1.split('#')
        # print(str2)
        for i in range(0, 3):
            data[yf][f'{i + 4}'] = str2[i]


def get_level(phone, ck):
    url = "https://wapside.189.cn:9001/jt-sign/paradise/getLevelRightsList"
    body = {"para": encrypt_para(f'{{"phone":{phone}}}')}
    right_list = requests.post("https://wapside.189.cn:9001/jt-sign/paradise/getLevelRightsList", json=body,
                               cookies=ck).text
    right_list_json = json.loads(right_list)
    rightsId = ''
    levelStr = ['V4', 'V5', 'V6']

    for str in levelStr:
        # right_list = self.req(url, "POST", body)[f"{str}"]
        # right_list = requests.post("https://wapside.189.cn:9001/jt-sign/paradise/getLevelRightsList",json=body,cookies=ck).json()
        # printn(right_list[f'{str}'])
        right_list1 = right_list_json[f'{str}']
        for data in right_list1:
            # print(dumps(data, indent=2, ensure_ascii=0))
            if "话费" in data["righstName"]:
                rightsId += f'{data["id"]}#'

    print(rightsId)
    return rightsId


wxp = {}
errcode = {
    "0": "兑换成功",
    "412": "兑换次数已达上限",
    "413": "商品已兑完",
    "420": "未知错误",
    "410": "该活动已失效~",
    "Y0001": "当前等级不足，去升级兑当前话费",
    "Y0002": "使用翼相连网络600分钟或连接并拓展网络500分钟可兑换此奖品",
    "Y0003": "使用翼相连共享流量400M或共享WIFI：2GB可兑换此奖品",
    "Y0004": "使用翼相连共享流量2GB可兑换此奖品",
    "Y0005": "当前等级不足，去升级兑当前话费",
    "E0001": "您的网龄不足10年，暂不能兑换"
}

# 加密参数
key = b'1234567`90koiuyhgtfrdews'
iv = 8 * b'\0'

public_key_b64 = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBkLT15ThVgz6/NOl6s8GNPofdWzWbCkWnkaAm7O2LjkM1H7dMvzkiqdxU02jamGRHLX/ZNMCXHnPcW/sDhiFCBN18qFvy8g6VYb9QtroI09e176s+ZCtiv7hbin2cCTj99iUpnEloZm19lwHyo69u5UMiPMpq0/XKBO8lYhN/gwIDAQAB
-----END PUBLIC KEY-----'''

public_key_data = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+ugG5A8cZ3FqUKDwM57GM4io6JGcStivT8UdGt67PEOihLZTw3P7371+N47PrmsCpnTRzbTgcupKtUv8ImZalYk65dU8rjC/ridwhw9ffW2LBwvkEnDkkKKRi2liWIItDftJVBiWOh17o6gfbPoNrWORcAdcbpk2L+udld5kZNwIDAQAB
-----END PUBLIC KEY-----'''


def t(h):
    date = datetime.datetime.now()
    date_zero = datetime.datetime.now().replace(year=date.year, month=date.month, day=date.day, hour=h, minute=59,
                                                second=55)
    date_zero_time = int(time.mktime(date_zero.timetuple()))
    return date_zero_time


def encrypt(text):
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(text.encode(), DES3.block_size))
    return ciphertext.hex()


def decrypt(text):
    ciphertext = bytes.fromhex(text)
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
    return plaintext.decode()


def b64(plaintext):
    public_key = RSA.import_key(public_key_b64)
    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()


def encrypt_para(plaintext):
    public_key = RSA.import_key(public_key_data)
    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(plaintext.encode())
    return ciphertext.hex()


def encode_phone(text):
    encoded_chars = []
    for char in text:
        encoded_chars.append(chr(ord(char) + 2))
    return ''.join(encoded_chars)


def ophone(t):
    key = b'34d7cb0bcdf07523'
    utf8_key = key.decode('utf-8')
    utf8_t = t.encode('utf-8')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(utf8_t, AES.block_size))
    return ciphertext.hex()


# def send(uid,content):
#     r = requests.post('https://wxpusher.zjiecode.com/api/send/message',json={"appToken":"AT_3hr0wdZn5QzPNBbpTHFXawoDIsSUmPkN","content":content,"contentType":1,"uids":[uid]}).json()
#     return r


def userLoginNormal(phone, password):
    alphabet = 'abcdef0123456789'
    uuid = [''.join(random.sample(alphabet, 8)), ''.join(random.sample(alphabet, 4)),
            '4' + ''.join(random.sample(alphabet, 3)), ''.join(random.sample(alphabet, 4)),
            ''.join(random.sample(alphabet, 12))]
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    loginAuthCipherAsymmertric = 'iPhone 14 15.4.' + uuid[0] + uuid[1] + phone + timestamp + password[:6] + '0$$$0.'

    r = ss.post('https://appgologin.189.cn:9031/login/client/userLoginNormal', json={
        "headerInfos": {"code": "userLoginNormal", "timestamp": timestamp, "broadAccount": "", "broadToken": "",
                        "clientType": "#9.6.1#channel50#iPhone 14 Pro Max#", "shopId": "20002", "source": "110003",
                        "sourcePassword": "Sid98s", "token": "", "userLoginName": phone}, "content": {"attach": "test",
                                                                                                      "fieldData": {
                                                                                                          "loginType": "4",
                                                                                                          "accountType": "",
                                                                                                          "loginAuthCipherAsymmertric": b64(
                                                                                                              loginAuthCipherAsymmertric),
                                                                                                          "deviceUid":
                                                                                                              uuid[0] +
                                                                                                              uuid[1] +
                                                                                                              uuid[2],
                                                                                                          "phoneNum": encode_phone(
                                                                                                              phone),
                                                                                                          "isChinatelecom": "0",
                                                                                                          "systemVersion": "15.4.0",
                                                                                                          "authentication": password}}}).json()

    l = r['responseData']['data']['loginSuccessResult']

    if l:
        load_token[phone] = l
        with open(load_token_file, 'w') as f:
            json.dump(load_token, f)
        ticket = get_ticket(phone, l['userId'], l['token'])
        return ticket

    return False


def get_ticket(phone, userId, token):
    r = ss.post('https://appgologin.189.cn:9031/map/clientXML',
                data='<Request><HeaderInfos><Code>getSingle</Code><Timestamp>' + datetime.datetime.now().strftime(
                    "%Y%m%d%H%M%S") + '</Timestamp><BroadAccount></BroadAccount><BroadToken></BroadToken><ClientType>#9.6.1#channel50#iPhone 14 Pro Max#</ClientType><ShopId>20002</ShopId><Source>110003</Source><SourcePassword>Sid98s</SourcePassword><Token>' + token + '</Token><UserLoginName>' + phone + '</UserLoginName></HeaderInfos><Content><Attach>test</Attach><FieldData><TargetId>' + encrypt(
                    userId) + '</TargetId><Url>4a6862274835b451</Url></FieldData></Content></Request>',
                headers={'user-agent': 'CtClient;10.4.1;Android;13;22081212C;NTQzNzgx!#!MTgwNTg1'})

    # printn(phone, '获取ticket', re.findall('<Reason>(.*?)</Reason>',r.text)[0])

    tk = re.findall('<Ticket>(.*?)</Ticket>', r.text)
    if len(tk) == 0:
        return False

    return decrypt(tk[0])


def queryInfo(phone, s):
    global rs
    a = 1
    while a < 10:
        if rs:
            bd = js.call('main').split('=')
            ck[bd[0]] = bd[1]

        r = s.get('https://wapact.189.cn:9001/gateway/golden/api/queryInfo', cookies=ck).json()
        try:
            printn(f'{phone} 金豆余额 {r["biz"]["amountTotal"]}')
            amountTotal = r["biz"]["amountTotal"]
        except:
            amountTotal = 0
        if amountTotal < 3000:
            if rs == 1:
                bd = js.call('main').split('=')
                ck[bd[0]] = bd[1]

            res = s.post('http://wapact.189.cn:9000/gateway/stand/detail/exchange', json={"activityId": jdaid},
                         cookies=ck).text

            if '$_ts=window' in res:
                first_request()
                rs = 1

            time.sleep(3)
        else:
            return r
        a += 1

    return r


def getSign(ticket, session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]

        response_data = \
        session.get('https://wapside.189.cn:9001/jt-sign/ssoHomLogin?ticket=' + ticket, cookies=ck).json()[
            'sign']

        # print(response_data)
        return response_data
    except Exception as e:
        print(e)


def level_ex(phone, rightsId, session, ck):
    # self.get_level()
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')
        url = "https://wapside.189.cn:9001/jt-sign/paradise/conversionRights"
        data = {"para": encrypt_para(f'{{"phone":{phone},"rightsId":"{rightsId}"}},"receiveCount":1')}

        response = session.post('https://wapside.189.cn:9001/jt-sign/paradise/conversionRights', json=data, cookies=ck)
        print(f'{now}--Phone:{phone}--{response.text}')
    except Exception as e:
        print(e)


'''
{"userInfo":{"firstSign":false,"paradiseDressup":{"createdDate":"2021-10-21 14:55:52","newp":1,"smallPicUrl":"https://wapside.189.cn:9001/statics/paradise/l6moxiao.png","level":6,"previewPicUrl":"https://wapside.189.cn:9001/statics/paradise/l6moda.png","expireDate":"2221-10-21 14:56:06","id":"875819fe9cc74205be14aa490b66df34","delFlag":1,"dynamicUrl":"l-6-on.png","defaultUrl":"l-6.png","dressName":"默认服装","coin":0},"name":"云宝Le小信","levelInfoMap":{"level":"6","levelUp":false,"fullGrowthCoinValue":99999,"growthValue":17140},"delFlag":0,"paradiseSkin":{"bigpicUrl":"https://wapside.189.cn:9001/statics/paradise/lv-6-moren-taikongcang.jpg","level":6,"sceneName":"太空舱","smallpicUrl":"https://wapside.189.cn:9001/statics/paradise/lv-6-moren.png","expireDate":"2099-12-31 23:59:59","id":"84ce6dce88d8487b920b44d2af54f96f","type":0,"delFlag":1,"coin":0}},"resoultCode":"0","redPoint":true,"rights":{"picUrl":"https://wapside.189.cn:9001/statics/paradise/v6meiyesongjindou.png","rightsSize":2,"righstName":"Lv6专享1000金豆"},"percentage":"再喂食00.00%次,即可升级","config":[{"configName":"服装场景","configPicture":"https://wapside.189.cn:9001/statics/paradise/tab1.png","showDay":99,"expireDate":{"date":31,"hours":23,"seconds":59,"month":11,"timezoneOffset":-480,"year":199,"minutes":59,"time":4102415999000,"day":4},"id":"52fed78b17b649eebf274914d29a5298","delFlag":1,"sortFlag":1,"jumpUrl":"https://wapside.189.cn:9001/resources/dist/sceneLayout.html?ticket=$ticket$"},{"configName":"等级权益","configPicture":"https://wapside.189.cn:9001/statics/paradise/tab2.png","showDay":99,"expireDate":{"date":31,"hours":23,"seconds":59,"month":11,"timezoneOffset":-480,"year":199,"minutes":59,"time":4102415999000,"day":4},"id":"5aa9363cd1144cdbb2db24ee9033aeaf","delFlag":1,"sortFlag":2,"jumpUrl":"https://wapside.189.cn:9001/resources/dist/classEquity.html?ticket=$ticket$"},{"configName":"金豆商城","configPicture":"https://wapside.189.cn:9001/statics/paradise/tab5.png","showDay":99,"expireDate":{"date":31,"hours":0,"seconds":0,"month":11,"timezoneOffset":-480,"year":199,"minutes":0,"time":4102329600000,"day":4},"id":"3dee17e2a8a24800a3d10ce5df4b204f","delFlag":1,"sortFlag":3,"jumpUrl":"https://wapact.189.cn:9001/JinDouMall/JinDouMall_luckDraw.html?ticket=$ticket$&cmpid=czlyicon"},{"configName":"兑换记录","configPicture":"https://wapside.189.cn:9001/statics/paradise/tab7.png","showDay":99,"expireDate":{"date":31,"hours":23,"seconds":59,"month":11,"timezoneOffset":-480,"year":199,"minutes":59,"time":4102415999000,"day":4},"id":"ec414905fc124376a1d8bf5c33322fff","delFlag":1,"sortFlag":4,"jumpUrl":"https://wapside.189.cn:9001/resources/dist/recordsNew.html?ticket=$ticket$&type=3"}],"openBlindbox":false}
'''


def getParadiseInfo(phone, session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]

        url = "https://wapside.189.cn:9001/jt-sign/paradise/getParadiseInfo"
        data = {"para": encrypt_para(f'{{"phone":{phone}}}')}

        response = session.post(url, json=data, cookies=ck)
        # printn(f'{phone[-4:]}=='+response.text)
        resp = json.loads(response.text)
        level = resp["userInfo"]["levelInfoMap"]["level"]
        jy = resp["userInfo"]["levelInfoMap"]["growthValue"]
        printn(f'等级：{level},经验：{jy}')
        return level, jy
    except Exception as e:
        print(e)


def food(phone, session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        ll, jy = getParadiseInfo(phone, session)
        if jy < 15000:
            bd = js.call('main').split('=')
            ck[bd[0]] = bd[1]
            url = "https://wapside.189.cn:9001/jt-sign/paradise/food"
            data = {"para": encrypt_para(f'{{"phone":{phone}}}')}

            response = session.post('https://wapside.189.cn:9001/jt-sign/paradise/food', json=data, cookies=ck)
            printn(f'=={phone[-4:]}==' + response.text)
            # {"resoultCode": "0", "levelUp": false, "resoultMsg": "喂食成功"}
        else:
            printn('无需喂养，等待降级')
    except Exception as e:
        print(e)


from tools.aes_encrypt import AES_Ctypt


# 签到
def chech_in(phone, session, ck):
    url = "https://wapside.189.cn:9001/jt-sign/api/home/sign"
    time1 = int(round(time.time() * 1000))
    data = {
        "encode": AES_Ctypt("34d7cb0bcdf07523").encrypt(
            f'{{"phone":{phone},"date":{time1},"signSource":"smlprgrm"}}')
    }
    response = session.post(url, json=data, cookies=ck)
    printn(f'=={phone[-4:]}==' + response.text)
    # printn(type(response.text))
    '''
    {"resoultCode":"0","data":{"next":{"signSource":"","signTime":"","iSeven":"","id":"","state":"","specialFlag":"","userId":"","flow":0,"coin":100},"msg":"签到成功","signSource":"smlprgrm","code":1,"continuousDay":1,"currentDate":1733131397963,"type":"firstSign","userId":"2022072000057809098","flow":0,"coin":120,"totalDay":1},"resoultMsg":"成功"}
    '''


# {'resoultCode': 0, 'data': {'continuousDay': 1, 'signDay': 1, 'reStatus': 0, 'isSign': 1, 'isSeven': False}, 'resoultMsg': '请求成功'}
def userStatusInfo(phone, session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/api/home/userStatusInfo"
        data = {"para": encrypt_para(f'{{"phone":{phone}}}')}
        response = session.post(url, json=data, cookies=ck)
        printn(f'=={phone[-4:]}==' + response.text)
        resp = json.loads(response.text)
        if resp["resoultCode"] == 0:
            printn(
                f'=={phone[:3]}***{phone[-4:]}连续签到{resp["data"]["continuousDay"]}天=当前签到{resp["data"]["signDay"]}天=\n')
            return f'=={phone[:3]}***{phone[-4:]}连续签到{resp["data"]["continuousDay"]}天=当前签到{resp["data"]["signDay"]}天='
        else:
            return '签到失败\n'

    except Exception as e:
        print(e)


def continueSignDays(phone, session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/webSign/continueSignDays"
        data = {"para": encrypt_para(f'{{"phone":{phone}}}')}
        response = session.post(url, json=data, cookies=ck)
        printn(f'=={phone[-4:]}==' + response.text)
        resp = json.loads(response.text)
        # {'continueSignDays': 1, 'resoultCode': '0', 'level': 6}
        if resp['resoultCode'] == '0':
            printn(f'抽奖连签天数：{resp["continueSignDays"]}')
            if resp["continueSignDays"] == 7:
                exchangePrize(phone, 7, session)
            elif resp["continueSignDays"] == 15:
                exchangePrize(phone, 15, session)
            elif resp["continueSignDays"] == 28:
                exchangePrize(phone, 28, session)
            else:
                printn('查询抽奖天数失败')

    except Exception as e:
        print(e)


# 抽奖
def exchangePrize(phone, cd, session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/webSign/exchangePrize"
        data = {"para": encrypt_para(f'{{"phone":"{phone}","type":"{cd}"}}')}
        response = session.post(url, json=data, cookies=ck)
        printn(response.text)

    except Exception as e:
        print(e)

msg = ''

'''
{"resoultCode":"0","data":{"flag":"fc380bdaa8104804a86e29257eb0c96a","resoultCode":1,"resoultMsg":"用户已领取"},"resoultMsg":"fc380bdaa8104804a86e29257eb0c96a"}
{'resoultCode': '0', 'data': {'area': True, 'biz': '保存成功', 'code': 0, 'err': ''}, 'resoultMsg': 'efa82058f6e24edf96f3975a2b2e44f9'}
'''
def month_jml_preCost(phone,session):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/short/message/preCost"
        str1 = AES_Ctypt("34d7cb0bcdf07523").encrypt(f'{phone}')
        data ={"phone":f"{str1}","activityCode":"shortMesssge"}
        str = session.post(url,json=data,cookies=ck)
        resp = json.loads(str.text)
        printn(resp)
        if resp["resoultCode"] == '0':
            flag = resp["resoultMsg"]
            month_jml_userCost(phone,session,flag)
            month_jml_receive(phone,session,flag)
            month_jml_getCount(phone,session,flag)
            month_jml_refresh(phone,session,flag)
        else:
            printn('每月见面礼登录失败')


    except Exception as e:
        print(e)

'''
{"resoultCode":"0","data":[{"image":"https://www.189.cn/wapactivity/wapsign/shortMessage/image/f200jin.png","createdDate":"2024-11-22 11:02:21.343","expire":"2024-11-25 11:02:21.343","pizeName":"200金豆","state":-1},{"image":"https://www.189.cn/wapactivity/wapsign/shortMessage/image/fuihuishou.png","createdDate":"2024-11-22 11:02:21.347","expire":"2024-11-25 11:02:21.347","pizeName":"20元回收加价券","state":-1},{"image":"https://www.189.cn/wapactivity/wapsign/shortMessage/image/f66meituan.png","createdDate":"2024-11-22 11:02:21.351","expire":"2024-11-25 11:02:21.351","pizeName":"66元美团券包","state":-1}],"resoultMsg":"请求成功"}
'''
def month_jml_userCost(phone,session,flag):
    try:
        global msg
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/short/message/userCost"
        str1 = AES_Ctypt("34d7cb0bcdf07523").encrypt(f'{phone}')
        data = {"phone": f"{str1}", "activityCode": "shortMesssge","flag":f"{flag}"}
        str1 = session.post(url, json=data, cookies=ck)
        resp = json.loads(str1.text)
        if resp["resoultCode"] == '0':
            for item in resp['data']:
                msg +=f'{phone[:3]}****{phone[-4:]}获取的奖品为：{item["pizeName"]}\n'
                printn(f'获取的奖品为：{item["pizeName"]}')
        else:
            printn('获取每月见面礼失败')
    except Exception as e:
        print(e)

# {"msg":"领取成功","code":0}
def month_jml_receive(phone,session,flag):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/lottery/receive"
        data1 = {"phone": f"{phone}","flag":f"{flag}"}
        data  = {"para": encrypt_para(str(data1))}
        str1 = session.post(url, json=data, cookies=ck).text
        resp = json.loads(str1)
        if resp['code'] == 0:
            printn('领取app抽奖次数成功')
        else:
            printn('领取App抽奖次数失败')
    except Exception as e:
        print(e)

'''
{"app":[{"month":20241220,"createTime":{"date":3,"hours":18,"seconds":48,"month":11,"timezoneOffset":-480,"year":124,"minutes":25,"time":1733221548000,"day":2},"phone":"18552988878","videoType":0,"id":22731949,"source":0}],"code":0,"video":[{"month":20241220,"createTime":{"date":22,"hours":11,"seconds":22,"month":10,"timezoneOffset":-480,"year":124,"minutes":2,"time":1732244542000,"day":5},"phone":"18552988878","videoType":202201,"id":22242095,"source":1},{"month":20241220,"createTime":{"date":22,"hours":11,"seconds":27,"month":10,"timezoneOffset":-480,"year":124,"minutes":2,"time":1732244547000,"day":5},"phone":"18552988878","videoType":202202,"id":22242102,"source":1},{"month":20241220,"createTime":{"date":22,"hours":11,"seconds":33,"month":10,"timezoneOffset":-480,"year":124,"minutes":2,"time":1732244553000,"day":5},"phone":"18552988878","videoType":202203,"id":22242112,"source":1}]}
{'app': [{'month': 20241220, 'createTime': {'date': 3, 'hours': 19, 'seconds': 11, 'month': 11, 'timezoneOffset': -480, 'year': 124, 'minutes': 14, 'time': 1733224451000, 'day': 2}, 'phone': '18118672666', 'videoType': 0, 'id': 22734472, 'source': 0}], 'code': 0, 'video': []}
'''
def month_jml_getCount(phone,session,flag):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/lottery/getCount"
        data1 = {"phone": f"{phone}", "flag": f"{flag}"}
        data = {"para": encrypt_para(str(data1))}
        str1 = session.post(url, json=data, cookies=ck).text
        resp = json.loads(str1)
        printn(resp)
        if resp["code"] == 0:
            islook = False
            # for item in resp["video"]:
            for item in ['202201','202202','202203']:
                # print(item['videoType'])
                if islook:
                    waittime = random.randint(5, 8)
                    time.sleep(waittime)
                month_jml_addVideoCount(phone,session,flag,item)
                islook = True
        else:
            printn('查询看视频得抽奖机会次数失败')
    except Exception as e:
        print(e)


# {'msg': '此视频已获取过抽奖次数！', 'code': 1}
def month_jml_addVideoCount(phone,session,flag,videoType):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/lottery/addVideoCount"
        data1 = {"phone": f"{phone}","videoType":f"{videoType}","flag": f"{flag}"}
        data = {"para": encrypt_para(str(data1))}
        str1 = session.post(url, json=data, cookies=ck).text
        resp = json.loads(str1)
        if resp['code'] == 0:
            printn(f'观看{videoType}视频获取抽奖机会成功')
        else:
            printn(f'观看{videoType}视频获取抽奖机会失败')
    except Exception as e:
        print(e)

# {'rNumber': '2'}
def month_jml_refresh(phone,session,flag):
    try:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/lottery/refresh"
        data1 = {"phone": f"{phone}", "flag": f"{flag}"}
        data = {"para": encrypt_para(str(data1))}
        str1 = session.post(url, json=data, cookies=ck).text
        resp = json.loads(str1)
        # printn(resp)
        # if resp['code'] == '-1':
        lottime = int(resp["rNumber"])
        islot = False
        printn(f'可以抽奖{lottime}次')
        while lottime > 0:
            if islot:
                waittime = random.randint(5, 8)
                time.sleep(waittime)
            month_jml_lotteryRevice(phone,session,flag)
            lottime-=1
            islot = True

    except Exception as e:
        print(e)

# {'msg': '抽奖成功', 'img': 'https://www.189.cn/wapactivity/wapsign/shortMessage/image/t300.png', 'code': '0', 'rname': '300金豆', 'id': '8a7a66c430644112b5e7bc130412ddbc'}
def month_jml_lotteryRevice(phone,session,flag):
    try:
        global msg
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]
        url = "https://wapside.189.cn:9001/jt-sign/lottery/lotteryRevice"
        data1 = {"phone": f"{phone}", "flag": f"{flag}"}
        data = {"para": encrypt_para(str(data1))}
        str1 = session.post(url, json=data, cookies=ck).text
        resp = json.loads(str1)
        if resp['code'] == '0':
            msg +=f'抽奖奖品为：{resp["rname"]}\n'
            printn(f'抽奖奖品为：{resp["rname"]}')
        else:
            printn('每月见面礼抽奖失败')
    except Exception as e:
        print(e)



from tools.notify import send




def ks(phone, ticket, uid):
    global wt, msg

    wxp[phone] = uid
    s = requests.session()
    s.headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; 22081212C Build/TKQ1.220829.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.97 Mobile Safari/537.36",
        "Referer": "https://wapact.189.cn:9001/JinDouMall/JinDouMall_independentDetails.html"}
    s.cookies.set_policy(BlockAll())
    s.mount('https://', DESAdapter())
    s.timeout = 30
    if rs:
        bd = js.call('main').split('=')
        ck[bd[0]] = bd[1]

    login = s.post('https://wapact.189.cn:9001/unified/user/login',
                   json={"ticket": ticket, "backUrl": "https%3A%2F%2Fwapact.189.cn%3A9001",
                         "platformCode": "P201010301", "loginType": 2}, cookies=ck).json()
    if login['code'] == 0:
        printn(phone + " 获取token成功")
        s.headers["Authorization"] = "Bearer " + login["biz"]["token"]

        queryInfo(phone, s)

        if rs:
            sign = getSign(ticket, s)
            new_header = {
                "Host": "wapside.189.cn:9001",
                "User-Agent": f"CtClient;9.6.1;Android;12;SM-G9860;{base64.b64encode(phone[5:11].encode()).decode().strip('=+')}!#!{base64.b64encode(phone[0:5].encode()).decode().strip('=+')}",
                "Referer": "https://wapside.189.cn:9001/resources/dist/signInActivity.html",
                "sign": sign}
            s.headers.update(new_header)
            month_jml_preCost(phone,s)
            # month_jml_lotteryRevice(phone,s,'cdbe6ea4a4a74060921c551cf61a16e6')
    else:

        printn(f"{phone} 获取token {login['message']}")


def first_request(res=''):
    global js, fw
    url = 'https://wapact.189.cn:9001/gateway/standExchange/detailNew/exchange'
    if res == '':
        response = ss.get(url)
        res = response.text
    soup = BeautifulSoup(res, 'html.parser')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'src' in str(script):
            rsurl = re.findall('src="([^"]+)"', str(script))[0]

        if '$_ts=window' in script.get_text():
            ts_code = script.get_text()

    urls = url.split('/')
    rsurl = urls[0] + '//' + urls[2] + rsurl
    # print(rsurl)
    ts_code += ss.get(rsurl).text
    content_code = soup.find_all('meta')[1].get('content')
    with open("瑞数通杀.js", encoding='utf-8') as f:
        js_code_ym = f.read()
    js_code = js_code_ym.replace('content_code', content_code).replace("'ts_code'", ts_code)
    js = execjs.compile(js_code)

    for cookie in ss.cookies:
        ck[cookie.name] = cookie.value
    return content_code, ts_code, ck


def main():
    global wt, rs, msg
    r = ss.get('https://wapact.189.cn:9001/gateway/standExchange/detailNew/exchange')
    if '$_ts=window' in r.text:
        rs = 1
        print("瑞数加密已开启")
        first_request()
    else:
        print("瑞数加密已关闭")
        rs = 0
    if os.environ.get('chinaTelecomAccountEv') != None:
        chinaTelecomAccount = os.environ.get('chinaTelecomAccountEv')
    else:
        printn('填写环境变量chinaTelecomAccountEv')


    for i in chinaTelecomAccount.split('&'):

        i = i.split('#')
        phone = i[0]
        password = i[1]
        uid = i[1]
        ticket = False

        # ticket = get_userTicket(phone)

        if phone in load_token:
            printn(f'{phone} 使用缓存登录')
            ticket = get_ticket(phone, load_token[phone]['userId'], load_token[phone]['token'])

        if ticket == False:
            printn(f'{phone} 使用密码登录')
            ticket = userLoginNormal(phone, password)

        if ticket:
            ks(phone, ticket, uid)
        else:
            printn(f'{phone} 登录失败')
    send('电信签到通知', msg)


jdhf = ""
cfcs = 20
jdaid = '60dd79533dc03d3c76bdde30'
ck = {}
load_token_file = 'chinaTelecom_cache.json'
try:
    with open(load_token_file, 'r') as f:
        load_token = json.load(f)
except:
    load_token = {}

main()
