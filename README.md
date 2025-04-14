# TransTextFotMtool

# 翻譯小助手：日文 ➜ 繁體中文 對話翻譯工具

這是一個命令列工具，可將日文逐行翻譯成自然流暢的繁體中文對話語氣。支援 GPT（OpenAI）與 DeepL 雙引擎翻譯，並提供 JSON 或 CSV 格式輸出。

---

## ✅ 功能特色

- 支援兩種翻譯平台：OpenAI GPT 與 DeepL
- 可自訂每批翻譯的行數，避免 token 過多
- 支援 JSON 與 CSV 輸出格式
- 進度條顯示翻譯進度，適合大量文本處理
- 輕量命令列介面

---

## 📁 使用說明

### 1️⃣ 準備原文檔案

先使用Mtool匯出原文json檔(.json)，再點擊exe兩下開啟程式生成固定格式原文文字檔(.txt)，或是在終端機（命令列）執行程式：

```bash
python 使用take_original_text.exe
```

也可以自己將要翻譯的日文文本存為 `output.txt`，每行一段句子。

---

### 2️⃣ 設定 `config.json`

建立一個 `config.json` 檔案，內容如下：

```json
{
  "INPUT_FILE": "output.txt",
  "OUTPUT_JSON": "translationToJson.json",
  "OUTPUT_CSV": "translationToCsv.csv",
  "WAIT_TIME": 1.5,
  "max_lines": 5,
  "deepl": {
    "api_key": "你的 DeepL API 金鑰",
    "source_lang": "JA",
    "target_lang": "ZH"
  },
  "gpt": {
    "api_key": "你的 OpenAI API 金鑰",
    "model": "gpt-3.5-turbo"
  }
}
```

- `WAIT_TIME`：每批翻譯間等待秒數，避免 API 過載
- `max_lines`：每批送出翻譯的行數（建議 3~10 行）
- `source_lang` / `target_lang`：語言代碼（JA ➜ ZH）

---

### 3️⃣ 執行程式

在終端機（命令列）執行主程式：

```bash
python translate_main.exe
```

會出現互動式選單，讓你選擇翻譯平台與輸出格式：

```
🔍 翻譯平台選擇：1. DeepL  2. GPT
請選擇翻譯方式 (1/2)：
```

```
💾 輸出格式選擇：1. JSON  2. CSV
請選擇輸出格式 (1/2)：
```

確認選項後，程式將開始翻譯並顯示進度條。

---

## 📦 輸出說明

### JSON 檔（translationToJson.json）

```json
{
  "まさかステーキのSって意味か": "難道是牛排的 S 嗎？",
  "食べていい？ やったー！": "可以吃了嗎？太棒了！"
}
```

### CSV 檔（translationToCsv.csv）

```csv
原文,,翻譯
まさかステーキのSって意味か,,難道是牛排的 S 嗎？
食べていい？ やったー！,,可以吃了嗎？太棒了！
```

---

## ⚠ 注意事項

- 使用 GPT 時，長文本可能需注意 token 限制（建議每批 5 行）
- 若發生 API 限速錯誤，可調整 `WAIT_TIME` 增加間隔
- 請確認 `config.json` 中 API 金鑰正確填寫
- 程式執行後會覆蓋原本的輸出檔案，請記得備份

---

## 📄 授權與用途

本工具自由使用與修改，適用於：

- 同人翻譯
- 遊戲對話文本翻譯
- 漫畫字幕翻譯
- 學習日文輔助工具

如需商業用途，請確保 API 使用授權範圍合法。

---

## 🙌 感謝使用

如果覺得好用歡迎點個星星 ⭐ 或提供建議！
