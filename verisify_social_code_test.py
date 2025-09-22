import requests
import random

ses = requests.session()

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Origin': 'https://www.creditchina.gov.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://www.creditchina.gov.cn/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

params = {
    'website': '10019513',
    'server': 's1',
    'datatype': 'click_change',
    'sendid': '1758505937650',
}

data = 'AWS=10019513&ASER=s1&ARD=click&ARDT=change&ACT=web&ATP=pc&AVER=20240618&ASDKVER=20240618&AUC=20250922012311320938212209162211&AVUC=1758504191312&AUID=&AUN=&ALG=zh-CN&ACL=24&ASS=1920*1080&AFST=1758504191312&ALST=1758504191312&ARC=0&ACS=UTF-8&ASY=linux%20x86&ASYT=pc&ABOT=visitor&ABR=chrome&AWXBR=0&ATZ=0&AMD=&ALOGT=&APS=www.creditchina.gov.cn&APU=%2Fxinxigongshi%2Fshehuixinyongdaimachaxun%2F&ASSCW=1061&AXPOS=0&AYPOS=0&ASSH=1080&ASSCH=895&ASSSH=1319&AFORMNAME=&ATAG=INPUT&ATAGTYPE=text&ATAGID=&ATAGNAME=&ATAGVALUE=%E6%89%AC%E5%B7%9E%E4%B8%9C%E7%91%9E%E4%BC%A0%E6%84%9F%E6%8A%80%E6%9C%AF%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&ATAGURL=&ATAGPOS=309_472_517_36&ARECOMCLICK=&ARECOMSHOWCLICK=&ATAGTIMES=1659&AMID=1758505913747877&AEVTMID=&ASENDID=1758505937650&ARANDID=183440147696640783&ARANDOM=0.6834401476966407&ARESEND=0'

response = ses.post('https://cdn.yeefx.cn/logcount.html', params=params, headers=headers, data=data)


# 请求验证码 GET请求
getVerify = 'https://public.creditchina.gov.cn/private-api/verify/getVerify'

# 需要参数_v 随机数 random.random()
resGetVerify = ses.get(url=getVerify, params=str(random.random()), headers=headers, timeout=30)

print(resGetVerify.text)
print(resGetVerify.status_code)




