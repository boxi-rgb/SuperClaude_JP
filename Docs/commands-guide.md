# SuperClaude コマンドガイド 🛠️

## 💡 考えすぎないで - SuperClaudeが助けてくれます

**これら17個のコマンドについての真実**: これらを覚える必要はありません。まずは `/sc:analyze` や `/sc:implement` から始めて、何が起こるか見てみましょう！

**通常の動作はこうです:**
- Claude Codeで `/` をタイプ → 利用可能なコマンドが表示されます
- `/sc:analyze`, `/sc:build`, `/sc:improve` のような基本的なものを使います
- **SuperClaudeは、各状況に応じて役立つツールや専門家を選ぼうとします**
- 慣れてくると、より多くのコマンドが役立つようになります

**自動アクティベーションはかなり便利です** 🪄 - SuperClaudeは、あなたがやろうとしていることを検出し、関連する専門家（セキュリティ専門家、パフォーマンスオプティマイザなど）をあなたが管理することなくアクティブ化しようと試みます。通常はうまく機能します！ 😊

---

## クイック "まずこれを試して" リスト 🚀

**ここから始めてください**（読む必要はありません）:
```bash
/sc:index                    # 利用可能なものを確認
/sc:analyze src/            # コードを賢く分析しようとします
/sc:workflow feature-100-prd.md  # PRDからステップバイステップの実装ワークフローを作成
/sc:implement user-auth     # 機能やコンポーネントを作成（v2の/buildを置き換え）
/sc:build                   # インテリジェントなプロジェクトビルドを試みます
/sc:improve messy-file.js   # コードをクリーンアップしようとします
/sc:troubleshoot "error"    # 問題解決を手伝おうとします
```

**正直なところ、これで始めるには十分です。** 以下のすべては、他にどんなツールが利用できるか気になったときのためにあります。🛠️

---

SuperClaudeの全17スラッシュコマンドに関する実用的なガイドです。何がうまく機能し、何がまだ荒削りなのか、正直にお伝えします。

## クイックリファレンス 📋

*（これを覚える必要は本当にありません - 役立ちそうなものを選ぶだけです）*

| コマンド | 目的 | 自動アクティベート | 最適な用途 |
|---|---|---|---|
| `/sc:analyze` | スマートなコード分析 | セキュリティ/パフォーマンス専門家 | 問題発見、コードベース理解 |
| `/sc:build` | インテリジェントなビルド | フロントエンド/バックエンド専門家 | コンパイル、バンドル、デプロイ準備 |
| `/sc:implement` | 機能実装 | ドメイン固有の専門家 | 機能、コンポーネント、API、サービスの作成 |
| `/sc:improve` | 自動コードクリーンアップ | 品質専門家 | リファクタリング、最適化、品質修正 |
| `/sc:troubleshoot` | 問題調査 | デバッグ専門家 | デバッグ、問題調査 |
| `/sc:test` | スマートなテスト | QA専門家 | テスト実行、カバレッジ分析 |
| `/sc:document` | 自動ドキュメンテーション | ライティング専門家 | READMEファイル、コードコメント、ガイド |
| `/sc:git` | 強化されたgitワークフロー | DevOps専門家 | スマートコミット、ブランチ管理 |
| `/sc:design` | システム設計支援 | アーキテクチャ専門家 | アーキテクチャ計画、API設計 |
| `/sc:explain` | 学習アシスタント | 教育専門家 | コンセプト学習、コード理解 |
| `/sc:cleanup` | 技術的負債の削減 | リファクタリング専門家 | 不要コードの削除、ファイル整理 |
| `/sc:load` | コンテキスト理解 | 分析専門家 | プロジェクト分析、コードベース理解 |
| `/sc:estimate` | スマートな見積もり | 計画専門家 | 時間/工数計画、複雑性分析 |
| `/sc:spawn` | 複雑なワークフロー | オーケストレーションシステム | マルチステップ操作、ワークフロー自動化 |
| `/sc:task` | プロジェクト管理 | 計画システム | 長期的な機能計画、タスク追跡 |
| `/sc:workflow` | 実装計画 | ワークフローシステム | PRDからステップバイステップのワークフローを作成 |
| `/sc:index` | コマンドナビゲーション | ヘルプシステム | タスクに適したコマンドを見つける |

