#!/bin/bash
# 每日备份脚本
# 执行时间: 每天 23:00

BACKUP_DIR="/tmp/openclaw_backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="openclaw_backup_${DATE}.tar.gz"

echo "=== 开始备份 ==="
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 创建临时目录
mkdir -p ${BACKUP_DIR}

# 1. 备份主要配置文件
echo "[1/4] 备份配置文件..."
mkdir -p ${BACKUP_DIR}/config
cp -r ~/.openclaw/config/* ${BACKUP_DIR}/config/ 2>/dev/null || true
cp ~/.openclaw/workspace/AGENTS.md ${BACKUP_DIR}/ 2>/dev/null || true
cp ~/.openclaw/workspace/SOUL.md ${BACKUP_DIR}/ 2>/dev/null || true
cp ~/.openclaw/workspace/TOOLS.md ${BACKUP_DIR}/ 2>/dev/null || true
cp ~/.openclaw/workspace/IDENTITY.md ${BACKUP_DIR}/ 2>/dev/null || true
cp ~/.openclaw/workspace/USER.md ${BACKUP_DIR}/ 2>/dev/null || true

# 2. 备份凭证目录
echo "[2/4] 备份凭证..."
mkdir -p ${BACKUP_DIR}/learnings
cp ~/.openclaw/workspace/.learnings/*.md ${BACKUP_DIR}/learnings/ 2>/dev/null || true

# 3. 备份工作区
echo "[3/4] 备份工作区..."
mkdir -p ${BACKUP_DIR}/memory
cp ~/.openclaw/workspace/memory/*.md ${BACKUP_DIR}/memory/ 2>/dev/null || true
cp ~/.openclaw/workspace/HEARTBEAT.md ${BACKUP_DIR}/ 2>/dev/null || true

# 4. 备份会话状态
echo "[4/4] 备份会话状态..."
cat > ${BACKUP_DIR}/backup_info.txt << EOF
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
备份内容:
- 主要配置文件
- 凭证目录
- 工作区文件
- 会话状态

文件清单:
EOF

find ${BACKUP_DIR} -type f >> ${BACKUP_DIR}/backup_info.txt

# 打包
echo "打包备份文件..."
cd /tmp
tar -czf ${BACKUP_NAME} openclaw_backup/

# 生成备份清单
cat > /tmp/backup_manifest.txt << EOF
=== OpenClaw 每日备份清单 ===
备份时间: $(date '+%Y-%m-%d %H:%M:%S')
备份文件: ${BACKUP_NAME}

【备份内容】
1. 主要配置文件
   - AGENTS.md
   - SOUL.md
   - TOOLS.md
   - IDENTITY.md
   - USER.md
   - ~/.openclaw/config/

2. 凭证目录
   - .learnings/*.md (含 InStreet API Key)

3. 工作区
   - memory/*.md
   - HEARTBEAT.md

4. 会话状态
   - 预测准确率
   - 因子权重配置
   - 学习进度

【文件位置】
备份包: /tmp/${BACKUP_NAME}
清单: /tmp/backup_manifest.txt

【恢复方法】
tar -xzf ${BACKUP_NAME} -C ~/.openclaw/workspace/
EOF

echo "=== 备份完成 ==="
echo "备份文件: /tmp/${BACKUP_NAME}"
echo "清单文件: /tmp/backup_manifest.txt"
ls -lh /tmp/${BACKUP_NAME}
