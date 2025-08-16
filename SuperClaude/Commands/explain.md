---
allowed-tools: [Read, Grep, Glob, Bash]
description: "コード、概念、またはシステムの動作について明確な説明を提供します"
---

# /sc:explain - コードと概念の説明

## Purpose
コードの機能、概念、またはシステムの動作について、明確で包括的な説明を提供します。

## Usage
```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|diagram|examples]
```

## Arguments
- `target` - 説明対象のコードファイル、関数、概念、またはシステム
- `--level` - 説明の複雑さ (basic, intermediate, advanced)
- `--format` - 出力形式 (text, diagram, examples)
- `--context` - 説明のための追加コンテキスト

## Execution
1. Analyze target code or concept thoroughly
2. Identify key components and relationships
3. Structure explanation based on complexity level
4. Provide relevant examples and use cases
5. Present clear, accessible explanation with proper formatting

## Claude Code Integration
- Uses Read for comprehensive code analysis
- Leverages Grep for pattern identification
- Applies Bash for runtime behavior analysis
- Maintains clear, educational communication style