**プロのヒント**: 役立ちそうなものを試してみてください。SuperClaudeは通常、各状況に応じて役立つ専門家やツールをアクティブにしようとします！ 🎯

## 開発コマンド 🔨

### `/workflow` - 実装ワークフロー生成 🗺️
**何をするか**: PRDや機能要件を分析し、包括的なステップバイステップの実装ワークフローを作成します。

**役立つ点**: あなたのPRDを受け取り、専門家のガイダンス、依存関係マッピング、タスクオーケストレーションを備えた構造化された実装計画に分解します！ 🎯

**いつ使うか**:
- PRDや仕様書から新機能を開始する時
- 明確な実装ロードマップが必要な時
- 実装戦略に関する専門家のガイダンスが欲しい時
- 複数の依存関係を持つ複雑な機能を計画する時

**魔法**: あなたの機能要件に基づいて、適切な専門家ペルソナ（アーキテクト、セキュリティ、フロントエンド、バックエンド）とMCPサーバー（パターン用のContext7、複雑な分析用のSequential）を自動でアクティブ化します。

**例**:
```bash
/sc:workflow docs/feature-100-prd.md --strategy systematic --c7 --sequential
/sc:workflow "user authentication system" --persona security --output detailed
/sc:workflow payment-api --strategy mvp --risks --dependencies
```

**得られるもの**:
- **ロードマップ形式**: タイムライン付きのフェーズベースの実装計画
- **タスク形式**: 整理されたエピック、ストーリー、実行可能なタスク
- **詳細形式**: 時間見積もり付きのステップバイステップ指示
- **リスク評価**: 潜在的な問題と緩和戦略
- **依存関係マッピング**: 内部および外部の依存関係
- **専門家のガイダンス**: ドメイン固有のベストプラクティスとパターン

### `/implement` - 機能実装
**何をするか**: インテリジェントな専門家のアクティベーションにより、機能、コンポーネント、および機能性を実装します。

**役立つ点**: SuperClaudeは、あなたが実装しているものに基づいて、適切な専門家（フロントエンド、バックエンド、セキュリティ）とツールを自動でアクティブ化します！ 🎯

**いつ使うか**:
- 新しい機能やコンポーネントを作成する時（v2の`/build`機能を置き換え）
- API、サービス、またはモジュールを実装する時
- 最新のフレームワークでUIコンポーネントを構築する時
- ビジネスロジックと統合を開発する時

**基本的な構文**:
```bash
/sc:implement user authentication system      # 完全な機能を実装
/sc:implement --type component LoginForm      # 特定のコンポーネントを作成
/sc:implement --type api user-management      # APIエンドポイントを構築
/sc:implement --framework react dashboard     # フレームワーク固有の実装
```

**便利なフラグ**:
- `--type component|api|service|feature|module` - 実装タイプ
- `--framework react|vue|express|django|etc` - ターゲットフレームワーク
- `--safe` - 保守的な実装アプローチ
- `--iterative` - 検証を伴うステップバイステップの開発
- `--with-tests` - テスト実装を含む
- `--documentation` - コードと同時にドキュメントを生成

**実際の例**:
```bash
/sc:implement user authentication --type feature --with-tests
/sc:implement dashboard component --type component --framework react
/sc:implement REST API for orders --type api --safe
/sc:implement payment processing --type service --iterative
/sc:implement search functionality --framework vue --documentation
```

**自動アクティベーションパターン**:
- **フロントエンド**: UIコンポーネント, React/Vue/Angular → フロントエンドペルソナ + Magic MCP
- **バックエンド**: API, サービス, データベース → バックエンドペルソナ + Context7
- **セキュリティ**: 認証, 支払い, 機密データ → セキュリティペルソナ + 検証
- **複雑な機能**: マルチステップ実装 → Sequential MCP + アーキテクトペルソナ

