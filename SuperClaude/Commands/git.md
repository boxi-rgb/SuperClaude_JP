---
allowed-tools: [Bash, Read, Glob, TodoWrite, Edit]
description: "インテリジェントなコミットメッセージとブランチ管理を伴うGit操作"
---

# /sc:git - Git操作

## Purpose
インテリジェントなコミットメッセージ、ブランチ管理、ワークフローの最適化を伴うGit操作を実行します。

## Usage
```
/sc:git [operation] [args] [--smart-commit] [--branch-strategy]
```

## Arguments
- `operation` - Git操作 (add, commit, push, pull, merge, branch, status)
- `args` - 操作固有の引数
- `--smart-commit` - インテリジェントなコミットメッセージを生成します
- `--branch-strategy` - ブランチの命名規則を適用します
- `--interactive` - 複雑な操作のための対話モード

## Execution
1. Analyze current Git state and repository context
2. Execute requested Git operations with validation
3. Apply intelligent commit message generation
4. Handle merge conflicts and branch management
5. Provide clear feedback and next steps

## Claude Code Integration
- Uses Bash for Git command execution
- Leverages Read for repository analysis
- Applies TodoWrite for operation tracking
- Maintains Git best practices and conventions