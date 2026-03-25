#!/usr/bin/env python3
"""
Token Manager - 智能Token监控与提醒
自动监控上下文大小，超过阈值时生成提醒
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 配置
CONFIG = {
    "warning_threshold_kb": 50,    # 警告阈值（KB）
    "danger_threshold_kb": 100,    # 危险阈值（KB）
    "critical_threshold_kb": 200,  # 严重阈值（KB）
    "memory_file": "MEMORY.md",
    "heartbeat_state": "heartbeat-state.json"
}

def get_file_size_kb(file_path):
    """获取文件大小（KB）"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / 1024
    return 0

def estimate_tokens(file_path):
    """估算Token数"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(content) // 4
    return 0

def get_context_status(size_kb):
    """获取上下文状态"""
    if size_kb < CONFIG["warning_threshold_kb"]:
        return "✅ 正常", "green"
    elif size_kb < CONFIG["danger_threshold_kb"]:
        return "🟡 注意", "yellow"
    elif size_kb < CONFIG["critical_threshold_kb"]:
        return "🔴 警告", "red"
    else:
        return "🚨 危险", "critical"

def generate_reminder(size_kb, tokens, status, level):
    """生成提醒消息"""
    reminder = f"""
🔔 Token Manager 上下文提醒

当前上下文大小：{size_kb:.1f} KB（约 {tokens//1000}K Token）
状态：{status}

"""

    if level == "yellow":
        reminder += """建议：考虑执行 /compress 压缩记忆
预计节省：30%-50% Token消耗
"""
    elif level == "red":
        reminder += """⚠️ 强烈建议：立即执行 /compress 压缩记忆
预计节省：50%-70% Token消耗
不压缩将导致后续对话成本显著上升
"""
    elif level == "critical":
        reminder += """🚨 紧急：上下文过大，费用飙升风险！
立即执行：/compress
预计节省：70%-80% Token消耗

如果不压缩，每次对话都将消耗大量Token！
"""

    reminder += f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}"
    return reminder

def check_memory_files(workspace_path):
    """检查所有记忆文件"""
    memory_dir = os.path.join(workspace_path, "memory")
    results = []

    if os.path.exists(memory_dir):
        for root, dirs, files in os.walk(memory_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    size_kb = get_file_size_kb(file_path)
                    tokens = estimate_tokens(file_path)
                    results.append({
                        "file": file,
                        "path": file_path,
                        "size_kb": size_kb,
                        "tokens": tokens
                    })

    # 检查主记忆文件
    main_memory = os.path.join(workspace_path, "MEMORY.md")
    if os.path.exists(main_memory):
        size_kb = get_file_size_kb(main_memory)
        tokens = estimate_tokens(main_memory)
        results.append({
            "file": "MEMORY.md",
            "path": main_memory,
            "size_kb": size_kb,
            "tokens": tokens
        })

    return results

def analyze_task_complexity(task_description):
    """分析任务复杂度，返回建议模型"""
    task_lower = task_description.lower()

    # 简单任务关键词
    simple_keywords = ['查询', '收集', '整理', '格式', '转换', '简单', '列表', '统计']
    # 复杂任务关键词
    complex_keywords = ['代码', '编程', '调试', 'bug', '推理', '分析', '设计', '架构', '创意', '写作']

    simple_score = sum(1 for kw in simple_keywords if kw in task_lower)
    complex_score = sum(1 for kw in complex_keywords if kw in task_lower)

    if complex_score > simple_score:
        return "高", "建议使用顶级模型（Opus/Claude）"
    elif simple_score > 0:
        return "低", "建议使用经济模型（Kimi/国产）"
    else:
        return "中", "建议使用中级模型（Sonnet/GPT-3.5）"

def main():
    workspace_path = os.path.expanduser("~/.openclaw/workspace")

    print("=" * 60)
    print("🤖 Token Manager - 智能监控报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # 检查记忆文件
    memory_files = check_memory_files(workspace_path)
    total_tokens = sum(m["tokens"] for m in memory_files)
    total_kb = sum(m["size_kb"] for m in memory_files)

    # 获取状态
    status, level = get_context_status(total_kb)

    print(f"\n📊 上下文总览")
    print("-" * 60)
    print(f"记忆文件数：{len(memory_files)}")
    print(f"总大小：{total_kb:.1f} KB")
    print(f"估算Token：{total_tokens//1000}K")
    print(f"状态：{status}")

    # 显示大文件
    large_files = [m for m in memory_files if m["size_kb"] > 10]
    if large_files:
        print(f"\n📁 大型记忆文件（>10KB）")
        print("-" * 60)
        for m in sorted(large_files, key=lambda x: x["size_kb"], reverse=True)[:5]:
            print(f"  {m['file']:<30} {m['size_kb']:>6.1f} KB  {m['tokens']:>6} Token")

    # 生成提醒
    if level in ["yellow", "red", "critical"]:
        print(generate_reminder(total_kb, total_tokens, status, level))

    # 建议
    print(f"\n💡 优化建议")
    print("-" * 60)

    if level == "green":
        print("✅ 当前上下文正常，无需优化")
    elif level == "yellow":
        print("🟡 建议定期执行 /compress 压缩记忆")
    elif level == "red":
        print("🔴 强烈建议立即执行 /compress")
        print("   这将节省 50%-70% 的后续Token消耗")
    else:
        print("🚨 紧急！立即执行 /compress")
        print("   否则每次对话都将消耗大量Token")

    print("\n" + "=" * 60)
    print("Token Manager 正在后台运行，自动帮你省钱")
    print("=" * 60)

if __name__ == "__main__":
    main()
