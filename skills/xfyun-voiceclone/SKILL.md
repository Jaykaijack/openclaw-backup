---
name: xfyun-voiceclone
description: "iFlytek Voice Clone (声音复刻) — train a custom voice model from audio samples and synthesize speech with the cloned voice. Supports the full workflow: get training text → create task → upload audio → submit training → poll results → synthesize with cloned voice. Pure Python stdlib, no pip dependencies."
---

# xfyun-voiceclone

Clone a voice from audio samples and synthesize speech with it, using iFlytek's Voice Clone (声音复刻) API. Two-phase workflow: **train** a voice model, then **synthesize** speech with it.

## Setup

1. Create an app at [讯飞控制台](https://console.xfyun.cn) with **一句话声音复刻** service enabled
2. Set environment variables:
   ```bash
   export XFYUN_APP_ID="your_app_id"
   export XFYUN_API_KEY="your_api_key"
   export XFYUN_API_SECRET="your_api_secret"
   ```

## Workflow

### Phase 1: Train a Voice Model

#### Step 1 — Get training text

```bash
python3 scripts/voiceclone.py train get-text
```

This returns a list of text segments with `segId`. You need to record yourself reading one of these texts.

#### Step 2 — Create a training task

```bash
python3 scripts/voiceclone.py train create --name "MyVoice" --sex female --engine omni_v1
```

Returns `task_id`. Supported engines:
- `omni_v1` — Multi-style universal voice (recommended)

Gender: `male`/`female` (or `1`/`2`).

#### Step 3 — Upload audio

```bash
# Local file:
python3 scripts/voiceclone.py train upload --task-id 12345 --audio recording.wav --text-id 5001 --seg-id 1

# URL:
python3 scripts/voiceclone.py train upload --task-id 12345 --audio-url "https://example.com/voice.wav" --text-id 5001 --seg-id 1
```

Audio requirements:
- Format: WAV/MP3/M4A/PCM
- Duration: match the training text (typically 3-60 seconds)
- Quality: clear recording, minimal background noise

#### Step 4 — Submit for training

```bash
python3 scripts/voiceclone.py train submit --task-id 12345
```

#### Step 5 — Check status (poll until done)

```bash
python3 scripts/voiceclone.py train status --task-id 12345
```

When complete, returns the `res_id` (voice resource ID) needed for synthesis.

#### Quick one-shot training

```bash
python3 scripts/voiceclone.py train quick \
    --audio recording.wav \
    --name "MyVoice" \
    --sex female \
    --wait
```

This combines create → upload → submit → poll in one command. `--wait` polls every 30s until training completes and prints the `res_id`.

### Phase 2: Synthesize Speech

```bash
# Basic synthesis
python3 scripts/voiceclone.py synth "你好，这是我的声音克隆。" --res-id YOUR_RES_ID

# With output file
python3 scripts/voiceclone.py synth "Hello world" --res-id YOUR_RES_ID --output hello.mp3

# From file
python3 scripts/voiceclone.py synth --file article.txt --res-id YOUR_RES_ID -o article.mp3

# From stdin
echo "测试语音合成" | python3 scripts/voiceclone.py synth --res-id YOUR_RES_ID

# Adjust parameters
python3 scripts/voiceclone.py synth "快一点" --res-id YOUR_RES_ID --speed 70 --volume 80
```

## Train Subcommands

| Command | Description |
|---------|-------------|
| `train get-text` | Get training text segments |
| `train create` | Create a training task |
| `train upload` | Upload audio to a task |
| `train submit` | Submit task for training |
| `train status` | Check training status |
| `train quick` | One-shot: create + upload + submit |

## Synthesis Options

| Flag | Default | Description |
|------|---------|-------------|
| `--res-id` | (required) | Voice resource ID from training |
| `--output` / `-o` | `output.mp3` | Output audio file path |
| `--format` | `mp3` | Audio format: mp3, pcm, speex, opus |
| `--sample-rate` | `16000` | Sample rate: 8000, 16000, 24000 |
| `--speed` | `50` | Speed 0–100 (50=normal) |
| `--volume` | `50` | Volume 0–100 (50=normal) |
| `--pitch` | `50` | Pitch 0–100 (50=normal) |

## Notes

- **Training API**: HTTP REST at `http://opentrain.xfyousheng.com/voice_train` (MD5-based token auth)
- **Synthesis API**: WebSocket at `wss://cn-huabei-1.xf-yun.com/v1/private/voice_clone` (HMAC-SHA256 URL auth)
- **vcn**: always `x6_clone` for cloned voice synthesis
- **Engine `omni_v1`**: multi-style universal voice, supports cn/en/jp/ko/ru
- **Training text**: use `get-text` to find available text segments — you must record yourself reading the corresponding text
- **Training time**: typically 2–10 minutes depending on load
- **No pip dependencies**: uses pure Python stdlib (built-in WebSocket client)
- **Env vars**: `XFYUN_APP_ID`, `XFYUN_API_KEY`, `XFYUN_API_SECRET`
- **Output**: prints absolute path of saved audio to stdout
- **API doc**: https://www.xfyun.cn/doc/spark/voiceclone.html
