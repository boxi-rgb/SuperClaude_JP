---
allowed-tools: [Read, Grep, Glob, Edit, MultiEdit, TodoWrite]
description: "コードの品質、パフォーマンス、および保守性に対する体系的な改善を適用します"
---

# /sc:improve - コード改善

## Purpose
コードの品質、パフォーマンス、保守性、およびベストプラクティスに体系的な改善を適用します。

## Usage
```
/sc:improve [target] [--type quality|performance|maintainability|style] [--safe] [--preview]
```

## Arguments
- `target` - 改善対象のファイル、ディレクトリ、またはプロジェクト
- `--type` - 改善の種類 (quality, performance, maintainability, style)
- `--safe` - 安全でリスクの低い改善のみを適用します
- `--preview` - 改善を適用せずに表示します

## Execution
1. Analyze code for improvement opportunities
2. Identify specific improvement patterns and techniques
3. Create improvement plan with risk assessment
4. Apply improvements with appropriate validation
5. Verify improvements and report changes

## Claude Code Integration
- Uses Read for comprehensive code analysis
- Leverages MultiEdit for batch improvements
- Applies TodoWrite for improvement tracking
- Maintains safety and validation mechanisms