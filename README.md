# SuperClaude v3 🚀 (日本語フォーク版)

**これは `SuperClaude-Org/SuperClaude_Framework` の日本語化フォークです。**
**ドキュメントやコミュニケーションは日本語で行われます。**

[![Website Preview](https://img.shields.io/badge/Visit-Website-blue?logo=google-chrome)](https://superclaude-org.github.io/SuperClaude_Website/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/SuperClaude.svg)](https://pypi.org/project/SuperClaude/)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/SuperClaude-Org/SuperClaude_Framework)
[![GitHub issues](https://img.shields.io/github/issues/SuperClaude-Org/SuperClaude_Framework)](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/master/CONTRIBUTING.md)
[![Contributors](https://img.shields.io/github/contributors/SuperClaude-Org/SuperClaude_Framework)](https://github.com/SuperClaude-Org/SuperClaude_Framework/graphs/contributors)
[![Website](https://img.shields.io/website?url=https://superclaude-org.github.io/SuperClaude_Website/)](https://superclaude-org.github.io/SuperClaude_Website/)

Claude Codeを専門コマンド、ペルソナ、MCPサーバー統合で拡張するフレームワークです。

**📢 ステータス**: 初期リリース、ベータ版を卒業したばかりです！改善を続ける中でバグが発生する可能性があります。

## SuperClaudeとは？ 🤔

SuperClaudeは、以下の機能を追加することで、Claude Codeを開発作業でより役立つものにします:
- 🛠️ 一般的な開発タスクのための**17の専門コマンド**（一部はまだ改善の余地があります！）
- 🎭 様々なドメインに適した専門家を自動で選択する**スマートペルソナ**
- 🔧 ドキュメント、UIコンポーネント、ブラウザ自動化のための**MCPサーバー統合**
- 📋 進捗を追跡しようと試みる**タスク管理**
- ⚡ 長い会話を助ける**トークン最適化**

これは、開発ワークフローをよりスムーズにするために私たちが構築してきたものです。まだ粗削りですが、日々改善されています！ 😊

## 現在のステータス 📊

✅ **正常に機能しているもの:**
- インストールスイート（ゼロから再設計）
- 9つのドキュメントファイルを持つコアフレームワーク
- 様々な開発タスクのための17のスラッシュコマンド
- MCPサーバー統合（Context7, Sequential, Magic, Playwright）
- 簡単なセットアップのための統一CLIインストーラー

⚠️ **既知の問題:**
- これは初期リリースです - バグが予想されます
- 一部の機能はまだ完璧に動作しない可能性があります
- ドキュメントはまだ改善中です
- フックシステムは削除されました（v4で復活予定）

## 主な特徴 ✨

### コマンド 🛠️
最も一般的なタスクのために、17の必須コマンドに焦点を当てました:

**開発**: `/sc:implement`, `/sc:build`, `/sc:design`
**分析**: `/sc:analyze`, `/sc:troubleshoot`, `/sc:explain`
**品質**: `/sc:improve`, `/sc:test`, `/sc:cleanup`
**その他**: `/sc:document`, `/sc:git`, `/sc:estimate`, `/sc:task`, `/sc:index`, `/sc:load`, `/sc:spawn`, `/sc:workflow`

### スマートペルソナ 🎭
関連性がある場合に自動で介入するAIスペシャリスト:
- 🏗️ **architect** - システム設計とアーキテクチャ
- 🎨 **frontend** - UI/UXとアクセシビリティ
- ⚙️ **backend** - APIとインフラストラクチャ
- 🔍 **analyzer** - デバッグと問題解明
- 🛡️ **security** - セキュリティの懸念と脆弱性
- ✍️ **scribe** - ドキュメントとライティング
- *...その他5人のスペシャリスト*

*（常に完璧ではありませんが、通常は正しく選択されます！）*

### MCP統合 🔧
役立つ時に接続する外部ツール:
- **Context7** - 公式ライブラリのドキュメントとパターンを取得
- **Sequential** - 複雑な多段階思考を支援
- **Magic** - 最新のUIコンポーネントを生成
- **Playwright** - ブラウザの自動化とテスト

*（正しく接続されれば、これらは非常によく機能します！🤞）*

### 管理コマンド ⚙️
- **`SuperClaude add_mcp`** - MCPサーバーを後から追加でインストールします。
- **`SuperClaude diagnose_mcp`** - MCPサーバー関連の問題を診断するためのトラブルシューティングツールです。

## ⚠️ v2からのアップグレードですか？重要！

SuperClaude v2から移行する場合、まずクリーンアップが必要です:

1. **v2のアンインストール** - アンインストーラーが利用可能な場合はそれを使用
2. **手動クリーンアップ** - 以下のファイル/ディレクトリが存在する場合は削除:
   - `SuperClaude/`
   - `~/.claude/shared/`
   - `~/.claude/commands/` 
   - `~/.claude/CLAUDE.md`
3. **その後** v3のインストールに進んでください

これは、v3が異なる構造を持っており、古いファイルが競合を引き起こす可能性があるためです。

### 🔄 v2ユーザー向けの主な変更点
**`/build`コマンドが変更されました！** v2では、`/build`は機能実装に使用されていました。v3では:
- `/sc:build` = コンパイル/パッケージングのみ
- `/sc:implement` = 機能実装（新規！）

**移行**: `v2 /build myFeature` を `v3 /sc:implement myFeature` に置き換えてください

## インストール 📦

SuperClaudeのインストールは**2段階のプロセス**です:
1. まずPythonパッケージをインストールします
2. 次にインストーラーを実行してClaude Codeとの統合をセットアップします

### ステップ1: パッケージのインストール

**オプションA: PyPIから（推奨）**
```bash
uv add SuperClaude
```

**オプションB: ソースから**
```bash
git clone https://github.com/SuperClaude-Org/SuperClaude_Framework.git
cd SuperClaude_Framework
uv sync
```

### 🔧 UV / UVX セットアップガイド

SuperClaude v3は、[`uv`](https://github.com/astral-sh/uv)（高速でモダンなPythonパッケージマネージャー）またはクロスプラットフォーム用の `uvx` を介したインストールもサポートしています。

### 🌀 `uv` でインストール

`uv` がインストールされていることを確認してください:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

> または、こちらの指示に従ってください: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

`uv` が利用可能になったら、次のようにSuperClaudeをインストールできます:

```bash
uv venv
source .venv/bin/activate
uv pip install SuperClaude
```

### ⚡ `uvx` でインストール（クロスプラットフォームCLI）

`uvx` を使用している場合は、次を実行するだけです:

```bash
uvx pip install SuperClaude
```

### ✅ インストールの完了

インストール後、通常のインストーラーステップに進みます:

```bash
python3 -m SuperClaude install
```

またはbash形式のCLIを使用:

```bash
SuperClaude install
```

### 🧠 注意:

* `uv` は、より優れたキャッシングとパフォーマンスを提供します。
* Python 3.8+と互換性があり、SuperClaudeとスムーズに動作します。

---
**Pythonがありませんか？** まずPython 3.8+をインストールしてください:
```bash
# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip

# macOS  
brew install python3

# Windows
# https://python.org/downloads/ からダウンロード
```

### ステップ2: インストーラーの実行

パッケージをインストールした後、SuperClaudeインストーラーを実行してClaude Codeを設定します（いずれかの方法を使用できます）:
### ⚠️ 重要事項
**SuperClaudeをインストールした後。**
**`SuperClaude <コマンド>`、`python3 -m SuperClaude <コマンド>`、または `python3 SuperClaude <コマンド>` が使用できます**
```bash
# クイックセットアップ（ほとんどのユーザーに推奨）
SuperClaude install

# インタラクティブ選択（コンポーネントを選択）
SuperClaude install --interactive

# 最小インストール（コアフレームワークのみ）
SuperClaude install --minimal

# 開発者向けセットアップ（すべて込み）
SuperClaude install --profile developer

# 利用可能なすべてのオプションを表示
SuperClaude install --help
```

**以上です！🎉** インストーラーがすべてを処理します：フレームワークファイル、MCPサーバー、およびClaude Codeの設定。

## 仕組み 🔄

SuperClaudeは、以下を通じてClaude Codeを強化しようと試みます:

1. **フレームワークファイル** - `~/.claude/` にインストールされるドキュメントで、Claudeの応答をガイドします
2. **スラッシュコマンド** - 様々な開発タスクのための17の専門コマンド
3. **MCPサーバー** - 追加機能を提供する外部サービス（正常に動作する場合！）
4. **スマートルーティング** - あなたの作業内容に基づいて適切なツールと専門家を選択しようと試みます

ほとんどの場合、Claude Codeの既存の機能とうまく連携します。🤝

## v4での今後の予定 🔮

次のバージョンでは、これらのことに取り組みたいと考えています:
- **フックシステム** - イベント駆動の機能（v3で削除、適切に再設計中）
- **MCPスイート** - さらなる外部ツール統合
- **パフォーマンス向上** - より速く、バグの少ない動作を目指します
- **ペルソナの追加** - さらにいくつかのドメイン専門家を追加するかもしれません
- **クロスCLIサポート** - 他のAIコーディングアシスタントで動作する可能性があります

*（タイムラインは約束できませんが - まだv3を模索中です！😅）*

## 設定 ⚙️

インストール後、以下を編集してSuperClaudeをカスタマイズできます:
- `~/.claude/settings.json` - メイン設定
- `~/.claude/*.md` - フレームワークの振る舞いを定義するファイル

ほとんどのユーザーは何も変更する必要はないでしょう - 通常は初期設定のままで問題なく動作します。🎛️

## ドキュメント 📖

さらに詳しく知りたいですか？私たちのガイドをご覧ください:

- 📚 [**ユーザーガイド**](Docs/superclaude-user-guide.md) - 完全な概要と入門
- 🛠️ [**コマンドガイド**](Docs/commands-guide.md) - 17すべてのスラッシュコマンドの説明
- 🏳️ [**フラグガイド**](Docs/flags-guide.md) - コマンドのフラグとオプション
- 🎭 [**ペルソナガイド**](Docs/personas-guide.md) - ペルソナシステムの理解
- 📦 [**インストールガイド**](Docs/installation-guide.md) - 詳細なインストール手順

これらのガイドは、このREADMEよりも詳細な情報を含み、常に最新の状態に保たれています。

## 貢献 🤝

貢献を歓迎します！ご協力いただけると助かる分野:
- 🐛 **バグ報告** - 何が壊れているか教えてください
- 📝 **ドキュメント** - より良い説明にご協力ください
- 🧪 **テスト** - 様々なセットアップのためのテストカバレッジ向上
- 💡 **アイデア** - 新機能や改善点の提案

コードベースは、非常に単純なPython + ドキュメントファイルで構成されています。

## プロジェクト構造 📁

```
SuperClaude/
├── setup.py               # pypiセットアップファイル
├── SuperClaude/           # フレームワークファイル
│   ├── Core/              # 振る舞いを定義するドキュメント (COMMANDS.md, FLAGS.md, など)
│   ├── Commands/          # 17のスラッシュコマンド定義
│   └── Settings/          # 設定ファイル
├── setup/                 # インストールシステム
└── profiles/              # インストールプロファイル (quick, minimal, developer)
```

## アーキテクチャに関する注意点 🏗️

v3のアーキテクチャは以下に焦点を当てています:
- **シンプルさ** - 価値を生まない複雑さを排除
- **信頼性** - より良いインストールと少ない破壊的変更
- **モジュール性** - 必要なコンポーネントだけを選択
- **パフォーマンス** - よりスマートなキャッシングによる高速な操作

私たちはv2から多くを学び、主な問題点に対処しようと試みました。

## よくある質問 🙋

**Q: なぜフックシステムは削除されたのですか？**
A: 複雑でバグが多くなっていたためです。v4に向けて適切に再設計しています。

**Q: これは他のAIアシスタントで動作しますか？**
A: 現在はClaude Codeのみですが、v4ではより広範な互換性を持つ予定です。

**Q: これは日常的に使用できるほど安定していますか？**
A: 基本的な機能はかなりうまく動作しますが、リリースされたばかりなので、間違いなくいくつかの荒削りな部分があります。実験には問題ないでしょう！🧪

## SuperClaude 貢献者

[![Contributors](https://contrib.rocks/image?repo=SuperClaude-Org/SuperClaude_Framework)](https://github.com/SuperClaude-Org/SuperClaude_Framework/graphs/contributors)

## ライセンス

MIT - [詳細はLICENSEファイルをご覧ください](LICENSE)

## Starの履歴

<a href="https://www.star-history.com/#SuperClaude-Org/SuperClaude_Framework&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=SuperClaude-Org/SuperClaude_Framework&type=Date" />
 </picture>
</a>
---

*ありきたりな応答に飽きた開発者によって作られました。お役に立てれば幸いです！🙂*

---
