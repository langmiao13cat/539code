import pandas as pd
import numpy as np
from jinja2 import Environment, FileSystemLoader

# 初始數據
data = {
    "日期": ["2024/05/08", "2024/05/07", "2024/05/06", "2024/05/04", "2024/05/03",
             "2024/05/02", "2024/05/01", "2024/04/30", "2024/04/29", "2024/04/27"],
    "今彩539中獎號碼": ["12, 13, 16, 26, 37", "04, 09, 18, 25, 39", "12, 28, 31, 35, 39",
                    "02, 07, 13, 18, 28", "05, 06, 11, 16, 37", "03, 06, 13, 28, 35",
                    "09, 24, 32, 36, 39", "03, 07, 12, 17, 37", "04, 10, 12, 21, 27",
                    "09, 15, 22, 34, 36"]
}

# 轉換為 DataFrame
df = pd.DataFrame(data)

# 將中獎號碼分割成多列
winning_numbers = df["今彩539中獎號碼"].str.split(", ", expand=True)
winning_numbers.columns = [f"號碼{i+1}" for i in range(winning_numbers.shape[1])]

# 合併到主 DataFrame
df_combined = pd.concat([df, winning_numbers], axis=1)

# 計算所有號碼的機率
all_numbers = pd.concat([df_combined[col] for col in df_combined.columns if col.startswith("號碼")]).dropna()
all_numbers = pd.to_numeric(all_numbers, errors='coerce')
frequency = all_numbers.value_counts().reindex(range(1, 40), fill_value=0)
probabilities = frequency / frequency.sum()

# 根據機率生成 3 組最佳組合
np.random.seed(42)
best_combinations = []
for _ in range(3):
    combination = np.random.choice(range(1, 40), size=5, replace=False, p=probabilities)
    best_combinations.append(sorted(combination))

# Jinja2 模板環境
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")

# 渲染模板
html_content = template.render(combinations=best_combinations)

# 將結果保存為靜態 HTML 檔案
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("靜態網站已生成並保存為 index.html")
