#!/usr/bin/env python3
"""
Token消耗分析脚本
分析当前会话的Token消耗情况，给出优化建议
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime

def get_file_size_kb(file_path):
    """获取文件大小（KB）"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / 1024
    return 0

def count_lines(file_path):
    """统计文件行数"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    return 0

def estimate_tokens(file_path):
    """估算文件Token数（粗略：1 Token ≈ 4 字符）"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(content) // 4
    return 0

def analyze_memory_files(workspace_path):
    """分析记忆文件"""
    memory_dir = os.path.join(workspace_path, "memory")
    results = []

    if os.path.exists(memory_dir):
        for file_path in glob.glob(os.path.join(memory_dir, "*.md")):
            file_name = os.path.basename(file_path)
            size_kb = get_file_size_kb(file_path)
            tokens = estimate_tokens(file_path)
            lines = count_lines(file_path)

            status = "✅ 正常"
            if size_kb > 100:
                status = "⚠️ 建议压缩"
            elif size_kb > 50:
                status = "🟡 可优化"

            results.append({
                "file": file_name,
                "size_kb": round(size_kb, 1),
                "tokens": tokens,
                "lines": lines,
                "status": status
            })

    return results

def analyze_skill_files(workspace_path):
    """分析技能文件"""
    skills_dir = os.path.join(workspace_path, "skills")
    results = []

    if os.path.exists(skills_dir):
        for skill_dir in glob.glob(os.path.join(skills_dir, "*")):
            if os.path.isdir(skill_dir):
                skill_name = os.path.basename(skill_dir)
                skill_md = os.path.join(skill_dir, "SKILL.md")
                if os.path.exists(skill_md):
                    size_kb = get_file_size_kb(skill_md)
                    tokens = estimate_tokens(skill_md)
                    results.append({
                        "skill": skill_name,
                        "size_kb": round(size_kb, 1),
                        "tokens": tokens
                    })

    return results

def generate_recommendations(memory_analysis, skill_analysis):
    """生成优化建议"""
    recommendations = []

    # 记忆文件建议
    large_memory = [m for m in memory_analysis if m["size_kb"] > 50]
    if large_memory:
        recommendations.append({
            "type": "memory",
            "priority": "high" if any(m["size_kb"] > 100 for m in large_memory) else "medium",
            "message": f"发现 {len(large_memory)} 个大记忆文件，建议使用 /compress 压缩",
            "files": [m["file"] for m in large_memory]
        })

    # 技能文件建议
    large_skills = [s for s in skill_analysis if s["tokens"] > 5000]
    if large_skills:
        recommendations.append({
            "type": "skill",
            "priority": "low",
            "message": f"发现 {len(large_skills)} 个大型技能文件，可能增加加载时间",
            "files": [s["skill"] for s in large_skills]
        })

    # 通用建议
    total_memory_tokens = sum(m["tokens"] for m in memory_analysis)
    if total_memory_tokens > 50000:
        recommendations.append({
            "type": "general",
            "priority": "high",
            "message": f"总记忆Token约 {total_memory_tokens//1000}K，每次对话都会加载，建议精简",
            "action": "考虑归档旧记忆到单独文件"
        })

    return recommendations

def main():
    workspace_path = os.path.expanduser("~/.openclaw/workspace")

    print("=" * 50)
    print("📊 Token消耗分析报告")
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # 分析记忆文件
    print("\n📁 记忆文件分析")
    print("-" * 50)
    memory_analysis = analyze_memory_files(workspace_path)

    if memory_analysis:
        print(f"{'文件名':<30} {'大小(KB)':<10} {'估算Token':<12} {'状态'}")
        print("-" * 70)
        for m in memory_analysis:
            print(f"{m['file']:<30} {m['size_kb']:<10} {m['tokens']:<12} {m['status']}")
    else:
        print("未找到记忆文件")

    # 分析技能文件
    print("\n🔧 技能文件分析")
    print("-" * 50)
    skill_analysis = analyze_skill_files(workspace_path)

    if skill_analysis:
        print(f"{'技能名':<30} {'大小(KB)':<10} {'估算Token'}")
        print("-" * 60)
        for s in skill_analysis[:10]:  # 只显示前10个
            print(f"{s['skill']:<30} {s['size_kb']:<10} {s['tokens']}")
        if len(skill_analysis) > 10:
            print(f"... 还有 {len(skill_analysis) - 10} 个技能")
    else:
        print("未找到技能文件")

    # 生成建议
    print("\n💡 优化建议")
    print("-" * 50)
    recommendations = generate_recommendations(memory_analysis, skill_analysis)

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            print(f"\n{i}. {priority_emoji.get(rec['priority'], '⚪')} {rec['message']}")
            if 'files' in rec:
                for f in rec['files'][:3]:
                    print(f"   - {f}")
    else:
        print("✅ 当前配置良好，无需优化")

    # 总结
    total_memory = sum(m["tokens"] for m in memory_analysis)
    print("\n" + "=" * 50)
    print(f"📈 总计: 记忆约 {total_memory//1000}K Token, {len(skill_analysis)} 个技能")
    print("=" * 50)

if __name__ == "__main__":
    main()