**注意点**:
- より良い結果を得るには`--type`を指定してください（component vs service vs feature）
- 特定の技術スタックで作業する場合は`--framework`を使用してください
- 本番コードには`--safe`を、複雑な機能には`--iterative`を試してください
- 覚えておいてください: これはv2の`/build`を実際のコード実装のために置き換えるものです

---

### `/build` - プロジェクトのビルド
**何をするか**: スマートなエラーハンドリングでプロジェクトをビルド、コンパイル、パッケージ化します。

**簡単な方法**: `/sc:build`と入力するだけで、SuperClaudeはあなたのビルドシステムを理解しようとします！ 🎯

**いつ使うか**:
- プロジェクトをコンパイル/バンドルする必要がある時（`/sc:build`を試してみてください）
- ビルドプロセスが失敗していて、デバッグの手助けが欲しい時
- ビルド最適化を設定する時（必要なものを検出しようとします）
- デプロイ準備をする時

**基本的な構文**:
```bash
/sc:build                          # 現在のプロジェクトをビルド
/sc:build --type prod              # 本番ビルド
/sc:build --clean                  # クリーンビルド（古い成果物を削除）
/sc:build --optimize               # 最適化を有効化
/sc:build src/                     # 特定のディレクトリをビルド
```

**便利なフラグ**:
- `--type dev|prod|test` - ビルドタイプ
- `--clean` - ビルド前にクリーン
- `--optimize` - ビルド最適化を有効化
- `--verbose` - 詳細なビルド出力を表示

**実際の例**:
```bash
/sc:build --type prod --optimize   # 最適化付きの本番ビルド
/sc:build --clean --verbose        # 詳細な出力付きのクリーンビルド
/sc:build src/components           # componentsフォルダのみをビルド
```

**注意点**:
- 一般的なビルドツール（npm, webpackなど）で最も効果的に機能します
- 非常にカスタムなビルド設定では苦労するかもしれません
- ビルドツールがPATHにあることを確認してください

---

### `/design` - システム＆コンポーネント設計
**何をするか**: システムアーキテクチャ、API設計、コンポーネント仕様を作成します。

**いつ使うか**:
- 新機能やシステムの計画時
- APIやデータベースの設計が必要な時
- コンポーネントアーキテクチャの作成時
- システム関係の文書化時

**基本的な構文**:
```bash
/sc:design user-auth-system        # ユーザー認証システムを設計
/sc:design --type api auth         # API部分のみを設計
/sc:design --format spec payment   # 正式な仕様書を作成
```

**便利なフラグ**:
- `--type architecture|api|component|database` - 設計の焦点
- `--format diagram|spec|code` - 出力形式
- `--iterative` - イテレーションを通じて設計を洗練

**実際の例**:
```bash
/sc:design --type api user-management    # ユーザー管理APIを設計
/sc:design --format spec chat-system     # チャットシステムの仕様書を作成
/sc:design --type database ecommerce     # eコマースのデータベーススキーマを設計
```

**注意点**:
- コード生成よりも概念的です
- 出力の品質は、要件をどれだけ明確に記述するかに依存します
- 計画段階には最適ですが、実装の詳細にはあまり向きません

## 分析コマンド 🔍

### `/analyze` - コード分析
**何をするか**: コードの品質、セキュリティ、パフォーマンス、アーキテクチャを包括的に分析します。

**役立つ点**: SuperClaudeは、どのような分析が必要かを検出し、通常は関連する専門家を選び出します！ 🔍

**いつ使うか**:
- 見慣れないコードベースを理解する時（どのフォルダを指しても大丈夫です）
- セキュリティ脆弱性を見つける時（通常、セキュリティ専門家が介入します）
- パフォーマンスのボトルネックを探す時（通常、パフォーマンス専門家が助けてくれます）
- コード品質を評価する時（品質専門家がしばしば担当します）

**基本的な構文**:
```bash
/sc:analyze src/                   # srcディレクトリ全体を分析
/sc:analyze --focus security       # セキュリティ問題に焦点を当てる
/sc:analyze --depth deep app.js    # 特定のファイルを深く分析
```

**便利なフラグ**:
- `--focus quality|security|performance|architecture` - 分析の焦点
- `--depth quick|deep` - 分析の徹底度
- `--format text|json|report` - 出力形式

