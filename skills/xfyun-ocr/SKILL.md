---
name: xfyun-ocr
description: iFlytek OCR LLM (通用文档识别/OCR大模型) — recognize text from images using Spark-based OCR engine. Supports formulas, tables, columns, and complex layouts. Pure Python stdlib, no pip dependencies.
---

# xfyun-ocr

Recognize text from images using iFlytek's Spark-based OCR LLM engine (通用文档识别/OCR大模型). Supports complex layouts including formulas, tables, columns, watermarks, and more.

## Setup

1. Create an app at [讯飞控制台](https://console.xfyun.cn) with 通用文档识别 (OCR大模型) service enabled
2. Set environment variables:
   ```bash
   export XFYUN_APP_ID="your_app_id"
   export XFYUN_API_KEY="your_api_key"
   export XFYUN_API_SECRET="your_api_secret"
   ```

## Usage

### Basic OCR

```bash
python3 scripts/ocr.py image.jpg
```

### Markdown output (great for documents with tables/formulas)

```bash
python3 scripts/ocr.py document.png --markdown
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `image` | | Image file path (.jpg, .jpeg, .png, .bmp) |
| `--markdown` | `-m` | Output in markdown format (shortcut for `--format json,markdown`) |
| `--format` | `-f` | Result format: `json`, `json,markdown`, `json,sed`, `json,markdown,sed` |
| `--result-option` | | `normal`, `normal,char` (with char coords), `normal,no_line_position` |
| `--raw` | | Output raw API JSON response |
| `--raw-result` | | Output decoded result JSON only |

### Examples

```bash
# OCR a receipt
python3 scripts/ocr.py receipt.jpg

# Document with tables → markdown
python3 scripts/ocr.py document.png -m

# Formula recognition
python3 scripts/ocr.py formula.png --markdown

# With character-level coordinates
python3 scripts/ocr.py image.jpg --result-option normal,char --raw-result

# Raw API response for debugging
python3 scripts/ocr.py image.jpg --raw
```

## Notes

- **Image formats**: .jpg, .jpeg, .png, .bmp
- **Max image size**: ~10MB (base64 encoded)
- **Auth**: HMAC-SHA256 signed URL
- **Endpoint**: `POST https://cbm01.cn-huabei-1.xf-yun.com/v1/private/se75ocrbm`
- **Env vars**: `XFYUN_APP_ID`, `XFYUN_API_KEY`, `XFYUN_API_SECRET`
- **Capabilities**: formulas, tables, columns, watermarks, seals, QR codes, barcodes, code blocks, footnotes
- **Result format**: supports JSON structured output, Markdown, and SED (Simple Element Document)
