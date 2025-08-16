---
allowed-tools: [Read, Grep, Glob, Bash, Edit, MultiEdit]
description: "コードのクリーンアップ、不要なコードの削除、プロジェクト構造の最適化を行います"
---

# /sc:cleanup - コードとプロジェクトのクリーンアップ

## Purpose
体系的にコードをクリーンアップし、不要なコードを削除し、インポートを最適化し、プロジェクト構造を改善します。

## Usage
```
/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--dry-run]
```

## Arguments
- `target` - クリーンアップ対象のファイル、ディレクトリ、またはプロジェクト全体
- `--type` - クリーンアップの種類 (code, imports, files, all)
- `--safe` - 保守的なクリーンアップ（デフォルト）
- `--aggressive` - より徹底的なクリーンアップ（リスクが高い）
- `--dry-run` - 変更を適用せずにプレビューします

## Execution
1. Analyze target for cleanup opportunities
2. Identify dead code, unused imports, and redundant files
3. Create cleanup plan with risk assessment
4. Execute cleanup operations with appropriate safety measures
5. Validate changes and report cleanup results

## Claude Code Integration
- Uses Glob for systematic file discovery
- Leverages Grep for dead code detection
- Applies MultiEdit for batch cleanup operations
- Maintains backup and rollback capabilities