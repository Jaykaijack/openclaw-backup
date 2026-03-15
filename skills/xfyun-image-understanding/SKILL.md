---
name: xfyun-image-understanding
description: iFlytek Image Understanding (图片理解) — analyze and answer questions about images using Spark Vision model. WebSocket API, pure Python stdlib, no pip dependencies.
---

# xfyun-image-understanding

Analyze images and answer questions about their content using iFlytek's Spark Vision model (图片理解).

## Setup

1. Create an app at [讯飞控制台](https://console.xfyun.cn) with 图片理解 service enabled
2. Set environment variables:
   ```bash
   export XFYUN_APP_ID="your_app_id"
   export XFYUN_API_KEY="your_api_key"
   export XFYUN_API_SECRET="your_api_secret"
   ```

## Usage

### Describe an image

```bash
python3 scripts/image_understanding.py photo.jpg
```

### Ask a question about an image

```bash
python3 scripts/image_understanding.py photo.jpg -q "图片里有什么动物？"
```

### Use basic model (lower token cost)

```bash
python3 scripts/image_understanding.py photo.jpg --domain general
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `image` | | Image file path (.jpg, .jpeg, .png) |
| `--question` | `-q` | Question about the image (default: describe) |
| `--domain` | `-d` | `imagev3` (advanced, default) or `general` (basic, fixed 273 tokens/image) |
| `--temperature` | `-t` | Sampling temperature (0,1], default 0.5 |
| `--max-tokens` | | Max response tokens 1-8192, default 2048 |
| `--raw` | | Output raw WebSocket JSON frames |

### Examples

```bash
# OCR a receipt
python3 scripts/image_understanding.py receipt.png -q "总金额是多少？"

# Identify objects
python3 scripts/image_understanding.py scene.jpg -q "图片中有哪些物体？"

# Low-cost basic model
python3 scripts/image_understanding.py chart.png -q "图表的趋势是什么？" -d general
```

## Notes

- **Image formats**: .jpg, .jpeg, .png
- **Max image size**: 4MB
- **Max tokens**: 8192 (input + output combined)
- **Auth**: HMAC-SHA256 signed WebSocket URL
- **Endpoint**: `wss://spark-api.cn-huabei-1.xf-yun.com/v2.1/image`
- **Pure stdlib**: No pip dependencies — uses built-in `socket` + `ssl` for WebSocket
- **Model versions**: `imagev3` (advanced, dynamic token cost) vs `general` (basic, fixed 273 tokens/image)
