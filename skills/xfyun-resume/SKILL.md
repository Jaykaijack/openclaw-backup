---
name: xfyun-resume
description: "iFlytek Smart Resume Generator (智能简历生成) — generate 1-3 professional resume templates from personal info and job requirements using iFlytek AI Resume API. Supports text input, file input, and stdin. Use when the user wants to create, generate, or draft a resume/CV. Pure Python stdlib, no pip dependencies."
---

# xfyun-resume

Generate professional resumes from personal information and job requirements using iFlytek's AI Resume API (智能简历生成). Input basic info (name, age, education, work experience, skills, target position, etc.) and get 1–3 complete, polished resume templates with content.

## Setup

1. Create an app at [讯飞控制台](https://console.xfyun.cn) with **简历生成** service enabled
2. Set environment variables:
   ```bash
   export XFYUN_APP_ID="your_app_id"
   export XFYUN_API_KEY="your_api_key"
   export XFYUN_API_SECRET="your_api_secret"
   ```

## Usage

### Generate resume from text

```bash
python3 scripts/resume.py "姓名：张三，年龄：28岁，教育经历：2018年本科毕业于合肥工业大学；工作经历：java开发工程师3年"
```

### Generate resume from file

```bash
python3 scripts/resume.py --file personal_info.txt
```

### Pipe input via stdin

```bash
echo "姓名：李四，学历：硕士，专业：计算机科学" | python3 scripts/resume.py
```

### Save result to file

```bash
python3 scripts/resume.py "..." --output resume.json
```

### Options

| Flag | Short | Description |
|------|-------|-------------|
| `text` | | Personal info text (positional argument) |
| `--file` | `-f` | Read input text from a file |
| `--output` | `-o` | Save result to a file |
| `--raw` | | Output full raw API JSON response |

### Input tips

Include as much relevant info as possible for better results:

- **姓名** (name)
- **年龄** (age)
- **教育经历** (education: school, degree, major, graduation year)
- **工作经历** (work experience: title, company, duration, responsibilities)
- **技能** (skills)
- **求职意向** (target position / industry)
- **项目经历** (project experience)
- **证书/奖项** (certifications / awards)

### Example

```bash
python3 scripts/resume.py "姓名：王明，年龄：25岁，教育经历：2023年硕士毕业于北京大学计算机科学专业，2020年本科毕业于武汉大学软件工程专业；工作经历：字节跳动后端开发实习6个月；技能：Python, Java, Go, MySQL, Redis, Docker；求职意向：后端开发工程师"
```

## Notes

- **Input**: plain text, max 4MB (base64 encoded)
- **Output**: JSON with 1–3 resume templates. The response `resData.text` is base64 encoded — the script decodes it automatically
- **Session timeout**: max 60 seconds per request
- **Auth**: HMAC-SHA256 signed URL (same pattern as other iFlytek APIs)
- **Endpoint**: `POST https://cn-huadong-1.xf-yun.com/v1/private/s73f4add9`
- **Env vars**: `XFYUN_APP_ID`, `XFYUN_API_KEY`, `XFYUN_API_SECRET`
- **No pip dependencies**: uses only Python stdlib (`urllib`, `hmac`, `hashlib`, `base64`, `json`, `argparse`)
