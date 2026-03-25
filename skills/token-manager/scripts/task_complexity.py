#!/usr/bin/env python3
"""
任务复杂度判断器
根据任务描述自动判断复杂度，推荐合适的模型
"""

import sys
import json

# 模型配置
MODELS = {
    "economic": {
        "name": "经济模型（Kimi/国产）",
        "examples": ["kimi", "qwen", "glm", "deepseek"],
        "cost": "💰",
        "suitable": "简单任务、信息收集、格式转换"
    },
    "mid": {
        "name": "中级模型（Sonnet/GPT-3.5）",
        "examples": ["sonnet", "gpt-3.5", "claude-3-sonnet"],
        "cost": "💰💰",
        "suitable": "文档整理、数据分析、报告生成"
    },
    "premium": {
        "name": "顶级模型（Opus/Claude）",
        "examples": ["opus", "claude-3-opus", "gpt-4"],
        "cost": "💰💰💰",
        "suitable": "代码编写、复杂推理、创意写作"
    }
}

# 任务分类规则
TASK_RULES = {
    "simple": {
        "keywords": [
            "查询", "收集", "整理", "格式", "转换", "简单", "列表",
            "统计", "汇总", "提取", "复制", "移动", "重命名",
            "查看", "显示", "告诉我", "什么是", "解释一下"
        ],
        "patterns": [
            "帮我查", "收集一下", "整理成", "转换成",
            "简单", "快速", "列出来", "统计"
        ],
        "level": "economic"
    },
    "medium": {
        "keywords": [
            "分析", "比较", "评估", "优化", "改进", "设计",
            "报告", "总结", "归纳", "提炼", "整合"
        ],
        "patterns": [
            "帮我分析", "比较一下", "写个报告", "做个总结",
            "优化", "改进", "设计方案"
        ],
        "level": "mid"
    },
    "complex": {
        "keywords": [
            "代码", "编程", "调试", "bug", "开发", "实现",
            "架构", "系统", "算法", "推理", "创意", "写作",
            "战略", "决策", "复杂", "深度"
        ],
        "patterns": [
            "写代码", "帮我写个程序", "调试", "修复bug",
            "设计架构", "复杂", "深度分析", "创意"
        ],
        "level": "premium"
    }
}

def analyze_task(task_description):
    """分析任务复杂度"""
    task_lower = task_description.lower()

    scores = {"simple": 0, "medium": 0, "complex": 0}

    # 关键词匹配
    for level, rules in TASK_RULES.items():
        for keyword in rules["keywords"]:
            if keyword in task_lower:
                scores[level] += 1

        for pattern in rules["patterns"]:
            if pattern in task_lower:
                scores[level] += 2

    # 判断最高分
    max_level = max(scores, key=scores.get)

    # 如果都是0，默认中等
    if scores[max_level] == 0:
        max_level = "medium"

    return max_level, scores

def get_model_recommendation(level):
    """获取模型推荐"""
    model_key = TASK_RULES[level]["level"]
    return MODELS[model_key]

def format_output(task, level, scores, model):
    """格式化输出"""
    output = f"""
╔══════════════════════════════════════════════════════════╗
║              Token Manager - 任务分析结果                 ║
╠══════════════════════════════════════════════════════════╣
║ 任务描述：{task[:40]}{'...' if len(task) > 40 else ''}
╠══════════════════════════════════════════════════════════╣
║ 复杂度评分：                                              ║
║   简单：{'█' * scores['simple']}{' ' * (10 - scores['simple'])} {scores['simple']} 分  ║
║   中等：{'█' * scores['medium']}{' ' * (10 - scores['medium'])} {scores['medium']} 分  ║
║   复杂：{'█' * scores['complex']}{' ' * (10 - scores['complex'])} {scores['complex']} 分  ║
╠══════════════════════════════════════════════════════════╣
║ 判定结果：{level.upper():^10}                              ║
╠══════════════════════════════════════════════════════════╣
║ 推荐模型：{model['name']:<20}              ║
║ 成本等级：{model['cost']:<20}              ║
║ 适用场景：{model['suitable'][:30]:<20}    ║
╚══════════════════════════════════════════════════════════╝
"""
    return output

def main():
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
    else:
        print("请输入任务描述：")
        task = input().strip()

    if not task:
        print("错误：任务描述不能为空")
        return

    # 分析任务
    level, scores = analyze_task(task)
    model = get_model_recommendation(level)

    # 输出结果
    print(format_output(task, level, scores, model))

    # JSON输出（供程序调用）
    result = {
        "task": task,
        "complexity": level,
        "scores": scores,
        "recommended_model": model["name"],
        "cost_level": model["cost"]
    }

    # 保存到文件
    output_file = "/tmp/task_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n详细结果已保存到：{output_file}")

if __name__ == "__main__":
    main()
