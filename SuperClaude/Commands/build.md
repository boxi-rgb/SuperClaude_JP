---
allowed-tools: [Read, Bash, Glob, TodoWrite, Edit]
description: "エラー処理と最適化を行いつつ、プロジェクトのビルド、コンパイル、パッケージ化を行います"
---

# /sc:build - プロジェクトのビルド

## Purpose
包括的なエラーハンドリングと最適化を行いながら、プロジェクトのビルド、コンパイル、パッケージ化を行います。

## Usage
```
/sc:build [target] [--type dev|prod|test] [--clean] [--optimize] [--verbose]
```

## Arguments
- `target` - ビルド対象のプロジェクトまたは特定のコンポーネント
- `--type` - ビルドタイプ (dev, prod, test)
- `--clean` - ビルド前にビルド成果物をクリーンアップします
- `--optimize` - ビルドの最適化を有効にします
- `--verbose` - 詳細なビルド出力を有効にします

## Execution
1. Analyze project structure and build configuration
2. Validate dependencies and environment setup
3. Execute build process with error monitoring
4. Handle build errors and provide diagnostic information
5. Optimize build output and report results

## Claude Code Integration
- Uses Bash for build command execution
- Leverages Read for build configuration analysis
- Applies TodoWrite for build progress tracking
- Maintains comprehensive error handling and reporting