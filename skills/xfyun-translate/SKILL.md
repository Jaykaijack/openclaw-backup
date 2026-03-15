---
name: xfyun-translate
description: iFlytek Machine Translation (机器翻译) — translate text between Chinese, English, Japanese, Korean, French, Spanish, German, Russian, Arabic, Thai, Vietnamese, and many more languages. Use when the user wants to translate text. Pure Python stdlib, no pip dependencies.
---

# xfyun-translate

Translate text using iFlytek's Machine Translation API (机器翻译). Supports 70+ language pairs.

## Setup

1. Create an app at [讯飞控制台](https://console.xfyun.cn) with 机器翻译 service enabled
2. Set environment variables:
   ```bash
   export XFYUN_APP_ID="your_app_id"
   export XFYUN_API_KEY="your_api_key"
   export XFYUN_API_SECRET="your_api_secret"
   ```

## Usage

### Basic translation (Chinese → English by default)

```bash
python3 scripts/translate.py "你好世界"
```

### Specify source and target language

```bash
python3 scripts/translate.py -s en -t cn "Hello world"
```

### Read from stdin

```bash
echo "こんにちは" | python3 scripts/translate.py - -s ja -t cn
```

### Read from file

```bash
python3 scripts/translate.py -f document.txt -s cn -t en
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `text` | | Text to translate (use `-` for stdin) |
| `--file` | `-f` | Read text from a file |
| `--from` | `-s` | Source language code (default: `cn`) |
| `--to` | `-t` | Target language code (default: `en`) |
| `--verbose` | `-v` | Show source/target language labels |
| `--raw` | | Output raw JSON response |

### Common language codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| `cn` | 中文 | `en` | English |
| `ja` | 日语 | `ko` | 韩语 |
| `fr` | 法语 | `de` | 德语 |
| `es` | 西班牙语 | `ru` | 俄语 |
| `ar` | 阿拉伯语 | `th` | 泰语 |
| `vi` | 越南语 | `pt` | 葡萄牙语 |
| `it` | 意大利语 | `tr` | 土耳其语 |

Aliases are supported: `zh`→`cn`, `chinese`→`cn`, `english`→`en`, `japanese`→`ja`, etc.

Full language list: <https://www.xfyun.cn/doc/nlp/xftrans/API.html>

### Examples

```bash
# Chinese to English
python3 scripts/translate.py "人工智能改变世界"

# English to Chinese
python3 scripts/translate.py -s en -t cn "Artificial intelligence changes the world"

# Japanese to Chinese
python3 scripts/translate.py -s ja -t cn "おはようございます"

# Verbose output with language labels
python3 scripts/translate.py -v "你好"

# Raw JSON for debugging
python3 scripts/translate.py --raw "测试翻译"
```

## Output

- Default: translated text only (stdout)
- `--verbose`: shows source and target with language labels
- `--raw`: full API JSON response

## Notes

- **Auth**: HMAC-SHA256 with Digest header (SHA-256 of body) — different from some other xfyun APIs
- **Endpoint**: `POST https://itrans.xfyun.cn/v2/its`
- **Env vars**: `XFYUN_APP_ID`, `XFYUN_API_KEY`, `XFYUN_API_SECRET`
- **Text is base64-encoded** in the request body
- **No pip deps**: Uses only Python stdlib (`urllib`, `hmac`, `hashlib`, `json`, etc.)
