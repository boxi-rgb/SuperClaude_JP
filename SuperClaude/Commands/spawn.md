---
allowed-tools: [Read, Grep, Glob, Bash, TodoWrite, Edit, MultiEdit, Write]
description: "複雑なタスクを連携したサブタスクに分割し、効率的に実行します"
---

# /sc:spawn - タスクオーケストレーション

## Purpose
複雑なリクエストを管理可能なサブタスクに分解し、その実行を調整します。

## Usage
```
/sc:spawn [task] [--sequential|--parallel] [--validate]
```

## Arguments
- `task` - オーケストレーションする複雑なタスクまたはプロジェクト
- `--sequential` - 依存関係の順序でタスクを実行します（デフォルト）
- `--parallel` - 独立したタスクを同時に実行します
- `--validate` - タスク間の品質チェックポイントを有効にします

## Execution
1. Parse request and create hierarchical task breakdown
2. Map dependencies between subtasks
3. Choose optimal execution strategy (sequential/parallel)
4. Execute subtasks with progress monitoring
5. Integrate results and validate completion

## Claude Code Integration
- Uses TodoWrite for task breakdown and tracking
- Leverages file operations for coordinated changes
- Applies efficient batching for related operations
- Maintains clear dependency management