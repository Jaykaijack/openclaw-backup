#!/usr/bin/env python3
"""
hot-finder search.py v4
真正可执行的多源热门内容搜索
数据源：
  - HackerNews Algolia API（科技/AI 热门）
  - Reddit JSON API（海外各圈子）
  - Bilibili API（B站视频）
  - 今日头条搜索（国内热点）
  - 微博搜索（国内热点）
  - YouTube/TikTok via Bing（视频）
"""
import urllib.request, urllib.parse, json, sys, time, re, os, argparse
from datetime import datetime, timedelta

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def fetch_json(url, headers=None, timeout=15):
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers: h.update(headers)
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return json.loads(raw.decode("utf-8", errors="ignore"))
    except Exception as e:
        print(f"    ⚠️  {url[:60]}... error: {e}", file=sys.stderr)
        return None

def fetch_html(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"    ⚠️  fetch error: {e}", file=sys.stderr)
        return ""

def clean(text):
    text = re.sub(r'<[^>]+>', '', str(text))
    return re.sub(r'\s+', ' ', text.replace("&amp;","&").replace("&#39;","'").replace("&quot;",'"')).strip()

# ─── 数据源函数 ────────────────────────────────────────────────────────────────

def search_hackernews(keyword, top=10, days=30):
    """HN Algolia API - 科技/AI 热门"""
    since = int((datetime.now() - timedelta(days=days)).timestamp())
    url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(keyword)}&tags=story&hitsPerPage=50&numericFilters=created_at_i%3E{since}"
    data = fetch_json(url)
    if not data: return []
    results = []
    for h in sorted(data.get("hits",[]), key=lambda x: -x.get("points",0))[:top]:
        title = h.get("title","").strip()
        if not title: continue
        url_val = h.get("url","") or f"https://news.ycombinator.com/item?id={h.get('objectID','')}"
        results.append({
            "platform": "HackerNews",
            "icon": "🟠",
            "title": title,
            "description": "",
            "link": url_val,
            "hn_link": f"https://news.ycombinator.com/item?id={h.get('objectID','')}",
            "score": h.get("points", 0),
            "comments": h.get("num_comments", 0),
            "author": h.get("author",""),
            "keyword": keyword,
            "content_type": "tech_post",
        })
    return results

def search_reddit(keyword, subreddit="all", top=10, time_filter="week"):
    """Reddit JSON API - 海外各圈热门"""
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={urllib.parse.quote(keyword)}&sort=top&t={time_filter}&limit={top*2}&restrict_sr=false"
    data = fetch_json(url, headers={"User-Agent": "hot-finder/1.0"})
    if not data: return []
    results = []
    for p in data.get("data",{}).get("children",[])[:top]:
        d = p.get("data",{})
        title = d.get("title","").strip()
        if not title: continue
        link = d.get("url","")
        # 内容类型判断
        ctype = "video" if any(x in link for x in ["youtube","youtu.be","tiktok","v.redd.it"]) else \
                "news" if any(x in link for x in ["cnn","bbc","reuters","nytimes","techcrunch"]) else "post"
        results.append({
            "platform": f"Reddit r/{d.get('subreddit','all')}",
            "icon": "🔴",
            "title": title,
            "description": d.get("selftext","")[:200].strip(),
            "link": link,
            "hn_link": f"https://reddit.com{d.get('permalink','')}",
            "score": d.get("score",0),
            "comments": d.get("num_comments",0),
            "author": f"u/{d.get('author','')}",
            "keyword": keyword,
            "content_type": ctype,
        })
    return results

def search_bilibili(keyword, top=10):
    """B站搜索 API"""
    url = f"https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={urllib.parse.quote(keyword)}&order=click&page=1"
    data = fetch_json(url, headers={"Referer": "https://www.bilibili.com/"})
    if not data: return []
    results = []
    for item in (data.get("data",{}).get("result",[]) or [])[:top]:
        title = clean(item.get("title",""))
        if len(title) < 3: continue
        plays = item.get("play", 0)
        plays_str = f"{plays//10000}万" if plays >= 10000 else str(plays)
        results.append({
            "platform": "哔哩哔哩",
            "icon": "🔵",
            "title": title,
            "description": clean(item.get("description",""))[:200],
            "link": item.get("arcurl",""),
            "hn_link": "",
            "score": plays,
            "comments": item.get("review",0),
            "author": item.get("author",""),
            "keyword": keyword,
            "content_type": "video",
            "plays": plays_str,
        })
    return results

