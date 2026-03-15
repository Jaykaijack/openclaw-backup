#!/bin/bash
# GitHub 备份脚本
# 每日23:00执行，将备份推送到 GitHub

GITHUB_USER="Jaykaijack"
GITHUB_PASS="Jay922158"
REPO_NAME="openclaw-backup"
DATE=$(date +%Y%m%d)
BACKUP_DIR="/tmp/github_backup_${DATE}"

echo "=== GitHub 备份开始 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 创建备份目录
mkdir -p ${BACKUP_DIR}

# 复制核心文件
echo "[1/3] 复制核心文件..."
cp -r ~/.openclaw/workspace/*.md ${BACKUP_DIR}/ 2>/dev/null || true
cp -r ~/.openclaw/workspace/memory ${BACKUP_DIR}/ 2>/dev/null || true
cp -r ~/.openclaw/workspace/.learnings ${BACKUP_DIR}/ 2>/dev/null || true

# 生成备份信息
cat > ${BACKUP_DIR}/BACKUP_INFO.txt << EOF
OpenClaw 每日备份
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
备份内容:
- 主要配置文件 (*.md)
- 记忆文件 (memory/)
- 学习日志 (.learnings/)

恢复方法:
1. 克隆仓库: git clone https://github.com/${GITHUB_USER}/${REPO_NAME}.git
2. 复制文件到 ~/.openclaw/workspace/
EOF

# 初始化 git 仓库
echo "[2/3] 初始化 Git 仓库..."
cd ${BACKUP_DIR}
git init
git config user.email "erlang@openclaw.ai"
git config user.name "二郎"

# 添加所有文件
git add .
git commit -m "Backup ${DATE} - $(date '+%H:%M:%S')"

# 推送到 GitHub (需要仓库已存在)
echo "[3/3] 推送到 GitHub..."
git remote add origin "https://${GITHUB_USER}:${GITHUB_PASS}@github.com/${GITHUB_USER}/${REPO_NAME}.git" 2>/dev/null || true

# 尝试推送
git push -u origin master --force 2>/dev/null || git push -u origin main --force 2>/dev/null || echo "推送失败，请检查仓库是否存在"

echo "=== GitHub 备份完成 ==="
echo "备份目录: ${BACKUP_DIR}"
echo "GitHub 仓库: https://github.com/${GITHUB_USER}/${REPO_NAME}"
