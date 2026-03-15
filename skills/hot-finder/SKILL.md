---
name: hot-finder
description: "热点雷达 — 多源热门内容搜索 + Excel 数据导出。覆盖国内外视频、帖子、热点新闻。数据源：HackerNews、Reddit、哔哩哔哩、YouTube、TikTok、必应视频、微博、小红书。触发词：热点雷达、热门视频搜索、找爆款、搜索热门、trending、viral、热点新闻搜索、导出热门数据。"
---

# 热点雷达 (Hot Finder) v2

多源热门内容搜索 + Excel 数据导出。覆盖国内外视频、帖子、热点新闻，**无需 API Key**，全部可实际执行。

## 数据源（已验证可用）

| Key | 平台 | 内容类型 | 可靠性 |
|-----|------|---------|-------|
| `hackernews` | 🟠 HackerNews | 科技热帖/视频/新闻 | ✅ 稳定（Algolia API） |
| `reddit` | 🔴 Reddit | 海外各圈热帖/视频 | ✅ 稳定（JSON API） |
| `reddit_ai` | 🔴 Reddit/r/artificial | AI 专区热帖 | ✅ 稳定 |
| `bilibili` | 🔵 哔哩哔哩 | 中文热门视频 | ✅ 稳定（官方 API） |
| `youtube` | ▶️ YouTube | 英文热门视频 | ⚠️ Bing 代理 |
| `tiktok` | 🎵 TikTok | 英文短视频 | ⚠️ DDG 代理 |
| `bing_video` | 🔷 必应视频 | 综合视频 | ⚠️ 有时反爬 |
| `weibo` | 🟡 微博 | 中文热点视频 | ⚠️ 有时反爬 |
| `xiaohongshu` | 🔴 小红书 | 中文图文/视频 | ⚠️ Bing 代理 |

---

## 工作流程

### Step 1 — 理解需求

从用户请求提取：
- **关键词**（支持多个，如「AI 大模型」「DeepSeek」）
- **数据源**（默认：hackernews,reddit,bilibili,youtube,bing_video）
- **地区偏好**：
  - 国内为主 → 加 `bilibili,weibo,xiaohongshu`
  - 海外为主 → 加 `hackernews,reddit,reddit_ai,youtube,tiktok`
  - 全球综合 → 默认全部
- **内容类型**：视频/帖子/新闻（search.py 会自动分类）
- **每源条数**（默认 10）
- **是否导出 Excel**（默认是）

---

### Step 2 — 执行搜索

```bash
python3 ~/.openclaw/skills/hot-finder/scripts/search.py \
  "<关键词>" \
  --sources "hackernews,reddit,bilibili,youtube,bing_video" \
  --top 10 \
  --days 30 \
  --output /tmp/viral_results.json \
  --format json
```

**参数说明：**
- `--sources`：逗号分隔，可选值见上表
- `--top`：每个数据源返回条数
- `--days`：HN/Reddit 时间范围（天），默认30
- `--format`：json（导出用）/ text（预览用）

**多关键词示例：**
```bash
# 分别搜索再合并
for KW in "AI大模型" "DeepSeek"; do
  python3 ~/.openclaw/skills/hot-finder/scripts/search.py "$KW" \
    --sources "hackernews,bilibili" --top 8 \
    --output "/tmp/viral_${KW}.json" --format json 2>&1
done

# Python 合并
python3 -c "
import json, glob, sys
all=[]
for f in glob.glob('/tmp/viral_*.json'):
    try: all.extend(json.load(open(f)))
    except: pass
# 去重（按标题）
seen=set()
dedup=[r for r in all if not (r['title'] in seen or seen.add(r['title']))]
json.dump(dedup, open('/tmp/viral_results.json','w'), ensure_ascii=False, indent=2)
print(f'合并去重: {len(dedup)} 条', file=sys.stderr)
"
```

---

### Step 3 — 导出 Excel

```bash
python3 ~/.openclaw/skills/hot-finder/scripts/export_excel.py \
  --input /tmp/viral_results.json \
  --output /Users/eric/.openclaw/workspace/viral_<keyword>_<YYYYMMDD>.xlsx \
  --keyword "<关键词>"
```

**Excel 4个 Sheet：**
- **爆款内容**：主表（序号/平台/类型/标题/简介/评分/评论/作者/链接）
- **来源统计**：按平台 + 内容类型分类统计
- **热度排行**：按 score 降序排列的 Top 30
- **搜索信息**：关键词/时间/总条数

---

### Step 4 — 展示摘要

搜索完成后先展示文字摘要（高分前5 + 各平台代表作），再发送 Excel：

**格式：**
```
🎯 「<关键词>」热点雷达结果
📊 <N>个来源 | <M>条内容 | 视频<x>条 / 帖子<y>条 / 新闻<z>条

🏆 热度 Top5：
1. 🟠 [HN 1481⬆] Andrej Karpathy: Software in the era of AI
   🔗 https://youtube.com/...

...

📎 完整 Excel 数据发送中（<M>条，4个Sheet）
```

### Step 5 — 发送 Excel

```python
# 先把文件复制到 workspace（必须）
import shutil
shutil.copy("/tmp/...xlsx", "/Users/eric/.openclaw/workspace/viral_xxx.xlsx")

message(
  action="send",
  filePath="/Users/eric/.openclaw/workspace/viral_<keyword>_<YYYYMMDD>.xlsx",
  caption="📊 「<关键词>」热点雷达 | <N>来源 | <M>条 | 视频+帖子+新闻"
)
```

---

## 快速测试

```bash
# 文本预览（快速）
python3 ~/.openclaw/skills/hot-finder/scripts/search.py "AI" \
  --sources "hackernews,bilibili" --top 5 --format text

# 完整流程（含 Excel）
python3 ~/.openclaw/skills/hot-finder/scripts/search.py "AI大模型" \
  --sources "hackernews,reddit,bilibili" --top 10 \
  --output /tmp/test.json --format json
python3 ~/.openclaw/skills/hot-finder/scripts/export_excel.py \
  --input /tmp/test.json \
  --output /tmp/test.xlsx \
  --keyword "AI大模型"
```