**実際の例**:
```bash
/sc:analyze --focus security --depth deep     # 詳細なセキュリティ分析
/sc:analyze --focus performance src/api/      # APIのパフォーマンス分析
/sc:analyze --format report .                 # 分析レポートを生成
```

**注意点**:
- 大規模なコードベースでは時間がかかることがあります
- セキュリティ分析はかなり良いですが、パフォーマンス分析はまちまちです
- 一般的な言語（JS, Pythonなど）で最も効果的に機能します

---

### `/troubleshoot` - 問題調査
**何をするか**: 体系的なデバッグと問題調査。

**いつ使うか**:
- 何かが壊れていて理由がわからない時
- 体系的なデバッグアプローチが必要な時
- エラーメッセージが紛らわしい時
- パフォーマンス問題の調査時

**基本的な構文**:
```bash
/sc:troubleshoot "login not working"     # ログイン問題を調査
/sc:troubleshoot --logs error.log        # エラーログを分析
/sc:troubleshoot performance             # パフォーマンスのトラブルシューティング
```

**便利なフラグ**:
- `--logs <file>` - ログファイルの分析を含める
- `--systematic` - 構造化されたデバッグアプローチを使用
- `--focus network|database|frontend` - 焦点領域

**実際の例**:
```bash
/sc:troubleshoot "API returning 500" --logs server.log
/sc:troubleshoot --focus database "slow queries"
/sc:troubleshoot "build failing" --systematic
```

**注意点**:
- 具体的なエラー記述でより効果的に機能します
- 可能な場合は関連するエラーメッセージとログを含めてください
- 最初は明白なことを提案するかもしれませんが（それは通常良いことです！）

---

### `/explain` - 教育的な説明
**何をするか**: コード、概念、技術を教育的な方法で説明します。

**いつ使うか**:
- 新しい技術やパターンを学ぶ時
- 複雑なコードを理解する時
- チームメンバーに明確な説明が必要な時
- 難しい概念を文書化する時

**基本的な構文**:
```bash
/sc:explain async/await               # async/awaitの概念を説明
/sc:explain --code src/utils.js       # 特定のコードファイルを説明
/sc:explain --beginner React hooks    # 初心者向けの説明
```

**便利なフラグ**:
- `--beginner` - より簡単な説明
- `--advanced` - 技術的な深さ
- `--code <file>` - 特定のコードを説明
- `--examples` - 実用的な例を含む

**実際の例**:
```bash
/sc:explain --beginner "what is REST API"
/sc:explain --code src/auth.js --advanced
/sc:explain --examples "React context patterns"
```

**注意点**:
- よく知られた概念には最適ですが、非常にニッチなトピックでは苦労するかもしれません
- 「このコードベースを説明して」という曖昧な質問より、具体的な質問の方が良いです
- あなたの経験レベルに関するコンテキストを含めてください

## 品質コマンド ✨

### `/improve` - コード強化
**何をするか**: コードの品質、パフォーマンス、保守性を体系的に改善します。

**いつ使うか**:
- 散らかったコードのリファクタリング
- パフォーマンス最適化
- ベストプラクティスの適用
- 古いコードの近代化

**基本的な構文**:
```bash
/sc:improve src/legacy/            # レガシーコードを改善
/sc:improve --type performance     # パフォーマンスに焦点を当てる
/sc:improve --safe src/utils.js    # 安全で低リスクの改善のみ
```

**便利なフラグ**:
- `--type quality|performance|maintainability|style` - 改善の焦点
- `--safe` - 低リスクの変更のみを適用
- `--preview` - 実行せずに何が変更されるかを表示

**実際の例**:
```bash
/sc:improve --type performance --safe src/api/
/sc:improve --preview src/components/LegacyComponent.js
/sc:improve --type style . --safe
```

**注意点**:
- 常に`--preview`を最初に使用して、何を変更したいかを確認してください
- `--safe`はあなたの友達です - 危険なリファクタリングを防ぎます
- コードベース全体よりも、小さなファイル/モジュールで最も効果的に機能します

---

