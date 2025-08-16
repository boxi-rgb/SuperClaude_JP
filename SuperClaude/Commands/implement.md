---
allowed-tools: [Read, Write, Edit, MultiEdit, Bash, Glob, TodoWrite, Task]
description: "インテリジェントなペルソナアクティベーションとMCP統合による機能とコードの実装"
---

# /sc:implement - 機能実装

## Purpose
インテリジェントなエキスパートのアクティベーションと包括的な開発サポートにより、機能、コンポーネント、およびコードの機能を実装します。

## Usage
```
/sc:implement [feature-description] [--type component|api|service|feature] [--framework react|vue|express|etc] [--safe] [--iterative] [--with-tests] [--documentation]
```

## Arguments
- `feature-description` - 実装する内容の説明
- `--type` - 実装タイプ (component, api, service, feature, module)
- `--framework` - ターゲットフレームワークまたはテクノロジースタック
- `--safe` - 保守的な実装アプローチを使用します
- `--iterative` - 検証ステップを含む反復開発を有効にします
- `--with-tests` - テスト実装を含めます
- `--documentation` - 実装と同時にドキュメントを生成します

## Execution
1. Analyze implementation requirements and detect technology context
2. Auto-activate relevant personas (frontend, backend, security, etc.)
3. Coordinate with MCP servers (Magic for UI, Context7 for patterns, Sequential for complex logic)
4. Generate implementation code with best practices
5. Apply security and quality validation
6. Provide testing recommendations and next steps

## Claude Code Integration
- Uses Write/Edit/MultiEdit for code generation and modification
- Leverages Read and Glob for codebase analysis and context understanding
- Applies TodoWrite for implementation progress tracking
- Integrates Task tool for complex multi-step implementations
- Coordinates with MCP servers for specialized functionality
- Auto-activates appropriate personas based on implementation type

## Auto-Activation Patterns
- **Frontend**: UI components, React/Vue/Angular development
- **Backend**: APIs, services, database integration
- **Security**: Authentication, authorization, data protection
- **Architecture**: System design, module structure
- **Performance**: Optimization, scalability considerations

## Examples
```
/sc:implement user authentication system --type feature --with-tests
/sc:implement dashboard component --type component --framework react
/sc:implement REST API for user management --type api --safe
/sc:implement payment processing service --type service --iterative
```