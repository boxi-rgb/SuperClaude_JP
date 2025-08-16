---
allowed-tools: [Read, Grep, Glob, Write, Edit]
description: "特定のコンポーネントや機能に特化したドキュメントを作成します"
---

# /sc:document - 集中ドキュメンテーション

## Purpose
特定のコンポーネント、関数、または機能に対して、正確で焦点の絞られたドキュメントを生成します。

## Usage
```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

## Arguments
- `target` - ドキュメント化する特定のファイル、関数、またはコンポーネント
- `--type` - ドキュメントの種類 (inline, external, api, guide)
- `--style` - ドキュメントのスタイル (brief, detailed)
- `--template` - 特定のドキュメンテーションテンプレートを使用します

## Execution
1. Analyze target component and extract key information
2. Identify documentation requirements and audience
3. Generate appropriate documentation based on type and style
4. Apply consistent formatting and structure
5. Integrate with existing documentation ecosystem

## Claude Code Integration
- Uses Read for deep component analysis
- Leverages Edit for inline documentation updates
- Applies Write for external documentation creation
- Maintains documentation standards and conventions