### `/cleanup` - 技術的負債の削減
**何をするか**: 不要なコード、未使用のインポートを削除し、ファイル構造を整理します。

**いつ使うか**:
- コードベースが散らかっていると感じる時
- 未使用のインポート/変数がたくさんある時
- ファイルの整理がめちゃくちゃな時
- 大規模なリファクタリングの前

**基本的な構文**:
```bash
/sc:cleanup src/                   # srcディレクトリをクリーンアップ
/sc:cleanup --dead-code            # 不要コードの削除に焦点を当てる
/sc:cleanup --imports package.js   # 特定のファイルのインポートをクリーンアップ
```

**便利なフラグ**:
- `--dead-code` - 未使用のコードを削除
- `--imports` - インポート文をクリーンアップ
- `--files` - ファイル構造を再編成
- `--safe` - 保守的なクリーンアップのみ

**実際の例**:
```bash
/sc:cleanup --dead-code --safe src/utils/
/sc:cleanup --imports src/components/
/sc:cleanup --files . --safe
```

**注意点**:
- 攻撃的になることがあるので、変更は常に注意深くレビューしてください
- すべての不要コードをキャッチできるわけではありません（特に動的インポート）
- プロジェクト全体よりも、小さなセクションで実行する方が良いです

---

### `/test` - テスト＆品質保証
**何をするか**: テストを実行し、カバレッジレポートを生成し、テストの品質を維持します。

**いつ使うか**:
- テストスイートの実行
- テストカバレッジの確認
- テストレポートの生成
- 継続的なテストの設定

**基本的な構文**:
```bash
/sc:test                           # すべてのテストを実行
/sc:test --type unit               # ユニットテストのみを実行
/sc:test --coverage                # カバレッジレポートを生成
/sc:test --watch src/              # 開発用のウォッチモード
```

**便利なフラグ**:
- `--type unit|integration|e2e|all` - テストタイプ
- `--coverage` - カバレッジレポートを生成
- `--watch` - ウォッチモードでテストを実行
- `--fix` - 失敗したテストを自動的に修正しようと試みる

**実際の例**:
```bash
/sc:test --type unit --coverage
/sc:test --watch src/components/
/sc:test --type e2e --fix
```

**注意点**:
- テストフレームワークが適切に設定されている必要があります
- カバレッジレポートは既存のテスト設定に依存します
- `--fix`は実験的です - 何が変更されるかレビューしてください

## ドキュメンテーションコマンド 📝

### `/document` - 集中ドキュメンテーション
**何をするか**: 特定のコンポーネント、関数、または機能のドキュメントを作成します。

**いつ使うか**:
- READMEファイルが必要な時
- APIドキュメントの作成時
- コードコメントの追加時
- ユーザーガイドの作成時

**基本的な構文**:
```bash
/sc:document src/api/auth.js       # 認証モジュールを文書化
/sc:document --type api            # APIドキュメンテーション
/sc:document --style brief README  # 簡単なREADMEファイル
```

**便利なフラグ**:
- `--type inline|external|api|guide` - ドキュメントタイプ
- `--style brief|detailed` - 詳細レベル
- `--template` - 特定のドキュメンテーションテンプレートを使用

**実際の例**:
```bash
/sc:document --type api src/controllers/
/sc:document --style detailed --type guide user-onboarding
/sc:document --type inline src/utils/helpers.js
```

**注意点**:
- プロジェクト全体よりも、特定のファイル/関数でより効果的に機能します
- 品質の良し悪しは、コードがどれだけうまく構造化されているかによります
- プロジェクトのドキュメンテーションスタイルに合わせるために、いくつかの編集が必要になる場合があります

## プロジェクト管理コマンド 📊

### `/estimate` - プロジェクト見積もり
**何をするか**: 開発タスクの時間、労力、複雑性を見積もります。

**いつ使うか**:
- 新機能の計画時
- スプリント計画時
- プロジェクトの複雑性を理解する時
- リソース割り当て時

**基本的な構文**:
```bash
/sc:estimate "add user authentication"    # 認証機能を見積もり
/sc:estimate --detailed shopping-cart     # 詳細な内訳
/sc:estimate --complexity user-dashboard  # 複雑性分析
```

