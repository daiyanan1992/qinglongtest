"""
@Qim出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
加多宝_V0.1   兑饮品
入口 微信小程序_点亮城市 与加多宝喝彩
抓包域名https://wb.onlineweixin.com/取出token
export jdbtoken=token
多账号用'&'隔开 例 账号1&账号2
cron： 0 0 1,13 * * ?
"""
# from dotenv import load_dotenv
# load_dotenv()
import os
import requests
from tools.notify import send

accounts = os.getenv('jdbtoken')
msg = ''
# print(requests.get("http://1.94.61.34:50/index.txt").content.decode("utf-8"))
if accounts is None:
    print('你没有填入jdbtoken，咋运行？')
    exit()
else:
    accounts_list = os.environ.get('jdbtoken').split('&')
    num_of_accounts = len(accounts_list)
    print(f"获取到 {num_of_accounts} 个账号")
    for i, account in enumerate(accounts_list, start=1):
        values = account.split('@')
        token = values[0]
        print(f"\n=======开始执行账号{i}=======")
        url = "https://wb.onlineweixin.com/jdbcms/user/queryById"
        headers = {
            "Host": "wb.onlineweixin.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8447",
            "token": token,
        }

        response = requests.post(url, headers=headers).json()
        if response['code'] == 2000:
            residue = response['data']['residue']
            nickname = response['data']['userInfo']['nickname']
            # phone = response['data']['userInfo']['phone']
            print(f"【{nickname}】-当前点亮值:{residue}")
            msg += f"【{nickname}】-当前点亮值:{residue}"
            print(f"开始完成任务...")
            url = "https://wb.onlineweixin.com/jdbcms/record/drop"  # 城市点亮
            data = {"city": "杭州市", "province": "浙江省"}
            response = requests.post(url, headers=headers, json=data).json()
            if response['code'] == 2000:
                print(f"点亮成功，获得-{response['data']['integralB']}点亮值")
            elif response['code'] == 1002:
                print(f"点亮失败---{response['desc']}")
            else:
                print(f"点亮失败{response}")
            for i in range(5):
                url = "https://wb.onlineweixin.com/jdbcms/record/effect"
                data = {"storey": "169802776358969", "classification": "169802277606966",
                        "token": token, "Score": 201}
                response = requests.post(url, headers=headers, json=data).json()
                if response['code'] == 2000:
                    print(f"游戏麻辣消消乐，获得-{response['data']['integralB']}点亮值")
                elif response['code'] == 1002:
                    print(f"游戏麻辣消消乐---{response['desc']}")
                    break
                else:
                    print(f"游戏失败{response}")
                    break
            for i in range(5):
                url = "https://wb.onlineweixin.com/jdbcms/record/effect"
                data = {"storey": "169802835888997", "classification": "169802793875078",
                        "token": token, "Score": 1720}
                response = requests.post(url, headers=headers, json=data).json()
                if response['code'] == 2000:
                    print(f"游戏极限冲击，获得-{response['data']['integralB']}点亮值")
                elif response['code'] == 1002:
                    print(f"游戏极限冲击---{response['desc']}")
                    break
                else:
                    print(f"游戏失败{response}")
                    break
            for i in range(5):
                url = "https://wb.onlineweixin.com/jdbcms/record/effect"
                data = {"storey": "169802835888707", "classification": "146980285888701",
                        "token": token, "Score": 16070.5}
                response = requests.post(url, headers=headers, json=data).json()
                if response['code'] == 2000:
                    print(f"游戏我要去杭州，获得-{response['data']['integralB']}点亮值")
                elif response['code'] == 1002:
                    print(f"游戏我要去杭州---{response['desc']}")
                    break
                else:
                    print(f"游戏失败{response}")
                    break


        elif response['code'] == 5000:
            print(f"token失效")
        else:
            print(f"{response}")
send('加多宝通知',msg)
