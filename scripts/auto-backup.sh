#!/bin/bash
# 二郎自动备份脚本
# 用法: ./auto-backup.sh

set -e

WORKSPACE="$HOME/.openclaw/workspace"
BACKUP_DIR="$HOME/.openclaw/backups"
DATE=$(date +%Y-%m-%d-%H%M%S)

echo "🐺 二郎自动备份系统"
echo "===================="
echo "时间: $(date)"
echo ""

# 进入工作区
cd "$WORKSPACE"

# 1. Git 备份
echo "📤 推送到 GitHub..."
git add -A
git commit -m "Auto backup: $DATE" || echo "无变更需要提交"
git push origin main && echo "✅ GitHub 同步完成" || echo "⚠️ GitHub 推送失败"

echo ""

# 2. 本地 tar.gz 备份
echo "📦 创建本地备份..."
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/openclaw-backup-$DATE.tar.gz" \
    --exclude='.git' \
    --exclude='*.tar.gz' \
    -C "$HOME/.openclaw" \
    workspace/ && echo "✅ 本地备份完成: $BACKUP_DIR/openclaw-backup-$DATE.tar.gz"

echo ""

# 3. 清理旧备份（保留最近10个）
echo "🧹 清理旧备份..."
ls -t "$BACKUP_DIR"/openclaw-backup-*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm -f
echo "✅ 保留最近10个备份"

echo ""
echo "===================="
echo "✅ 备份完成!"
echo "GitHub: https://github.com/Jaykaijack/openclaw-backup"
echo "本地: $BACKUP_DIR"
