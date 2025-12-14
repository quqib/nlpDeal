import pandas as pd
import glob

KEY_COL = "统一社会信用代码"
VALUE_COL = "企业名称"

excel_files = glob.glob(r'./data/*.xlsx')
if not excel_files:
    raise Exception("未找到 Excel 文件")

# =========================
# 1. 构建 “信用代码 → 企业名称” 映射表（已修复 nan / E 问题）
# =========================
name_map = {}

for file in excel_files:
    df = pd.read_excel(
        file,
        dtype={KEY_COL: str, VALUE_COL: str}  # ⭐ 关键：强制文本
    )

    # 清洗字段
    df[KEY_COL] = (
        df[KEY_COL]
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA})
    )

    df[VALUE_COL] = (
        df[VALUE_COL]
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA})
    )

    # 构建映射
    for code, name in zip(df[KEY_COL], df[VALUE_COL]):
        if pd.isna(code) or pd.isna(name):
            continue

        # 先到先得（如需覆盖可改）
        if code not in name_map:
            name_map[code] = name


# =========================
# 2. 用第一个 Excel 作为输出基准
# =========================
result_df = pd.read_excel(
    excel_files[0],
    dtype={KEY_COL: str}
)

result_df[KEY_COL] = result_df[KEY_COL].str.strip()

# =========================
# 3. 回填企业名称
# =========================
result_df[VALUE_COL] = result_df[KEY_COL].map(name_map)

# =========================
# 4. 输出结果
# =========================
result_df.to_excel("name_reault.xlsx", index=False)

print("完成：已修复 nan / 科学计数法问题，安全生成 name_reault.xlsx")