def search_bing_video(keyword, top=10, region="CN"):
    """必应视频搜索（国内外均可）"""
    domain_filter = ""
    lang = "zh-CN" if region == "CN" else "en-US"
    url = f"https://cn.bing.com/videos/search?q={urllib.parse.quote(keyword)}&qft=+filterui:videoage-lt43200&mkt={lang}"
    html = fetch_html(url)
    if not html: return []
    matches = re.findall(
        r'"title"\s*:\s*"([^"]{5,100})"[^}]*?"viewCount"\s*:\s*"([^"]*)"[^}]*?"(?:publisherName|publisher)"\s*:\s*"([^"]*)"[^}]*?"(?:hostPageUrl|contentUrl)"\s*:\s*"([^"]+)"',
        html
    )
    results = []
    seen = set()
    for m in matches[:top*2]:
        title, views, publisher, link = [x.strip() for x in m]
        if len(title) < 5 or title in seen: continue
        seen.add(title)
        results.append({
            "platform": "必应视频",
            "icon": "🔷",
            "title": title,
            "description": "",
            "link": link,
            "hn_link": "",
            "score": 0,
            "comments": 0,
            "author": publisher,
            "keyword": keyword,
            "content_type": "video",
            "plays": views,
        })
        if len(results) >= top: break
    return results

def search_youtube_via_bing(keyword, top=10):
    """YouTube 热门视频（通过 Bing site: 过滤）"""
    url = f"https://www.bing.com/search?q=site:youtube.com+{urllib.parse.quote(keyword)}&cc=US&setlang=en"
    html = fetch_html(url)
    if not html: return []
    pattern = r'<h2[^>]*>\s*<a[^>]+href="(https://www\.youtube\.com/watch\?[^"]+)"[^>]*>([^<]{5,100})</a>'
    matches = re.findall(pattern, html)
    results = []
    seen = set()
    for link, title in matches[:top*2]:
        title = clean(title)
        if len(title) < 5 or title in seen: continue
        seen.add(title)
        results.append({
            "platform": "YouTube",
            "icon": "▶️",
            "title": title,
            "description": "",
            "link": link,
            "hn_link": "",
            "score": 0,
            "comments": 0,
            "author": "",
            "keyword": keyword,
            "content_type": "video",
        })
        if len(results) >= top: break
    return results

def search_tiktok_via_ddg(keyword, top=10):
    """TikTok 热门（通过 DuckDuckGo site: 过滤）"""
    url = f"https://duckduckgo.com/html/?q=site:tiktok.com+{urllib.parse.quote(keyword)}"
    html = fetch_html(url)
    if not html: return []
    pattern = r'class="result__a"[^>]+href="([^"]*tiktok\.com[^"]*)"[^>]*>([^<]{5,100})</a>'
    matches = re.findall(pattern, html)
    results = []
    seen = set()
    for link, title in matches[:top*2]:
        title = clean(title)
        if len(title) < 5 or title in seen: continue
        seen.add(title)
        results.append({
            "platform": "TikTok",
            "icon": "🎵",
            "title": title,
            "description": "",
            "link": link,
            "hn_link": "",
            "score": 0,
            "comments": 0,
            "author": "",
            "keyword": keyword,
            "content_type": "video",
        })
        if len(results) >= top: break
    return results

def search_weibo(keyword, top=10):
    """微博热搜视频"""
    url = f"https://s.weibo.com/video?q={urllib.parse.quote(keyword)}&Refer=SWeibo_box"
    html = fetch_html(url)
    if not html: return []
    titles = re.findall(r'<p[^>]*class="[^"]*txt[^"]*"[^>]*>([\s\S]{5,200}?)</p>', html)
    links = re.findall(r'href="(https://video\.weibo\.com/[^"]+)"', html)
    results = []
    seen = set()
    for i, title in enumerate(titles[:top*2]):
        title = clean(title)
        if len(title) < 5 or title in seen: continue
        seen.add(title)
        link = links[i] if i < len(links) else f"https://s.weibo.com/video?q={urllib.parse.quote(keyword)}"
        results.append({
            "platform": "微博",
            "icon": "🟡",
            "title": title,
            "description": "",
            "link": link,
            "hn_link": "",
            "score": 0,
            "comments": 0,
            "author": "",
            "keyword": keyword,
            "content_type": "video",
        })
        if len(results) >= top: break
    return results

