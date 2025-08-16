---
allowed-tools: [Read, Bash, Glob, TodoWrite, Edit, Write]
description: "テストの実行、テストレポートの生成、およびテストカバレッジの維持"
---

# /sc:test - テストと品質保証

## Purpose
テストを実行し、包括的なテストレポートを生成し、テストカバレッジの基準を維持します。

## Usage
```
/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]
```

## Arguments
- `target` - 特定のテスト、ファイル、またはテストスイート全体
- `--type` - テストの種類 (unit, integration, e2e, all)
- `--coverage` - カバレッジレポートを生成します
- `--watch` - ウォッチモードでテストを実行します
- `--fix` - 可能な場合に失敗したテストを自動的に修正します

## Execution
1. Discover and categorize available tests
2. Execute tests with appropriate configuration
3. Monitor test results and collect metrics
4. Generate comprehensive test reports
5. Provide recommendations for test improvements

## Claude Code Integration
- Uses Bash for test execution and monitoring
- Leverages Glob for test discovery
- Applies TodoWrite for test result tracking
- Maintains structured test reporting and coverage analysis