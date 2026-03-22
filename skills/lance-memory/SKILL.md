# LanceDB 记忆存储模块

## 功能
- 向量化存储二郎的记忆、学习日志、市场分析
- 语义搜索，快速检索相关记忆
- 持久化存储，支持长期记忆

## 使用方法

```python
# 初始化记忆存储
python3 ~/.openclaw/workspace/skills/lance-memory/memory_store.py --init

# 存储记忆
python3 ~/.openclaw/workspace/skills/lance-memory/memory_store.py --add "市场情绪修复，电力板块强势"

# 搜索记忆
python3 ~/.openclaw/workspace/skills/lance-memory/memory_store.py --search "电力板块"

# 查看所有记忆
python3 ~/.openclaw/workspace/skills/lance-memory/memory_store.py --list
```

## 数据结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识 |
| content | string | 记忆内容 |
| category | string | 分类（market/learning/trade/note） |
| date | string | 日期 |
| embedding | vector(384) | 向量嵌入 |

## 依赖
- lancedb >= 0.30.0
- sentence-transformers（可选，用于本地嵌入）
