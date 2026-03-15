---
name: ship-learn-next
description: Transform learning content (like YouTube transcripts, articles, tutorials) into actionable implementation plans using the Ship-Learn-Next framework. Use when user wants to turn advice, lessons, or educational content into concrete action steps, reps, or a learning quest.
allowed-tools:
  - Read
  - Write
---

# Ship-Learn-Next Action Planner

This skill helps transform passive learning content into actionable **Ship-Learn-Next cycles** - turning advice and lessons into concrete, shippable iterations.

## When to Use This Skill

Activate when the user:
- Has a transcript/article/tutorial and wants to "implement the advice"
- Asks to "turn this into a plan" or "make this actionable"
- Wants to extract implementation steps from educational content
- Needs help breaking down big ideas into small, shippable reps
- Says things like "I watched/read X, now what should I do?"

## Core Framework: Ship-Learn-Next

Every learning quest follows three repeating phases:

1. **SHIP** - Create something real (code, content, product, demonstration)
2. **LEARN** - Honest reflection on what happened
3. **NEXT** - Plan the next iteration based on learnings

**Key principle**: 100 reps beats 100 hours of study. Learning = doing better, not knowing more.

## How This Skill Works

### Step 1: Read the Content

Read the file the user provides (transcript, article, notes). Use the Read tool to analyze the content.

### Step 2: Extract Core Lessons

Identify from the content:
- **Main advice/lessons**: What are the key takeaways?
- **Actionable principles**: What can actually be practiced?
- **Skills being taught**: What would someone learn by doing this?
- **Examples/case studies**: Real implementations mentioned

### Step 3: Define the Ship-Learn-Next Quest

Create a structured learning quest with 3-7 reps. Each rep should have:
- **SHIP**: Exact thing to create/do
- **LEARN**: Reflection questions
- **NEXT**: How to progress

### Step 4: Make It Immediately Startable

The quest must be actionable RIGHT NOW:
- Rep 1 should be completable in under 30 minutes
- No prerequisites except what is in the content
- Clear "done" criteria for each rep
- Progressive difficulty

## Output Format

Produce a markdown file saved to the workspace with:
1. Quest overview (the skill + why reps matter)
2. 3-7 specific reps with SHIP/LEARN/NEXT structure
3. A "Quick Start" section for Rep 1
