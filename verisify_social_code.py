import time
import random
import requests

# 请求之前访问一个网址检查是否存在 cookienm POST请求
logcountUrl = f'https://cdn.yeefx.cn/logcount.html?website=10019513&server=s1&datatype=click_change&sendid={int(time.time()*1000)}'



# 请求验证码 GET请求
getVerify = 'https://public.creditchina.gov.cn/private-api/verify/getVerify'

# 需要参数_v 随机数 random.random()
resGetVerify = requests.get(url=getVerify, params=str(random.random()), timeout=30)

print(resGetVerify.text)
print(resGetVerify.status_code)


# 检测验证码 POST请求
checkVerifyUrl = 'https://public.creditchina.gov.cn/private-api/verify/checkVerify'

# 需要一个加密参数rcwCQitg

# 需要一个表单数据 verifyInput 识别出来的验证码

# 查找接口地址 GET请求 POST也可以
searchUrl = 'https://public.creditchina.gov.cn/private-api/catalogSearch'

# 需要一个加密参数rcwCQitg