**便利なフラグ**:
- `--detailed` - タスクの詳細な内訳
- `--complexity` - 技術的な複雑性に焦点を当てる
- `--team-size <n>` - 見積もりにチームサイズを考慮

**実際の例**:
```bash
/sc:estimate --detailed "implement payment system"
/sc:estimate --complexity --team-size 3 "migrate to microservices"
/sc:estimate "add real-time chat" --detailed
```

**注意点**:
- 見積もりは概算です - 絶対的なものではなく、出発点として使用してください
- 明確で具体的な機能記述でより効果的に機能します
- 技術スタックに関するチームの経験を考慮してください

---

### `/task` - 長期プロジェクト管理
**何をするか**: 複雑で複数セッションにわたる開発タスクと機能を管理します。

**いつ使うか**:
- 数日/数週間かかる機能の計画時
- 大規模プロジェクトの分割時
- セッションをまたいで進捗を追跡する時
- チーム作業の調整時

**基本的な構文**:
```bash
/sc:task create "implement user dashboard"  # 新しいタスクを作成
/sc:task status                            # タスクのステータスを確認
/sc:task breakdown "payment integration"    # サブタスクに分割
```

**便利なフラグ**:
- `create` - 新しい長期タスクを作成
- `status` - 現在のタスクステータスを確認
- `breakdown` - 大きなタスクを小さなものに分割
- `--priority high|medium|low` - タスクの優先度を設定

**実際の例**:
```bash
/sc:task create "migrate from REST to GraphQL" --priority high
/sc:task breakdown "e-commerce checkout flow"
/sc:task status
```

**注意点**:
- まだ実験的です - セッションをまたいで確実に持続するとは限りません 😅
- 実際のプロジェクト管理よりも計画に適しています
- 要件について具体的に記述すると最も効果的に機能します

---

### `/spawn` - 複雑な操作のオーケストレーション
**何をするか**: 複雑でマルチステップの操作とワークフローを調整します。

**いつ使うか**:
- 複数のツール/システムが関与する操作
- 並行ワークフローの調整
- 複雑なデプロイメントプロセス
- マルチステージのデータ処理

**基本的な構文**:
```bash
/sc:spawn deploy-pipeline          # デプロイメントをオーケストレーション
/sc:spawn --parallel migrate-data  # 並行データ移行
/sc:spawn setup-dev-environment    # 複雑な開発環境のセットアップ
```

**便利なフラグ**:
- `--parallel` - 可能な場合は操作を並行して実行
- `--sequential` - 順次実行を強制
- `--monitor` - 操作の進捗を監視

**実際の例**:
```bash
/sc:spawn --parallel "test and deploy to staging"
/sc:spawn setup-ci-cd --monitor
/sc:spawn --sequential database-migration
```

**注意点**:
- 最も複雑なコマンド - いくつかの荒削りな部分を期待してください
- アドホックな操作よりも、明確に定義されたワークフローに適しています
- 正しく動作させるには、複数回のイテレーションが必要になる場合があります

## バージョン管理コマンド 🔄

### `/git` - 強化されたGit操作
**何をするか**: インテリジェントなコミットメッセージとワークフロー最適化を備えたGit操作。

**いつ使うか**:
- より良いメッセージでコミットを作成する時
- ブランチ管理
- 複雑なgitワークフロー
- Gitのトラブルシューティング

**基本的な構文**:
```bash
/sc:git commit                     # 自動生成メッセージ付きのスマートコミット
/sc:git --smart-commit add .       # スマートメッセージで追加してコミット
/sc:git branch feature/new-auth    # 新しいブランチを作成して切り替え
```

**便利なフラグ**:
- `--smart-commit` - インテリジェントなコミットメッセージを生成
- `--branch-strategy` - ブランチ命名規則を適用
- `--interactive` - 複雑な操作のためのインタラクティブモード

**実際の例**:
```bash
/sc:git --smart-commit "fixed login bug"
/sc:git branch feature/user-dashboard --branch-strategy
/sc:git merge develop --interactive
```

