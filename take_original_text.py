import json
import re

# 讀取 JSON 檔
with open("ManualTransFile.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 正則：只保留含有日文假名或漢字的 key
jp_pattern = re.compile(r'[\u3040-\u30FF\u4E00-\u9FFF]+')

# 篩選 key
japanese_lines = [k for k in data.keys() if jp_pattern.search(k)]

# 輸出成純文字檔
with open("output.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(japanese_lines))

print("✅ 輸出完成，純日文句子已存入 output.txt")

