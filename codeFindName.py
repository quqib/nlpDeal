import time

import requests

def code_find_name(code):
    com_name = ''
    try:
        cookies = {
            'SESSION': 'e9c95d7b-bfc0-41bd-a3df-08155dcafe2c',
            'safeline_token': 'AJkD2esAAAAAAAAAAAAAAADgymkymQEAADtj0dwzdkgpVgOW1nHAdC+nJfl8',
            '9b928db0-e5ea-45e7-a3b1-392825e21a5c': 'WyI1OTUyNDUwMDUiXQ',
            'JSESSIONID': 'e9c95d7b-bfc0-41bd-a3df-08155dcafe2c',
            'SERVERID': '8638b73cb1e93cbe0e40fab72203dd4b|1757487458|1757487418',
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

        params = {
            'findCorpNameAndLiaisonName': 'true',
        }
        time.sleep(0.5)
        data = f'regNo={code}&temp=Wed+Sep+10+2025+06%3A57%3A38+GMT%2B0000+(GMT)'

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

    return com_name



