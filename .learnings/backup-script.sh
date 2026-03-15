#!/bin/bash
# 二郎每日备份脚本

BACKUP_DIR="$HOME/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
BACKUP_NAME="openclaw-backup-${DATE}"

echo "🐺 二郎备份系统启动..."
echo "📅 日期: $DATE $TIME"

# 创建临时备份目录
mkdir -p /tmp/${BACKUP_NAME}

# 备份核心配置文件
echo "📦 备份配置文件..."
cp -r "$BACKUP_DIR/.learnings" /tmp/${BACKUP_NAME}/
cp "$BACKUP_DIR/AGENTS.md" /tmp/${BACKUP_NAME}/ 2>/dev/null || true
cp "$BACKUP_DIR/SOUL.md" /tmp/${BACKUP_NAME}/ 2>/dev/null || true
cp "$BACKUP_DIR/TOOLS.md" /tmp/${BACKUP_NAME}/ 2>/dev/null || true
cp "$BACKUP_DIR/IDENTITY.md" /tmp/${BACKUP_NAME}/ 2>/dev/null || true
cp "$BACKUP_DIR/USER.md" /tmp/${BACKUP_NAME}/ 2>/dev/null || true
cp "$BACKUP_DIR/HEARTBEAT.md" /tmp/${BACKUP_NAME}/ 2>/dev/null || true

# 备份记忆文件
if [ -d "$BACKUP_DIR/memory" ]; then
    echo "🧠 备份记忆文件..."
    cp -r "$BACKUP_DIR/memory" /tmp/${BACKUP_NAME}/
fi

# 创建备份清单
echo "📝 生成备份清单..."
cat > /tmp/${BACKUP_NAME}/BACKUP-MANIFEST.md << EOF
# 备份清单 - ${DATE} ${TIME}

## 备份内容

### 配置文件
- AGENTS.md - 工作区配置
- SOUL.md - 身份配置
- TOOLS.md - 工具配置
- IDENTITY.md - 身份信息
- USER.md - 用户信息
- HEARTBEAT.md - 心跳任务清单

### 学习记录
- .learnings/ - 学习日志和框架文档
  - quant-framework-v2.md - 量化分析框架V2.0
  - instreet-config.md - InStreet配置
  - ERRORS.md - 错误记录
  - FEATURE_REQUESTS.md - 功能请求
  - LEARNINGS.md - 学习笔记

### 记忆文件
- memory/ - 每日记忆文件

## 备份信息
- 备份时间: ${DATE} ${TIME}
- 备份版本: V2.0
- 备份者: 二郎
EOF

# 打包
echo "🗜️ 打包备份文件..."
cd /tmp
tar -czf ${BACKUP_NAME}.tar.gz ${BACKUP_NAME}

# 移动回工作区
mv ${BACKUP_NAME}.tar.gz "$BACKUP_DIR/"

# 清理临时文件
rm -rf /tmp/${BACKUP_NAME}

echo "✅ 备份完成: ${BACKUP_NAME}.tar.gz"
echo "📊 文件大小: $(du -h $BACKUP_DIR/${BACKUP_NAME}.tar.gz | cut -f1)"

# Git 提交（如果配置了远程仓库）
if git remote -v > /dev/null 2>&1; then
    echo "🚀 推送到 GitHub..."
    cd "$BACKUP_DIR"
    git add .
    git commit -m "Daily backup: ${DATE} ${TIME}"
    git push origin main
    echo "✅ GitHub 推送完成"
else
    echo "⚠️ 未配置远程仓库，跳过 GitHub 推送"
    echo "💡 请运行以下命令配置："
    echo "   git remote add origin https://github.com/Jaykaijack/openclaw-backup.git"
fi

echo "🎉 备份流程结束"
