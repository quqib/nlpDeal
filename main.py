import time
import pandas as pd
from DrissionPage import WebPage, ChromiumOptions
from click import clear

co = ChromiumOptions().set_paths(browser_path=r"/opt/apps/cn.google.chrome/files/google/chrome/google-chrome")

page = WebPage('d', chromium_options=co)

page.get('https://www.qcc.com/')

# 点击登录
# page.ele('xpath:/html/body/div/div[1]/div/div/div[2]/div/div[1]/button').click()

# 点击×
# page.ele('xpath:/html/body/div[2]/div/div[2]/div/div[2]/div/i').click()
# time.sleep(20)

# 获取输入框
page.ele('xpath://*[@id="searchKey"]').input("春光印刷装订厂")

# 点击查询
page.ele('xpath:/html/body/div/div[2]/section[1]/div/div/div/div[1]/div/div/span/button').click()

# 页面发生跳转
time.sleep(5)

def get_code(company_name):
    time.sleep(3)
    # 先清理输入框
    page.ele('xpath:/html/body/div/div[1]/div/div/div/div[2]/div/span/span/span[1]/span').click()
    page.ele('xpath:/html/body/div/div[1]/div/div/div/div[2]/div/span/span/span[1]/input').clear()
    # 获取输入框
    page.ele('xpath:/html/body/div/div[1]/div/div/div/div[2]/div/span/span/span[1]/input').input(company_name)

    # 点击查询
    page.ele('xpath:/html/body/div/div[1]/div/div/div/div[2]/div/span/span/span[2]/button').click()

    # 解析页面
    # 获取公司名称
    com_name = page.ele('xpath:/html/body/div/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/span/span[1]/a')
    if com_name:
        com_name = com_name.text
    else:
        com_name = ''


    # 判断名称与EXCEL表格中的名称是否相等
    if com_name == company_name:
        # 获取页面统一编码
        page_code = page.ele('xpath:/html/body/div/div[2]/div[2]/div[3]/div/div[2]/div/table/tr[1]/td[3]/div/div[3]/div[1]/span[4]/span/span/span[1]')
        if page_code:
            page_code = page_code.text
        else:
            page_code = ''
    else:
        page_code = ''

    return page_code


def process_excel_in_batches(file_path, output_path, batch_size=5):
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
            # 如果存在值，设置为空
            if pd.isna(company_name) or not str(company_name).strip():
                continue  # 跳过空值

            # 判断其是否为nan
            if pd.notna(df.loc[idx, '统一社会信用代码']):
                credit_code = df.loc[idx, '统一社会信用代码']
            else:
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
    input_file = "剩余公司名.xlsx"  # 输入文件
    output_file = "剩余公司名结果.xlsx"  # 输出文件（可与输入相同）

    result_df = process_excel_in_batches(input_file, output_file, batch_size=5)









