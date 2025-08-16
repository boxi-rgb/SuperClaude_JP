---
allowed-tools: [Read, Glob, Grep, TodoWrite, Task, mcp__sequential-thinking__sequentialthinking]
description: "インテリジェントなワークフロー管理とセッションをまたいだ永続性により、複雑なタスクを実行します"
wave-enabled: true
complexity-threshold: 0.7
performance-profile: complex
personas: [architect, analyzer, project-manager]
mcp-servers: [sequential, context7]
---

# /sc:task - 拡張タスク管理

## Purpose
インテリジェントなワークフロー管理、セッションをまたいだ永続性、階層的なタスク編成、および高度なオーケストレーション機能により、複雑なタスクを実行します。

## Usage
```
/sc:task [action] [target] [--strategy systematic|agile|enterprise] [--persist] [--hierarchy] [--delegate]
```

## Actions
- `create` - 新しいプロジェクトレベルのタスク階層を作成します
- `execute` - インテリジェントなオーケストレーションでタスクを実行します
- `status` - セッションをまたいでタスクのステータスを表示します
- `analytics` - タスクのパフォーマンスと分析ダッシュボード
- `optimize` - タスク実行戦略を最適化します
- `delegate` - 複数のエージェントにタスクを委任します
- `validate` - 証拠を用いてタスクの完了を検証します

## Arguments
- `target` - タスクの説明、プロジェクトの範囲、または既存のタスクID
- `--strategy` - 実行戦略 (systematic, agile, enterprise)
- `--persist` - セッションをまたいだタスクの永続性を有効にします
- `--hierarchy` - 階層的なタスクの内訳を作成します
- `--delegate` - マルチエージェントのタスク委任を有効にします
- `--wave-mode` - ウェーブベースの実行を有効にします
- `--validate` - 品質ゲートと検証を強制します
- `--mcp-routing` - インテリジェントなMCPサーバーのルーティングを有効にします

## Execution Modes

### Systematic Strategy
1. **Discovery Phase**: Comprehensive project analysis and scope definition
2. **Planning Phase**: Hierarchical task breakdown with dependency mapping
3. **Execution Phase**: Sequential execution with validation gates
4. **Validation Phase**: Evidence collection and quality assurance
5. **Optimization Phase**: Performance analysis and improvement recommendations

### Agile Strategy
1. **Sprint Planning**: Priority-based task organization
2. **Iterative Execution**: Short cycles with continuous feedback
3. **Adaptive Planning**: Dynamic task adjustment based on outcomes
4. **Continuous Integration**: Real-time validation and testing
5. **Retrospective Analysis**: Learning and process improvement

### Enterprise Strategy
1. **Stakeholder Analysis**: Multi-domain impact assessment
2. **Resource Allocation**: Optimal resource distribution across tasks
3. **Risk Management**: Comprehensive risk assessment and mitigation
4. **Compliance Validation**: Regulatory and policy compliance checks
5. **Governance Reporting**: Detailed progress and compliance reporting

## Advanced Features

### Task Hierarchy Management
- **Epic Level**: Large-scale project objectives (weeks to months)
- **Story Level**: Feature-specific implementations (days to weeks)
- **Task Level**: Specific actionable items (hours to days)
- **Subtask Level**: Granular implementation steps (minutes to hours)

### Intelligent Task Orchestration
- **Dependency Resolution**: Automatic dependency detection and sequencing
- **Parallel Execution**: Independent task parallelization
- **Resource Optimization**: Intelligent resource allocation and scheduling
- **Context Sharing**: Cross-task context and knowledge sharing

### Cross-Session Persistence
- **Task State Management**: Persistent task states across sessions
- **Context Continuity**: Preserved context and progress tracking
- **Historical Analytics**: Task execution history and learning
- **Recovery Mechanisms**: Automatic recovery from interruptions

### Quality Gates and Validation
- **Evidence Collection**: Systematic evidence gathering during execution
- **Validation Criteria**: Customizable completion criteria
- **Quality Metrics**: Comprehensive quality assessment
- **Compliance Checks**: Automated compliance validation

## Integration Points

### Wave System Integration
- **Wave Coordination**: Multi-wave task execution strategies
- **Context Accumulation**: Progressive context building across waves
- **Performance Monitoring**: Real-time performance tracking and optimization
- **Error Recovery**: Graceful error handling and recovery mechanisms

### MCP Server Coordination
- **Context7**: Framework patterns and library documentation
- **Sequential**: Complex analysis and multi-step reasoning
- **Magic**: UI component generation and design systems
- **Playwright**: End-to-end testing and performance validation

### Persona Integration
- **Architect**: System design and architectural decisions
- **Analyzer**: Code analysis and quality assessment
- **Project Manager**: Resource allocation and progress tracking
- **Domain Experts**: Specialized expertise for specific task types

## Performance Optimization

### Execution Efficiency
- **Batch Operations**: Grouped execution for related tasks
- **Parallel Processing**: Independent task parallelization
- **Context Caching**: Reusable context and analysis results
- **Resource Pooling**: Shared resource utilization

### Intelligence Features
- **Predictive Planning**: AI-driven task estimation and planning
- **Adaptive Execution**: Dynamic strategy adjustment based on progress
- **Learning Systems**: Continuous improvement from execution patterns
- **Optimization Recommendations**: Data-driven improvement suggestions

## Usage Examples

### Create Project-Level Task Hierarchy
```
/sc:task create "Implement user authentication system" --hierarchy --persist --strategy systematic
```

### Execute with Multi-Agent Delegation
```
/sc:task execute AUTH-001 --delegate --wave-mode --validate
```

### Analytics and Optimization
```
/sc:task analytics --project AUTH --optimization-recommendations
```

### Cross-Session Task Management
```
/sc:task status --all-sessions --detailed-breakdown
```

## Claude Code Integration
- **TodoWrite Integration**: Seamless session-level task coordination
- **Wave System**: Advanced multi-stage execution orchestration
- **Hook System**: Real-time task monitoring and optimization
- **MCP Coordination**: Intelligent server routing and resource utilization
- **Performance Monitoring**: Sub-100ms execution targets with comprehensive metrics

## Success Criteria
- **Task Completion Rate**: >95% successful task completion
- **Performance Targets**: <100ms hook execution, <5s task creation
- **Quality Metrics**: >90% validation success rate
- **Cross-Session Continuity**: 100% task state preservation
- **Intelligence Effectiveness**: >80% accurate predictive planning