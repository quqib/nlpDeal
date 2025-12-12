import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


from datetime import datetime, timezone
import urllib.parse




# 解析数据 (获取EXCEL数据)
def process_excel_in_batches(file_path, output_path, batch_size=100):
    """
    读取 Excel，分批处理企业名称，回填统一社会信用代码
    """
    # 1. 读取原始数据
    df = pd.read_excel(file_path)

    # 确保列名正确（可根据实际调整）
    if '企业名称' not in df.columns or '统一社会信用代码' not in df.columns:
        raise ValueError("Excel 必须包含 '企业名称' 和 '统一社会信用代码' 列")

    total_rows = len(df)
    print(f"共 {total_rows} 条数据，开始分批处理...")

    # 2. 遍历数据，处理并保存中间结果
    for start_idx in range(0, total_rows, batch_size):
        if start_idx < 600:
            continue
        end_idx = min(start_idx + batch_size, total_rows)
        batch_indices = list(range(start_idx, end_idx))

        print(f"处理第 {start_idx + 1} 到 {end_idx} 行...")

        # 提取当前批次的统一社会信用代码
        batch_companies = df.loc[batch_indices, '统一社会信用代码']

        # 处理每条数据
        for idx, com_code in zip(batch_indices, batch_companies):
            if pd.isna(com_code) or not str(com_code).strip():
                continue  # 跳过空值
            # 天眼查
            # com_name = get_name_t(com_code)
            # 企查查
            # com_name = get_name(com_code)
            # 从zyt给的接口拿
            com_name = code_find_name(com_code)
            df.loc[idx, '企业名称'] = com_name  # 直接在 df 中赋值

        # === 每批处理完，立即写回 Excel 文件 ===
        # 使用 openpyxl 引擎，避免覆盖其他格式（如果原文件有样式可保留）
        with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False)

        print(f"已回填第 {start_idx + 1} 到 {end_idx} 行数据到 {output_path}")

    print("所有数据处理完成，已保存结果。")
    return df

def get_name(searchKey):
    try:
        cookies = {
            'qcc_did': '0b099d9c-9cca-4bfb-8024-533a6882b6cb',
            'QCCSESSID': 'df3f574440f8a374ff94b0d9c7',
            'UM_distinctid': '1993108dbe116-0e95cdcb9164b6-12462c6c-1fa400-1993108dbe2b5c',
            '_c_WBKFRo': 'ac9g9nxgq5OaWlb3bNnY0F3cn94Oocdinkx7gRzT',
            '_nb_ioWEgULi': '',
            'acw_tc': '1a0c380b17574731650292265e087d4d458eb100a92aae415e9608a0f2cb87',
            'CNZZDATA1254842228': '1967424861-1757464288-https%253A%252F%252Fcn.bing.com%252F%7C1757474054',
        }

        headers = {
            '6bd1f3a0de81caee18f0': '87b9d3c96e061ff8acb4106dfbf627e5e7b072ce6c017e4109623ce0197a08b5e9a91d8edae91a51f2ec25b92c5dd2114a6c44a04812aafffa34b2bfcb856b36',
            'authority': 'www.qcc.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8',
            'cache-control': 'no-cache',
            # 'cookie': 'qcc_did=0b099d9c-9cca-4bfb-8024-533a6882b6cb; QCCSESSID=df3f574440f8a374ff94b0d9c7; UM_distinctid=1993108dbe116-0e95cdcb9164b6-12462c6c-1fa400-1993108dbe2b5c; _c_WBKFRo=ac9g9nxgq5OaWlb3bNnY0F3cn94Oocdinkx7gRzT; _nb_ioWEgULi=; acw_tc=1a0c380b17574731650292265e087d4d458eb100a92aae415e9608a0f2cb87; CNZZDATA1254842228=1967424861-1757464288-https%253A%252F%252Fcn.bing.com%252F%7C1757474054',
            'pragma': 'no-cache',
            'referer': 'https://www.qcc.com/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'x-pid': 'a4d409a8377f5a4723fcb014717d62fa',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'mindType': '9',
            'pageSize': '5',
            'person': 'true',
            'searchKey': searchKey,
            'suggest': 'true',
        }

        response = requests.get('https://www.qcc.com/api/search/searchMind', params=params, cookies=cookies,
                                headers=headers)

        resJson = response.json()
        data_dict = resJson.get('list')[0]
        com_name = data_dict.get('Name')
        return com_name
    except:
        return ''


