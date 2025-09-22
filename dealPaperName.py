import time
import re
import pandas as pd
import requests


# 解析数据 (通过名称查询到其编码)
def parase_data(data, comName):
    try:
        dataJson = data.json()
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


def get_code(comName):
    code = ''
    params = {
        '_': f'{int(time.time()*1000)}',
    }

    json_data = {
        'keyword': comName,
    }
    time.sleep(0.5)
    response = requests.post(
        'https://capi.tianyancha.com/cloud-tempest/search/suggest/company/main',
        params=params,
        headers=headers,
        json=json_data,
        timeout=20
    )

    code = parase_data(response, comName)

    return code

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
        end_idx = min(start_idx + batch_size, total_rows)
        batch_indices = list(range(start_idx, end_idx))

        print(f"处理第 {start_idx + 1} 到 {end_idx} 行...")

        # 提取当前批次的企业名称
        batch_companies = df.loc[batch_indices, '企业名称']

        # 处理每条数据
        for idx, company_name in zip(batch_indices, batch_companies):
            if pd.isna(company_name) or not str(company_name).strip():
                continue  # 跳过空值
            credit_code = get_code(company_name)
            df.loc[idx, '统一社会信用代码'] = credit_code  # 直接在 df 中赋值

        # === 每批处理完，立即写回 Excel 文件 ===
        # 使用 openpyxl 引擎，避免覆盖其他格式（如果原文件有样式可保留）
        with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False)

        print(f"已回填第 {start_idx + 1} 到 {end_idx} 行数据到 {output_path}")

    print("所有数据处理完成，已保存结果。")
    return df


# === 调用示例 ===
if __name__ == "__main__":
    input_file = "code.xlsx"  # 输入文件
    output_file = "企业数据_回填结果_code.xlsx"  # 输出文件（可与输入相同）

    result_df = process_excel_in_batches(input_file, output_file, batch_size=100)





