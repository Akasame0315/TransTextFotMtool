import requests
import json
import time
import os
import csv
import tqdm

def load_config(config_path="config.json"):
    if not os.path.exists(config_path):
        raise FileNotFoundError("找不到 config.json，請先建立設定檔。")
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
config = load_config()

# 通用設定
INPUT_FILE = config.get("INPUT_FILE", "output.txt")
OUTPUT_FILE_JSON = config.get("OUTPUT_JSON", "translationtoJson.json")
OUTPUT_FILE_CSV = config.get("OUTPUT_CSV", "translationToCSV.csv")
WAIT_TIME = config.get("WAIT_TIME", 1.5)
MAX_LINE = config.get("max_lines")  # None 表示不限制

# API Key
deepl_api_key = config.get("deepl", {}).get("api_key")
gpt_api_key = config.get("gpt", {}).get("api_key")
gpt_model = config.get("gpt", {}).get("model", "gpt-3.5-turbo")

token_limit = config.get("token_limit", {}).get("deepl", 4500)


def translate_with_deepl(text_list, source_lang, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
     # 使用列表解析式產生多個 text 欄位（requests 會自動處理） 支援多句一次翻譯
    data = [
        ('auth_key', deepl_api_key),
        ('source_lang', source_lang),
        ('target_lang', target_lang)
    ] + [('text', text) for text in text_list]
    
    try:
        response = requests.post(url, data=data, headers=headers)
        result = response.json()
        if "translations" in result:
            return [item["text"] for item in result["translations"]]
        else:
            print("❌ DeepL 翻譯失敗：", result)
            return [""] * len(text_list)
        
    except Exception as e:
        print("❌ 錯誤：", e)
        return ""
    
def translate_with_gpt(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {gpt_api_key}"
    }
    data = {
        "model":  gpt_model,  # 或使用 gpt-3.5 之類的模型
        "messages": [
            {"role": "user", "content": f"請將以下日文翻譯成優雅自然的繁體中文對話體，不要保留原文，每句對應翻譯即可：\n\n{text}"}
        ]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            print("❌ GPT翻譯失敗：", result)
            return ""
    except Exception as e:
        print("❌ GPT錯誤：", e)
        return ""

# ========== 資料處理 ========== #
def read_txt_file(file_path, max_lines=None):
    if not os.path.exists(file_path):
        print(f"❌ 找不到檔案：{file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
        return lines[:max_lines] if max_lines else lines
    
def split_into_batches(lines, batch_size):
    if batch_size is None:
        return [lines]  # 只傳回一個批次（全部資料）
    return [lines[i:i + batch_size] for i in range(0, len(lines), batch_size)]
    
# ========== 輸出函數 ========== #
def save_as_json(pairs, output_file):
    result = {original: translated for original, translated in pairs}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 儲存成功：{output_file}")

def save_as_csv(pairs, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        for original, translated in pairs:
            writer.writerow([original, "", translated])
    print(f"✅ CSV 儲存成功：{output_file}")

def main():
    # 讓使用者選擇翻譯管道
    print("🔍 翻譯平台選擇：1. DeepL  2. GPT")
    user_input = input("請選擇翻譯方式 (1/2)：").strip()
    
    if user_input == '1':
        translator = "deepl"
    elif user_input == '2':
        translator = "gpt"
    else:
        print("無效選擇，請重新執行程式並選擇有效的選項。")
        return

    # 選擇輸出格式
    print("💾 輸出格式選擇：1. JSON  2. CSV")
    format_choice = input("請選擇輸出格式 (1/2)：").strip()

    if format_choice == '1':
        output_format = "json"
    elif format_choice == '2':
        output_format = "csv"
    else:
        print("❌ 無效選擇，請重新執行程式並選擇有效的選項。")
        return
    
    # 更新 config 使其使用正確的翻譯管道
    config["translator"] = translator
    config["output_format"] = output_format
    
    # 確認輸入
    print(f"\n🔧 使用 {translator.upper()} 進行翻譯，輸出為 {output_format.upper()}，是否繼續？(Y/N)")
    if input().strip().lower() != 'y':
        print("❌ 已取消。")
        return
    
    # 取得最大處理行數，如果沒設定或為 None，就設為無限制
    max_ls = int(MAX_LINE) if MAX_LINE is not None and str(MAX_LINE).isdigit() else None

    lines = read_txt_file(INPUT_FILE, None)
    all_pairs = []

    # 分批翻譯，這裡加上 tqdm 顯示進度條
    for batch in tqdm.tqdm(split_into_batches(lines, max_ls), desc="翻譯進度", unit="批次"):
    # for batch in split_into_batches(lines, max_ls):
        joined_text = "\n".join(batch)
        if translator == "deepl":
            translated_list = translate_with_deepl(batch,
                                                        source_lang=config.get("deepl", {}).get("source_lang"),
                                                        target_lang=config.get("deepl", {}).get("target_lang"))
            for orig, trans in zip(batch, translated_list):
                all_pairs.append((orig, trans))
            time.sleep(WAIT_TIME)

        elif translator == "gpt":
            translated_block = translate_with_gpt(joined_text)
            translated_lines = [line for line in translated_block.strip().split("\n") if line.strip()]
            for i in range(len(batch)):
                orig = batch[i]
                trans = translated_lines[i] if i < len(translated_lines) else ""
                all_pairs.append((orig, trans))
            time.sleep(WAIT_TIME)

    # 輸出結果
    if output_format == "json":
        save_as_json(all_pairs, OUTPUT_FILE_JSON)
    elif output_format == "csv":
        save_as_csv(all_pairs, OUTPUT_FILE_CSV)

if __name__ == "__main__":
    main()