# 正则表达抽取统一社会编码
def extract_credit_code(text):
    """
    从文本中提取统一社会信用代码：后面的第一个字母数字组合
    """
    pattern = r"统一社会信用代码：([A-Za-z0-9]+)"

    match = re.search(pattern, text)
    if match:
        credit_code = match.group(1)  # group(1) 是括号内的捕获内容
        print("提取到的统一社会信用代码:", credit_code)
        return credit_code
    else:
        print("未找到统一社会信用代码")
        return ''


# 解析页面
def parse_div_from_html(response_text, com_code, target_class="index_list-content__wjkNi"):
    """
    解析 HTML 文本，查找指定 class 的 div 元素
    """
    # 公司名称
    com_name = ''
    # 将 response.text 解析为 HTML
    soup = BeautifulSoup(response_text, 'html.parser')

    # 查找 class 为 index_list-content__wjkNi 的 div
    target_div = soup.find('div', class_='index_list-content__wjkNi')

    if target_div:
        print("找到目标 div 元素：")
        # 输出该 div 的文本内容
        print(target_div.get_text(strip=True))
        # 查找该div下class 为index_search-box__7YVh6的数据
        all_div_targets = target_div.find_all('div', class_='index_search-box__7YVh6')
        for all_div_target in all_div_targets:
            # 查找该div下的公司name
            div_name = all_div_target.find('div', class_='index_header__x2QZ3')
            if div_name:
                com_name = div_name.get_text(strip=True)

                # 获取公司统一社会信用代码
                code = extract_credit_code(all_div_target.get_text(strip=True))

                if code == com_code:
                    return com_name

                else:
                    continue
            else:
                continue

    else:
        print(f"未找到 class='{target_class}' 的 div 元素")
        com_name = ''

    print(com_name)
    return com_name


# 从天眼查解析获取
def get_name_t(code):
    com_name = ''
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Version": "TYC-Web",
        "X-Tycid": "a08b2c108d5411f0b5376328c2c6d1d5"
    }
    time.sleep(2)
    # 通过统一社会编码来获取名称
    urlCode = f'https://www.tianyancha.com/nsearch?key={code}'
    responseCode = requests.get(urlCode, headers=headers, timeout=30)
    com_name = parse_div_from_html(responseCode.text, code)
    return com_name.replace('存续', '')