**注意点**:
- スマートコミットメッセージはかなり良いですが、レビューしてください
- 一般的なgitワークフローに従っていることを前提としています
- 悪いgitの習慣を修正するわけではありません - それらを容易にするだけです

## ユーティリティコマンド 🔧

### `/index` - コマンドナビゲーション
**何をするか**: タスクに適したコマンドを見つけるのに役立ちます。

**いつ使うか**:
- どのコマンドを使用すればよいかわからない時
- 利用可能なコマンドを探索する時
- コマンドの機能について学ぶ時

**基本的な構文**:
```bash
/sc:index                          # すべてのコマンドを一覧表示
/sc:index testing                  # テストに関連するコマンドを検索
/sc:index --category analysis      # 分析カテゴリのコマンド
```

**便利なフラグ**:
- `--category <cat>` - コマンドカテゴリでフィルタリング
- `--search <term>` - コマンドの説明を検索

**実際の例**:
```bash
/sc:index --search "performance"
/sc:index --category quality
/sc:index git
```

**注意点**:
- シンプルですが発見に役立ちます
- 17個すべてのコマンドを覚えようとするより良いです

---

### `/load` - プロジェクトコンテキストの読み込み
**何をするか**: より良い理解のためにプロジェクトのコンテキストを読み込んで分析します。

**いつ使うか**:
- 見慣れないプロジェクトでの作業開始時
- プロジェクト構造を理解する必要がある時
- 大きな変更を加える前
- チームメンバーのオンボーディング時

**基本的な構文**:
```bash
/sc:load                           # 現在のプロジェクトコンテキストを読み込み
/sc:load src/                      # 特定のディレクトリコンテキストを読み込み
/sc:load --deep                    # プロジェクト構造の詳細な分析
```

**便利なフラグ**:
- `--deep` - 包括的なプロジェクト分析
- `--focus <area>` - 特定のプロジェクト領域に焦点を当てる
- `--summary` - プロジェクトの概要を生成

**実際の例**:
```bash
/sc:load --deep --summary
/sc:load src/components/ --focus architecture
/sc:load . --focus dependencies
```

**注意点**:
- 大規模なプロジェクトでは時間がかかることがあります
- 開発中よりもプロジェクト開始時に役立ちます
- オンボーディングに役立ちますが、良いドキュメントの代わりにはなりません

---
### `add_mcp` - MCPサーバーの追加インストール
**何をするか**: SuperClaudeのインストール後に、追加でMCP（Multi-Claude Proxy）サーバーをインストールします。

**いつ使うか**:
- 特定のMCPサーバーだけを後から追加したい場合
- 最小構成でインストールした後、必要な機能を追加する際

**基本的な構文**:
```bash
# 利用可能なMCPサーバーの一覧を表示
SuperClaude add_mcp

# 特定のMCPサーバーをインストール
SuperClaude add_mcp magic

# 複数のMCPサーバーを一度にインストール
SuperClaude add_mcp magic playwright
```

**引数**:
- `mcp_names` - インストールしたいMCPサーバーの名前（複数指定可）。

**補足**:
- このコマンドは `claude mcp add` コマンドのラッパーとして機能します。
- サーバー名は `config/mcp_registry.json` に登録されている必要があります。

---

### `diagnose_mcp` - MCPサーバーの診断
**何をするか**: MCPサーバーに関する一般的な問題を診断するための一連のチェックを実行します。

**いつ使うか**:
- MCPサーバーが期待通りに動作しない場合
- コマンドがエラーを返す原因を特定したい時
- 環境設定（APIキーなど）が正しいか確認したい場合

**基本的な構文**:
```bash
# 診断プロセスを開始
SuperClaude diagnose_mcp
```

**診断内容**:
- **レベル1: 前提条件のチェック** - `node`, `npm`, `claude` CLIがインストールされているか、バージョンはいくつかを確認します。
- **レベル2: 設定ファイルの診断** - グローバルおよびローカルの設定ファイルを確認し、インストール済みのMCPが公式レジストリと一致しているか検証します。
- **レベル3: サーバー生存確認** - インストール済みの各サーバーにテスト通信を送り、正常に応答するか確認します。
- **レベル4: APIキーの確認** - APIキーを必要とするサーバー（例: `magic`）について、対応する環境変数が設定されているかチェックします。