def search_xiaohongshu_via_bing(keyword, top=10):
    """小红书（通过 Bing site: 过滤）"""
    url = f"https://cn.bing.com/search?q=site:xiaohongshu.com+{urllib.parse.quote(keyword)}"
    html = fetch_html(url)
    if not html: return []
    pattern = r'<h2[^>]*>\s*<a[^>]+href="(https://www\.xiaohongshu\.com[^"]*)"[^>]*>([^<]{5,100})</a>'
    matches = re.findall(pattern, html)
    results = []
    seen = set()
    for link, title in matches[:top*2]:
        title = clean(title)
        if len(title) < 5 or title in seen: continue
        seen.add(title)
        results.append({
            "platform": "小红书",
            "icon": "🔴",
            "title": title,
            "description": "",
            "link": link,
            "hn_link": "",
            "score": 0,
            "comments": 0,
            "author": "",
            "keyword": keyword,
            "content_type": "post",
        })
        if len(results) >= top: break
    return results

# ─── 主函数 ───────────────────────────────────────────────────────────────────

SOURCES = {
    "hackernews":    ("🟠", "HackerNews",  search_hackernews),
    "reddit":        ("🔴", "Reddit",       lambda kw, top: search_reddit(kw, "all", top)),
    "reddit_ai":     ("🔴", "Reddit/AI",    lambda kw, top: search_reddit(kw, "artificial", top)),
    "bilibili":      ("🔵", "哔哩哔哩",     search_bilibili),
    "youtube":       ("▶️", "YouTube",     search_youtube_via_bing),
    "tiktok":        ("🎵", "TikTok",       search_tiktok_via_ddg),
    "bing_video":    ("🔷", "必应视频",     lambda kw, top: search_bing_video(kw, top, "CN")),
    "weibo":         ("🟡", "微博",         search_weibo),
    "xiaohongshu":   ("🔴", "小红书",       search_xiaohongshu_via_bing),
}

DEFAULT_SOURCES = "hackernews,reddit,bilibili,youtube,bing_video"

def main():
    parser = argparse.ArgumentParser(description="爆款猎手 v4 — 多源热门内容搜索")
    parser.add_argument("keyword", help="搜索关键词")
    parser.add_argument("--sources", default=DEFAULT_SOURCES, help=f"数据源（逗号分隔）: {', '.join(SOURCES.keys())}")
    parser.add_argument("--top", type=int, default=10, help="每个来源返回条数")
    parser.add_argument("--days", type=int, default=30, help="HN/Reddit 时间范围（天）")
    parser.add_argument("--output", default="-", help="输出文件路径（-=stdout）")
    parser.add_argument("--format", default="json", choices=["json","text","csv"])
    args = parser.parse_args()

    sources = [s.strip() for s in args.sources.split(",") if s.strip() in SOURCES]
    if not sources:
        print(f"❌ 无效数据源，可选：{', '.join(SOURCES.keys())}", file=sys.stderr)
        sys.exit(1)

    all_results = []
    for src in sources:
        icon, name, fn = SOURCES[src]
        print(f"🔍 {icon} 搜索 {name}...", file=sys.stderr, flush=True)
        try:
            if src in ("hackernews",):
                results = fn(args.keyword, args.top, args.days)
            else:
                results = fn(args.keyword, args.top)
            print(f"   → {len(results)} 条", file=sys.stderr, flush=True)
            all_results.extend(results)
        except Exception as e:
            print(f"   ❌ 失败: {e}", file=sys.stderr)
        time.sleep(0.5)

    # 按 score 降序排列
    all_results.sort(key=lambda x: -x.get("score", 0))

    if args.format == "json":
        out = json.dumps(all_results, ensure_ascii=False, indent=2)
    elif args.format == "csv":
        import csv, io
        buf = io.StringIO()
        fields = ["platform","icon","title","description","link","score","comments","author","plays","keyword","content_type"]
        w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader(); w.writerows(all_results)
        out = buf.getvalue()
    else:
        lines = []
        for r in all_results:
            score = f"⬆️{r['score']}" if r.get("score") else ""
            plays = f"▶{r['plays']}" if r.get("plays") else ""
            cmts = f"💬{r['comments']}" if r.get("comments") else ""
            author = f"@{r['author']}" if r.get("author") else ""
            meta = " | ".join(x for x in [score, plays, cmts, author] if x)
            lines.append(f"{r['icon']} [{r['platform']}] {r['title']}")
            if meta: lines.append(f"   {meta}")
            if r.get("link"): lines.append(f"   🔗 {r['link']}")
        out = "\n".join(lines) if lines else "（未获取到结果）"

    if args.output == "-":
        print(out)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"✅ 保存完成: {args.output} ({len(all_results)} 条)", file=sys.stderr)

if __name__ == "__main__":
    main()
