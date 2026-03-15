#!/bin/bash
# GitHub 备份脚本 - 带重试机制

BACKUP_DIR="$HOME/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
REPO_URL="https://github.com/Jaykaijack/openclaw-backup.git"

echo "🐺 二郎 GitHub 备份系统"
echo "📅 $DATE $TIME"

cd "$BACKUP_DIR"

# 检查远程仓库
echo "🔍 检查远程仓库配置..."
git remote -v

# 添加所有更改
echo "📦 添加更改..."
git add .

# 提交
echo "💾 提交更改..."
git commit -m "Daily backup: $DATE $TIME" || echo "没有新更改需要提交"

# 推送到 GitHub（带重试）
echo "🚀 推送到 GitHub..."
MAX_RETRIES=3
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if git push -u origin main; then
        echo "✅ GitHub 推送成功！"
        echo "📎 仓库地址: $REPO_URL"
        exit 0
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        echo "⚠️ 推送失败，重试 $RETRY_COUNT/$MAX_RETRIES..."
        sleep 5
    fi
done

echo "❌ GitHub 推送失败"
echo "💡 备用方案："
echo "   1. 手动下载备份文件: openclaw-backup-$DATE.tar.gz"
echo "   2. 或稍后重试: bash .learnings/github-backup.sh"
exit 1
