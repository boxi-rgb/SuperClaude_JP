---
allowed-tools: [Read, Grep, Glob, Bash]
description: "タスク、機能、またはプロジェクトの開発見積もりを提供します"
---

# /sc:estimate - 開発見積もり

## Purpose
複雑性分析に基づいて、タスク、機能、またはプロジェクトの正確な開発見積もりを生成します。

## Usage
```
/sc:estimate [target] [--type time|effort|complexity|cost] [--unit hours|days|weeks]
```

## Arguments
- `target` - 見積もり対象のタスク、機能、またはプロジェクト
- `--type` - 見積もりの種類 (time, effort, complexity, cost)
- `--unit` - 見積もりの時間単位 (hours, days, weeks)
- `--breakdown` - 見積もりの詳細な内訳を提供します

## Execution
1. Analyze scope and requirements of target
2. Identify complexity factors and dependencies
3. Apply estimation methodologies and historical data
4. Generate estimates with confidence intervals
5. Present detailed breakdown with risk factors

## Claude Code Integration
- Uses Read for requirement analysis
- Leverages Glob for codebase complexity assessment
- Applies Grep for pattern-based estimation
- Maintains structured estimation documentation