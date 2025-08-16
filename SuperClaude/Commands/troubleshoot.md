---
allowed-tools: [Read, Grep, Glob, Bash, TodoWrite]
description: "コード、ビルド、またはシステムの動作における問題を診断および解決します"
---

# /sc:troubleshoot - 問題の診断と解決

## Purpose
コード、ビルド、デプロイメント、またはシステムの動作における問題を体系的に診断し、解決します。

## Usage
```
/sc:troubleshoot [issue] [--type bug|build|performance|deployment] [--trace] [--fix]
```

## Arguments
- `issue` - 問題またはエラーメッセージの説明
- `--type` - 問題のカテゴリ (bug, build, performance, deployment)
- `--trace` - 詳細なトレースとロギングを有効にします
- `--fix` - 安全な場合に自動的に修正を適用します

## Execution
1. Analyze issue description and gather initial context
2. Identify potential root causes and investigation paths
3. Execute systematic debugging and diagnosis
4. Propose and validate solution approaches
5. Apply fixes and verify resolution

## Claude Code Integration
- Uses Read for error log analysis
- Leverages Bash for runtime diagnostics
- Applies Grep for pattern-based issue detection
- Maintains structured troubleshooting documentation