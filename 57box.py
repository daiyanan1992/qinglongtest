"""
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
57Box_0.2
微信小程序  57Box   玩法：完成基础任务抽免费箱子
登录微信小程序授权手机号然后下载APP设置密码
export BOX_data=手机号@密码
多账号用'===='隔开 例 账号1====账号2
cron： 0 8 * * *
"""

lottery = 1  # 抽鞋盒开关 1开启 0关闭
from tools.notify import send
import os
import time

import requests
# from dotenv import load_dotenv
#
# load_dotenv()
accounts = os.getenv("BOX_data")
# response = requests.get('https://gitee.com/shallow-a/qim9898/raw/master/label.txt').text
# print(response)


msg = ''
if accounts is None:
    print('你没有填入BOX_data，咋运行？')
    exit()
accounts_list = accounts.split('&')
num_of_accounts = len(accounts_list)
print(f"获取到 {num_of_accounts} 个账号")
for i, account in enumerate(accounts_list, start=1):
    values = account.split('@')
    mobile, password = values[0], values[1]
    print(f"\n{'=' * 8}开始执行账号[{mobile}]{'=' * 8}")
    url = "https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=login&m=greatriver_lottery_operation"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Html5Plus/1.0 (Immersed/47) uni-app",
    }

    data = {
        "mobile": mobile,
        "password": password,
        "password2": "",
        "code": "",
        "invite_uid": "0",
        "source": "app"
    }

    response = requests.post(url, headers=headers, data=data).json()
    if response['errno'] == 0:
        print(f"{response['message']}")
        token = response['data']['token']
        print(f"{'=' * 12}开始每日任务{'=' * 12}")
        for i in range(3):
            url = f"https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=uptaskinfo&&token={token}"
            data = {
                "m": "greatriver_lottery_operation",
                "id": "35",
                "answer": ""
            }
            response = requests.post(url, headers=headers, data=data).json()
            state = "看广告领矿石"
            if response['errno'] == 999:
                print(f"{state}---{response['message']}")
                break
            elif response['errno'] == 0:
                print(f"第{i + 1}次{state}---{response['message']}")
                time.sleep(5)
            else:
                print(f"{state}错误未知{response}")
                break
        time.sleep(3)
        data = {
            "m": "greatriver_lottery_operation",
            "id": "26",
            "answer": "669988"
        }
        response = requests.post(url, headers=headers, data=data).json()
        state = "进群密码"
        if response['errno'] == 999:
            print(f"{state}---{response['message']}")
        elif response['errno'] == 0:
            print(f"{state}---{response['message']}")
        else:
            print(f"{state}错误未知{response}")
            break
        time.sleep(3)
        data = {
            "m": "greatriver_lottery_operation",
            "id": "30",
            "answer": "普通物品不可分解"
        }
        response = requests.post(url, headers=headers, data=data).json()
        state = "每日答题"
        if response['errno'] == 999:
            print(f"{state}---{response['message']}")
        elif response['errno'] == 0:
            print(f"{state}---{response['message']}")
        else:
            print(f"{state}错误未知{response}")
            break
        print(f"{'=' * 12}获取账号信息{'=' * 12}")
        url = f"https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=getuserinfo&&token={token}"
        data = {
            "m": "greatriver_lottery_operation",
            "title": "",
        }
        response = requests.post(url, headers=headers, data=data).json()
        if response['errno'] == 999:
            print(f"{response['message']}")
        elif response['errno'] == 0:
            nickname = response['data']['nickname']
            integral_str = response['data']['integral']
            try:
                integral = int(float(integral_str))
                print(f"Name:{nickname}---矿石余额:{integral}")
                msg += f"Name:{nickname}---矿石余额:{integral}\n"
            except ValueError:
                print(f"无效的integral值: {integral_str}")
        else:
            print(f"错误未知{response}")
            break
        if lottery == 1:  # 开始抽奖
            print(f"{'=' * 12}执行开鞋盒{'=' * 12}")
            num = integral // 120
            for i in range(num):
                url = "https://www.57box.cn/app/index.php"
                params = {
                    "i": "2",
                    "t": "0",
                    "v": "1",
                    "from": "wxapp",
                    "c": "entry",
                    "a": "wxapp",
                    "do": "openthebox",
                    "token": token,
                    "m": "greatriver_lottery_operation",
                    "box_id": "303",
                    "paytype": "1",
                    "answer": "",
                    "num": 1
                }
                response = requests.post(url, headers=headers, data=params).json()
                if response['errno'] == 0:
                    complete_prize_title = response['data']['prizes_data'][0]['complete_prize_title']
                    prize_market_price = response['data']['prizes_data'][0]['prize_market_price']
                    print(f"{response['message']}---{complete_prize_title}  市场价:{prize_market_price}")
                elif response['errno'] == 999:
                    print(f"{response['message']}")
                else:
                    print(f"错误未知{response}")
                    break
            print(f"开鞋盒完毕")
            if num >= 1:
                url = f"https://www.57box.cn/app/index.php?i=2&t=0&v=1&from=wxapp&c=entry&a=wxapp&do=uptaskinfo&&token={token}"
                data = {
                    "m": "greatriver_lottery_operation",
                    "id": "39",
                    "answer": ""
                }
                response = requests.post(url, headers=headers, data=data).json()
                state = "开盒看视频领矿石"
                if response['errno'] == 999:
                    print(f"{state}---{response['message']}")
                elif response['errno'] == 0:
                    print(f"{state}---{response['message']}")
                else:
                    print(f"{state}错误未知{response}")
                    break
            else:
                print()

        elif lottery == 0:
            print(f"{'=' * 12}不执行开鞋盒{'=' * 12}")
        url = "https://www.57box.cn/app/index.php"

        params = {
            "i": "2",
            "t": "0",
            "v": "1",
            "from": "wxapp",
            "c": "entry",
            "a": "wxapp",
            "do": "getmemberprizes",
            "token": token,
            "m": "greatriver_lottery_operation",
            "page": "0",
            "type": "1",
            "prize_level": "1",
        }

        response = requests.get(url, headers=headers, params=params).json()

        all_prizes = response['data']

        for prize in all_prizes:
            prize_title = prize['prize']['complete_prize_title']
            prizes_count = prize['prizes_count']
            print(f"{prize_title} 数量:x{prizes_count}")
            msg += f"Name：{nickname}--{prize_title} 数量:x{prizes_count}\n"
    elif response['errno'] == 999:
        print(f"{response['message']}")
        break
    else:
        print(f"错误未知{response}")
        break
print(msg)
send('57box通知',msg)
