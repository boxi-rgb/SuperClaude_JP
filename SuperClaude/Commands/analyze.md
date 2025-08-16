---
allowed-tools: [Read, Grep, Glob, Bash, TodoWrite]
description: "コードの品質、セキュリティ、パフォーマンス、アーキテクチャを分析します"
---

# /sc:analyze - コード分析

## Purpose
品質、セキュリティ、パフォーマンス、アーキテクチャの各領域にわたって包括的なコード分析を実行します。

## Usage
```
/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]
```

## Arguments
- `target` - 分析対象のファイル、ディレクトリ、またはプロジェクト
- `--focus` - 分析の焦点領域（品質、セキュリティ、パフォーマンス、アーキテクチャ）
- `--depth` - 分析の深さ（quick、deep）
- `--format` - 出力形式（text、json、report）

## Execution
1. Discover and categorize files for analysis
2. Apply appropriate analysis tools and techniques
3. Generate findings with severity ratings
4. Create actionable recommendations with priorities
5. Present comprehensive analysis report

## Claude Code Integration
- Uses Glob for systematic file discovery
- Leverages Grep for pattern-based analysis
- Applies Read for deep code inspection
- Maintains structured analysis reporting