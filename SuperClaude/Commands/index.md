---
allowed-tools: [Read, Grep, Glob, Bash, Write]
description: "包括的なプロジェクトドキュメントとナレッジベースを生成します"
---

# /sc:index - プロジェクトドキュメンテーション

## Purpose
包括的なプロジェクトドキュメント、インデックス、ナレッジベースを作成および維持します。

## Usage
```
/sc:index [target] [--type docs|api|structure|readme] [--format md|json|yaml]
```

## Arguments
- `target` - ドキュメント化するプロジェクトディレクトリまたは特定のコンポーネント
- `--type` - ドキュメントの種類 (docs, api, structure, readme)
- `--format` - 出力形式 (md, json, yaml)
- `--update` - 既存のドキュメントを更新します

## Execution
1. Analyze project structure and identify key components
2. Extract documentation from code comments and README files
3. Generate comprehensive documentation based on type
4. Create navigation structure and cross-references
5. Output formatted documentation with proper organization

## Claude Code Integration
- Uses Glob for systematic file discovery
- Leverages Grep for extracting documentation patterns
- Applies Write for creating structured documentation
- Maintains consistency with project conventions