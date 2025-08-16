---
allowed-tools: [Read, Grep, Glob, Bash, Write]
description: "プロジェクトのコンテキスト、設定、および依存関係を読み込んで分析します"
---

# /sc:load - プロジェクトコンテキストの読み込み

## Purpose
プロジェクトのコンテキスト、設定、依存関係、および環境設定を読み込んで分析します。

## Usage
```
/sc:load [target] [--type project|config|deps|env] [--cache]
```

## Arguments
- `target` - 読み込むプロジェクトディレクトリまたは特定の設定
- `--type` - 読み込みの種類 (project, config, deps, env)
- `--cache` - 読み込んだコンテキストをキャッシュして、次回以降のアクセスを高速化します
- `--refresh` - キャッシュされたコンテキストを強制的に更新します

## Execution
1. Discover and analyze project structure and configuration files
2. Load dependencies, environment variables, and settings
3. Parse and validate configuration consistency
4. Create comprehensive project context map
5. Cache context for efficient future access

## Claude Code Integration
- Uses Glob for comprehensive project discovery
- Leverages Read for configuration analysis
- Applies Bash for environment validation
- Maintains efficient context caching mechanisms