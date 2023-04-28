import requests
from tools.notify import send

#获取号码 江苏南通 尾数拖带
class China_lianghao:


    def GetPhone(self,citycode):
        msg = ''
        url = f'http://www.num10010.com/moonapi/admin/phoneNumber/find?page.pn=1&page.size=48&search.operator_eq=1&search.city_eq={citycode}&search.rule1_eq=601&sort.price=asc'
        header = {
            'Referer': 'http://www.num10010.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        resp = requests.get(url, headers=header).json()
        date = resp['data']['rows']
        # print(date[0])
        for i in range(len(date)):
            if date[i]['poffset'] <=19 and not str(date[i]['number']).__contains__('444') :
                # print(f"当前账号为：{date[i]['number']},保底月费为：{date[i]['poffset']},低消信息为：{date[i]['pcontent']},账号价格为：{date[i]['price']}")
                msg +=f"当前账号为：{date[i]['number']},保底月费为：{date[i]['poffset']},低消信息为：{date[i]['pcontent']},账号价格为：{date[i]['price']}\n"
        print(msg)
        send("靓号信息通知",msg)








if __name__ == '__main__':
    #citycode = get_environ("CITYCODE")
    citycode = '320600'
    chinalianghao = China_lianghao()
    chinalianghao.GetPhone(citycode)