**補足**:
- トラブルシューティングの第一歩として非常に役立ちます。
- 問題が解決しない場合、この診断結果を添えてイシューを報告するとスムーズです。

## コマンドのヒントとパターン 💡

### 効果的なフラグの組み合わせ
```bash
# 安全な改善ワークフロー
/sc:improve --preview src/component.js    # 何が変更されるかを確認
/sc:improve --safe src/component.js       # 安全な変更のみを適用

# 包括的な分析
/sc:analyze --focus security --depth deep
/sc:test --coverage
/sc:document --type api

# スマートなgitワークフロー
/sc:git add .
/sc:git --smart-commit --branch-strategy

# プロジェクト理解ワークフロー
/sc:load --deep --summary
/sc:analyze --focus architecture
/sc:document --type guide
```

### 一般的なワークフロー

**新規プロジェクトのオンボーディング**:
```bash
/sc:load --deep --summary
/sc:analyze --focus architecture
/sc:test --coverage
/sc:document README
```

**バグ調査**:
```bash
/sc:troubleshoot "specific error message" --logs
/sc:analyze --focus security
/sc:test --type unit affected-component
```

**コード品質改善**:
```bash
/sc:analyze --focus quality
/sc:improve --preview src/
/sc:cleanup --safe
/sc:test --coverage
```

**デプロイ前チェックリスト**:
```bash
/sc:test --type all --coverage
/sc:analyze --focus security
/sc:build --type prod --optimize
/sc:git --smart-commit
```

### コマンド問題のトラブルシューティング

**コマンドが期待通りに動作しない場合**
- `--help`を追加してすべてのオプションを確認してみてください
- 利用可能な場合は`--preview`または`--safe`フラグを使用してください
- 小さなスコープ（単一ファイル対プロジェクト全体）から始めてください

**分析に時間がかかりすぎる場合**
- `--focus`を使用してスコープを絞ってください
- 詳細な分析の代わりに`--depth quick`を試してください
- まず小さなディレクトリを分析してください

**ビルド/テストコマンドが失敗する場合**
- ツールがPATHにあることを確認してください
- 設定ファイルが期待される場所にあることを確認してください
- まず基盤となるコマンドを直接実行してみてください

**どのコマンドを使用すればよいかわからない場合**
- `/index`を使用して利用可能なコマンドを閲覧してください
- 上記のクイックリファレンス表を見てください
- まず最も具体的なコマンドを試し、次に広範なものを試してください

---

## 最後の注意点 📝

**これらのコマンドについての本当の真実** 💯:
- **とにかく試してみてください** - このガイドを最初に勉強する必要はありません
- **基本から始める** - `/analyze`, `/build`, `/improve`がほとんどのニーズをカバーします
- **自動アクティベーションに任せる** - SuperClaudeは通常、役立つ専門家を選びます
- **自由に実験する** - 何が起こるかまず見たい場合は`--preview`を使用してください

**まだ荒削りな部分:**
- 複雑なオーケストレーション（spawn, task）は少し不安定なことがあります
- 一部の分析はプロジェクトの設定に大きく依存します
- 一部のコマンドではエラーハンドリングが改善される可能性があります

**常に改善されています:**
- ユーザーのフィードバックに基づいてコマンドを積極的に改善しています
- 新しいコマンド（analyze, improve）はよりうまく機能する傾向があります
- 自動アクティベーションはますます賢くなっています

**これを覚えることにストレスを感じないでください** 🧘‍♂️
- SuperClaudeは使用を通じて発見できるように設計されています
- `/`をタイプして利用可能なコマンドを確認してください
- コマンドは`--help`を使用すると何ができるか提案します
- インテリジェントなルーティングが複雑さのほとんどを処理します

**助けが必要ですか？** GitHubのイシューを確認するか、行き詰まったら新しいものを作成してください！ 🚀

---

*コーディングを楽しんでください！覚えておいてください - このガイドのほとんどをスキップして、実行することで学ぶことができます。 🎯*
