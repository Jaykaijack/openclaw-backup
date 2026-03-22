#!/usr/bin/env python3
"""
LanceDB 记忆存储模块 - 二郎量化分析系统
支持向量化的记忆存储和语义搜索
"""

import lancedb
import argparse
import json
from datetime import datetime
from pathlib import Path
import hashlib

# 数据库路径
DB_PATH = Path.home() / ".openclaw" / "workspace" / "data" / "lancedb"
DB_PATH.mkdir(parents=True, exist_ok=True)

# 表名
TABLE_NAME = "memories"

# 简单的文本向量化（使用哈希模拟，后续可替换为真实嵌入）
def simple_embedding(text: str, dim: int = 384) -> list:
    """简单的文本向量化（模拟）"""
    # 使用多个哈希函数生成向量
    vec = []
    for i in range(dim):
        h = hashlib.md5(f"{text}_{i}".encode()).hexdigest()
        vec.append(int(h[:8], 16) / 0xFFFFFFFF)
    return vec


class MemoryStore:
    def __init__(self):
        self.db = lancedb.connect(str(DB_PATH))
        self._init_table()
    
    def _init_table(self):
        """初始化表"""
        try:
            # 尝试打开表，如果不存在则创建
            self.db.open_table(TABLE_NAME)
        except Exception:
            # 表不存在，创建新表
            import pyarrow as pa
            schema = pa.schema([
                ("id", pa.string()),
                ("content", pa.string()),
                ("category", pa.string()),
                ("date", pa.string()),
                ("embedding", pa.list_(pa.float32(), 384)),
            ])
            self.db.create_table(TABLE_NAME, schema=schema)
            print(f"✅ 创建记忆表: {TABLE_NAME}")
    
    def add(self, content: str, category: str = "note"):
        """添加记忆"""
        table = self.db.open_table(TABLE_NAME)
        
        # 生成ID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        memory_id = f"{timestamp}_{content_hash}"
        
        # 生成嵌入
        embedding = simple_embedding(content)
        
        # 添加记录
        import pyarrow as pa
        data = [{
            "id": memory_id,
            "content": content,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "embedding": embedding,
        }]
        
        table.add(data)
        print(f"✅ 已存储记忆 [{category}]: {content[:50]}...")
        return memory_id
    
    def search(self, query: str, limit: int = 10):
        """语义搜索记忆"""
        table = self.db.open_table(TABLE_NAME)
        
        # 生成查询向量
        query_embedding = simple_embedding(query)
        
        # 向量搜索
        results = table.search(query_embedding).limit(limit).to_pandas()
        
        if len(results) == 0:
            print("❌ 未找到相关记忆")
            return []
        
        print(f"\n🔍 搜索结果 ({query}):")
        print("-" * 60)
        for _, row in results.iterrows():
            print(f"[{row['category']}] {row['date']}")
            print(f"  {row['content'][:100]}...")
            print(f"  相似度: {row.get('_distance', 'N/A')}")
            print()
        
        return results.to_dict('records')
    
    def list_all(self, category: str = None, limit: int = 50):
        """列出所有记忆"""
        table = self.db.open_table(TABLE_NAME)
        
        df = table.to_pandas()
        
        if len(df) == 0:
            print("📝 记忆库为空")
            return []
        
        if category:
            df = df[df['category'] == category]
        
        df = df.sort_values('date', ascending=False).head(limit)
        
        print(f"\n📝 记忆列表 (共{len(df)}条):")
        print("-" * 60)
        for _, row in df.iterrows():
            print(f"[{row['category']}] {row['date']} | {row['id']}")
            print(f"  {row['content'][:80]}...")
            print()
        
        return df.to_dict('records')
    
    def delete(self, memory_id: str):
        """删除记忆"""
        table = self.db.open_table(TABLE_NAME)
        table.delete(f"id = '{memory_id}'")
        print(f"✅ 已删除记忆: {memory_id}")
    
    def stats(self):
        """统计信息"""
        table = self.db.open_table(TABLE_NAME)
        df = table.to_pandas()
        
        print("\n📊 记忆库统计:")
        print("-" * 40)
        print(f"总记忆数: {len(df)}")
        
        if len(df) > 0:
            print("\n按类别:")
            for cat, count in df['category'].value_counts().items():
                print(f"  {cat}: {count}")
            
            print(f"\n日期范围: {df['date'].min()} ~ {df['date'].max()}")


def main():
    parser = argparse.ArgumentParser(description="二郎记忆存储模块")
    parser.add_argument("--init", action="store_true", help="初始化数据库")
    parser.add_argument("--add", type=str, help="添加记忆")
    parser.add_argument("--category", type=str, default="note", help="记忆类别")
    parser.add_argument("--search", type=str, help="搜索记忆")
    parser.add_argument("--list", action="store_true", help="列出所有记忆")
    parser.add_argument("--delete", type=str, help="删除记忆")
    parser.add_argument("--stats", action="store_true", help="统计信息")
    parser.add_argument("--limit", type=int, default=10, help="返回数量限制")
    
    args = parser.parse_args()
    
    store = MemoryStore()
    
    if args.init:
        print("✅ 数据库已初始化")
    elif args.add:
        store.add(args.add, args.category)
    elif args.search:
        store.search(args.search, args.limit)
    elif args.list:
        store.list_all(limit=args.limit)
    elif args.delete:
        store.delete(args.delete)
    elif args.stats:
        store.stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