# 从zyt给的接口拿
def code_find_name(code):
    com_name = ''
    try:
        cookies = {
            'safeline_token': 'AJkD2esAAAAAAAAAAAAAAABOp88QmwEAAAjEsNWY7bHs9LXqfccWNoiTdjJv',
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'SESSION=e9c95d7b-bfc0-41bd-a3df-08155dcafe2c; safeline_token=AJkD2esAAAAAAAAAAAAAAADgymkymQEAADtj0dwzdkgpVgOW1nHAdC+nJfl8; 9b928db0-e5ea-45e7-a3b1-392825e21a5c=WyI1OTUyNDUwMDUiXQ; JSESSIONID=e9c95d7b-bfc0-41bd-a3df-08155dcafe2c; SERVERID=8638b73cb1e93cbe0e40fab72203dd4b|1757487458|1757487418',
            'Origin': 'http://www.jsgsj.gov.cn:5888',
            'Referer': 'http://www.jsgsj.gov.cn:5888/province/loginReport.jsp',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        # 获取当前 UTC 时间（推荐方式）
        now_utc = datetime.now(timezone.utc)

        # 格式化为所需字符串
        formatted_time = now_utc.strftime("Wed %b %d %Y %H:%M:%S GMT+0000 (GMT)")

        # URL 编码（使用 quote_plus 以将空格转为 +）
        temp_encoded = urllib.parse.quote_plus(formatted_time)

        params = {
            'findCorpNameAndLiaisonName': 'true',
        }
        time.sleep(0.20)
        data = f'regNo={code}&temp={temp_encoded}'

        response = requests.post(
            'http://www.jsgsj.gov.cn:5888/province/loginServlet.json',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )

        com_name = response.json().get("content").get("CORP_NAME")

    except:
        com_name = ''
    print(f'获取到名称------{com_name}------')
    return com_name


# === 调用示例 ===
if __name__ == "__main__":

    input_file = "resource.xlsx"  # 输入文件
    output_file = "企业数据_回填结果_name_2.xlsx"  # 输出文件（可与输入相同）
    result_df = process_excel_in_batches(input_file, output_file, batch_size=100)






















exit()
# 解析数据 (通过名称查询到其编码)
def parase_data(data, comName):
    try:
        dataJson = data.json
        # 获取公司列表
        companySuggestList = dataJson.get('data').get('companySuggestList')
        for companyName in companySuggestList:
            if companyName.get('comName') == comName:
                return companyName.get('taxCode')
    except:
        return ''




headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Version": "TYC-Web",
    "X-Tycid": "a08b2c108d5411f0b5376328c2c6d1d5"
}

params = {
    '_': f'{int(time.time()*1000)}',
}

json_data = {
    'keyword': '国网江苏省电力有限公司',
}

response = requests.post(
    'https://capi.tianyancha.com/cloud-tempest/search/suggest/company/main',
    params=params,
    headers=headers,
    json=json_data,
)





# 通过统一社会编码来获取名称
urlCode = 'https://www.tianyancha.com/nsearch?key=91320000134766570R'
responseCode = requests.get(urlCode, headers=headers)

# 正则表达抽取统一社会编码
def extract_credit_code(text):
    """
    从文本中提取统一社会信用代码：后面的第一个字母数字组合
    """
    pattern = r"统一社会信用代码：([A-Za-z0-9]+)"

    match = re.search(pattern, text)
    if match:
        credit_code = match.group(1)  # group(1) 是括号内的捕获内容
        print("提取到的统一社会信用代码:", credit_code)
        return credit_code
    else:
        print("未找到统一社会信用代码")
        return ''


# 解析页面
def parse_div_from_html(response_text, com_code, target_class="index_list-content__wjkNi"):
    """
    解析 HTML 文本，查找指定 class 的 div 元素
    """
    # 公司名称
    com_name = ''
    # 将 response.text 解析为 HTML
    soup = BeautifulSoup(response_text, 'html.parser')

    # 查找 class 为 index_list-content__wjkNi 的 div
    target_div = soup.find('div', class_='index_list-content__wjkNi')

    if target_div:
        print("找到目标 div 元素：")
        # 输出该 div 的文本内容
        print(target_div.get_text(strip=True))
        # 查找该div下class 为index_search-box__7YVh6的数据
        all_div_targets = target_div.find_all('div', class_='index_search-box__7YVh6')
        for all_div_target in all_div_targets:
            # 查找该div下的公司name
            div_name = all_div_target.find('div', class_='index_header__x2QZ3')
            if div_name:
                com_name = div_name.get_text(strip=True)

                # 获取公司统一社会信用代码
                code = extract_credit_code(all_div_target.get_text(strip=True))

                if code == com_code:
                    return com_name

                else:
                    continue
            else:
                continue

    else:
        print(f"未找到 class='{target_class}' 的 div 元素")
        com_name = ''


    print(com_name)
    return com_name
print(responseCode.text)
parse_div_from_html(responseCode.text)



