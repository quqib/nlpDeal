import pandas as pd
import re

input_csv = "T_CORP1212_202512121135.csv"
output_xlsx = "clean.xlsx"

clean_lines = []

# ① 先按“纯文本”读取
with open(input_csv, "r", encoding="utf-8", errors="replace") as f:
    for line in f:
        # 去掉换行
        line = line.rstrip("\n")

        # ② 修复 DBeaver 导出的混合分隔符
        # 把 "\t," 或 "\"\t," 统一替换为 ","
        line = re.sub(r'"\s*\t\s*,', '",', line)

        # ③ 去掉残余的 tab
        line = line.replace("\t", "")

        clean_lines.append(line)

# ④ 把“修好的内容”交给 pandas
from io import StringIO

fixed_text = "\n".join(clean_lines)
df = pd.read_csv(StringIO(fixed_text), sep=",", dtype=str)

# ⑤ 再清洗一遍列名（保险）
df.columns = (
    df.columns
      .str.replace('"', '', regex=False)
      .str.strip()
)

print("最终列名：")
for c in df.columns:
    print(repr(c))

# ⑥ 输出 Excel
df.to_excel(output_xlsx, index=False)

print(f"\n✅ 修复完成，已输出：{output_xlsx}")
