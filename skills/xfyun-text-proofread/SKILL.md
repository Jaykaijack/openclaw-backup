---
name: xfyun-text-proofread
description: iFlytek Official Document Proofreading (公文校对) — detect and correct errors in Chinese text including typos, punctuation, word order, factual mistakes, sensitive content, and more (27 error types). Supports up to 220,000 characters. Use when the user wants to proofread, check, or correct Chinese text, especially official documents. Pure Python stdlib, no pip dependencies.
---

# xfyun-text-proofread

Proofread Chinese text using iFlytek's Official Document Proofreading API (公文校对). Detects 27 types of errors across three categories:

**文字标点差错**: 错别字、多字、少字、语义重复、语序错误、句式杂糅、标点符号、量词单位、数字差错、句子查重、序号检查

**知识性差错**: 地理名词、机构名称、专有名词及术语、常识差错、媒体报道禁用词和慎用词

**内容导向风险**: 涉低俗辱骂、其他敏感内容

## Setup

1. Create an app at [讯飞控制台](https://console.xfyun.cn) with 公文校对 service enabled
2. Set environment variables:
   ```bash
   export XFYUN_APP_ID="your_app_id"
   export XFYUN_API_KEY="your_api_key"
   export XFYUN_API_SECRET="your_api_secret"
   ```

## Usage

### Basic proofreading

```bash
python3 scripts/text_proofread.py "第二个百年目标"
```

### Read from stdin

```bash
echo "我们要加强对蓝球运动的推广" | python3 scripts/text_proofread.py -
```

### Read from file

```bash
python3 scripts/text_proofread.py --file document.txt
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `text` | | Text to proofread (use `-` for stdin) |
| `--file` | `-f` | Read text from a file |
| `--raw` | | Output decoded JSON response |

### Examples

```bash
# Proofread a sentence
python3 scripts/text_proofread.py "我国加强蓝球运动的推广力度"

# Proofread a long document from file
python3 scripts/text_proofread.py -f report.txt

# Pipe from clipboard or other tools
pbpaste | python3 scripts/text_proofread.py -

# Raw JSON for debugging
python3 scripts/text_proofread.py --raw "测试文本"
```

## Output

- **✅ 无错误** — text passed proofreading with no issues
- **🔍 发现 N 处问题** — lists each error with:
  - Error word + category
  - Explanation
  - Context in the original text
  - Position and length
  - Suggested action (标记/替换/删除)
  - Correction suggestions

## Notes

- **Max text length**: 220,000 characters per request (auto-truncated with warning)
- **Auth**: HMAC-SHA256 signed URL (host + date + request-line → signature → authorization)
- **Endpoint**: `POST https://cn-huadong-1.xf-yun.com/v1/private/s37b42a45`
- **Env vars**: `XFYUN_APP_ID`, `XFYUN_API_KEY`, `XFYUN_API_SECRET`
- **No pip deps**: Uses only Python stdlib (`urllib`, `hmac`, `hashlib`, `json`, etc.)
- **Text is base64-encoded** in the request body; response text field is also base64-encoded
