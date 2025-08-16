---
allowed-tools: [Read, Grep, Glob, Write, Edit, TodoWrite]
description: "システムアーキテクチャ、API、およびコンポーネントインターフェイスを設計します"
---

# /sc:design - システムとコンポーネントの設計

## Purpose
システムアーキテクチャ、API、コンポーネントインターフェース、および技術仕様を設計します。

## Usage
```
/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
```

## Arguments
- `target` - 設計対象のシステム、コンポーネント、または機能
- `--type` - 設計タイプ (architecture, api, component, database)
- `--format` - 出力形式 (diagram, spec, code)
- `--iterative` - 反復的な設計の改良を有効にします

## Execution
1. Analyze requirements and design constraints
2. Create initial design concepts and alternatives
3. Develop detailed design specifications
4. Validate design against requirements and best practices
5. Generate design documentation and implementation guides

## Claude Code Integration
- Uses Read for requirement analysis
- Leverages Write for design documentation
- Applies TodoWrite for design task tracking
- Maintains consistency with architectural patterns