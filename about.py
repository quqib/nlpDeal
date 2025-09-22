import pandas as pd

# 1. 读取两个 Excel 文件
df_a = pd.read_excel('./企业数据_回填结果_name_3.xlsx')  # 源：提供 【统一社会信用代码 → 企业名称】 映射
df_b = pd.read_excel('./企业数据_回填结果_name_two.xlsx')  # 目标：需要填充的文件
# df_b = pd.read_excel('./企业数据_回填结果_name_two.xlsx')  # 目标：需要填充的文件

# 2. 检查必要列是否存在
required_cols = ['企业名称', '统一社会信用代码']
if not all(col in df_a.columns for col in required_cols):
    raise ValueError(f"源文件必须包含列: {required_cols}")
if not all(col in df_b.columns for col in required_cols):
    raise ValueError(f"目标文件必须包含列: {required_cols}")

# 3. 构建 映射字典：统一社会信用代码 -> 企业名称（去重）
# 注意：我们以“统一社会信用代码”为键，映射到“企业名称”
mapping_dict = df_a.drop_duplicates(subset='统一社会信用代码').set_index('统一社会信用代码')['企业名称'].to_dict()

# 4. 定义函数：仅在“企业名称”为空时，尝试通过“统一社会信用代码”回填
def fill_name_if_missing(row, mapping):
    code = row['统一社会信用代码']
    current_name = row['企业名称']

    # 如果当前企业名称为空（NaN 或 空字符串），尝试用信用代码查找补全
    if pd.isna(current_name) or str(current_name).strip() == '':
        return mapping.get(code, current_name)  # 找得到就填，找不到保留原值（NaN）
    else:
        return current_name  # 已有名称，不覆盖

# 应用函数补全“企业名称”
df_b['企业名称'] = df_b.apply(fill_name_if_missing, axis=1, mapping=mapping_dict)

# 5. 保存结果
output_file = '企业数据_回填结果_name_three.xlsx'
df_b.to_excel(output_file, index=False)

print(f"数据填充完成，已保存至 '{output_file}'")
print("✅ 说明：仅对‘企业名称’为空的行，使用‘统一社会信用代码’进行了回填，已有名称未被覆盖。")














exit()
import pandas as pd

# 1. 读取两个 Excel 文件
df_a = pd.read_excel('./企业数据_回填结果_name_2.xlsx')  # 源：提供【企业名称 → 统一社会信用代码】映射
df_b = pd.read_excel('./企业数据_回填结果_name_two.xlsx')  # 目标：需要填充但不覆盖的文件

# 2. 检查必要列是否存在
required_cols = ['企业名称', '统一社会信用代码']
if not all(col in df_a.columns for col in required_cols):
    raise ValueError(f"源文件必须包含列: {required_cols}")
if not all(col in df_b.columns for col in required_cols):
    raise ValueError(f"目标文件必须包含列: {required_cols}")

# 3. 构建 映射字典：企业名称 -> 统一社会信用代码（去重）
mapping_dict = df_a.drop_duplicates(subset='企业名称').set_index('企业名称')['统一社会信用代码'].to_dict()


# 4. 定义一个函数，在不覆盖已有值的前提下补充空值
def fill_if_missing(row, mapping):
    name = row['企业名称']
    current_code = row['统一社会信用代码']

    # 如果当前信用代码为空（NaN 或 空字符串），尝试从映射中补全
    if pd.isna(current_code) or str(current_code).strip() == '':
        return mapping.get(name, current_code)  # 找得到就填，找不到还是保留原值（即 NaN）
    else:
        return current_code  # 已有值，不覆盖


# 应用该逻辑
df_b['统一社会信用代码'] = df_b.apply(fill_if_missing, axis=1, mapping=mapping_dict)

# 5. 保存结果
output_file = '企业数据_回填结果_name_填充后_two.xlsx'
df_b.to_excel(output_file, index=False)

print(f"数据填充完成，已保存至 '{output_file}'")
print("✅ 说明：仅对‘统一社会信用代码’为空的行进行了补充，已有数据未被覆盖。")



