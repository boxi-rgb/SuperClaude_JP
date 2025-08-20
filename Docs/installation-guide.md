# SuperClaude インストールガイド 📦

## 🎯 見た目より簡単です！

**正直なところ**: このガイドはすべての詳細を網羅しているため長く見えますが、実際のインストールは非常にシンプルです。ほとんどの人は1つのコマンドで2分で完了します！

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

### ⚠️ 重要事項
**SuperClaudeをインストールした後。**
**`SuperClaude <コマンド>`、`python3 -m SuperClaude <コマンド>`、または `python3 SuperClaude <コマンド>` が使用できます**

**何が起こったか？** SuperClaudeは必要なものをすべてセットアップしようとしました。通常、複雑な設定、依存関係の検索、セットアップの手間はありません！ 🎉

---

SuperClaude v3をインストールするための包括的なガイドです。しかし、ほとんどの人は上記のクイックスタート以降を読む必要はないことを覚えておいてください！ 😊

## 始める前に 🔍

### 必要なもの 💻

SuperClaudeは **Windows**、**macOS**、**Linux** で動作します。必要なものは以下の通りです:

**必須:**
- **Python 3.8以降** - フレームワークはPythonで書かれています
- **Claude CLI** - SuperClaudeはClaude Codeを強化するため、最初にインストールしておく必要があります

**任意（推奨）:**
- **Node.js 16+** - MCPサーバー統合が必要な場合のみ
- **Git** - 開発ワークフローに役立ちます

### クイックチェック 🔍

インストールする前に、基本的なものが揃っているか確認しましょう:

```bash
# Pythonのバージョンを確認（3.8+であるべき）
python3 --version

# Claude CLIがインストールされているか確認
claude --version

# Node.jsを確認（任意、MCPサーバー用）
node --version
```

これらのいずれかが失敗した場合は、下の[前提条件のセットアップ](#前提条件のセットアップ-️)セクションを参照してください。

## クイックスタート 🚀

**🏆 「とにかく動かす」アプローチ（90%のユーザーに推奨）**
**オプションA: PyPIから（推奨）**
```bash
pip install SuperClaude

# 推奨設定でインストール
SuperClaude install --quick

# これで完了です！ 🎉
```
**オプションB: ソースから**
```bash
# リポジトリをクローン
git clone <repository-url>
cd SuperClaude
pip install .

# 推奨設定でインストール
SuperClaude install --quick

# これで完了です！ 🎉
```
**⚠️ 重要事項**
**SuperClaudeをインストールした後。**
**`SuperClaude <コマンド>`、`python3 -m SuperClaude <コマンド>`、または `python3 SuperClaude <コマンド>` が使用できます**

**何が得られたか:**
- ✅ 専門家を自動起動する17のスマートコマンドすべて
- ✅ いつ助けるべきかを知っている11の専門家ペルソナ
- ✅ 複雑さを自動で解決するインテリジェントなルーティング
- ✅ 約2分間の時間と約50MBのディスクスペース

**本当に、これで完了です。** Claude Codeを開き、`/help`と入力して、SuperClaudeが魔法のように動作するのを見てください。

**何が起こるか心配ですか？** まずは以下で確認してください:
```bash
SuperClaude install --quick --dry-run
```

## インストールオプション 🎯

3つのインストールプロファイルから選択できます:

### 🎯 最小インストール
```bash
SuperClaude install --minimal
```
- **内容**: コアフレームワークファイルのみ
- **時間**: 約1分
- **容量**: 約20MB
- **適している人**: テスト、基本的な機能強化、最小限のセットアップ
- **含まれるもの**: Claudeの応答をガイドするコアな振る舞いに関するドキュメント

### 🚀 クイックインストール（推奨）
```bash
SuperClaude install --quick
```
- **内容**: コアフレームワーク + 17のスラッシュコマンド
- **時間**: 約2分
- **容量**: 約50MB
- **適している人**: ほとんどのユーザー、一般的な開発
- **含まれるもの**: 最小インストールのすべて + `/analyze`、`/build`、`/improve`などの専門コマンド

### 🔧 開発者向けインストール
```bash
SuperClaude install --profile developer
```
- **内容**: MCPサーバー統合を含むすべて
- **時間**: 約5分
- **容量**: 約100MB
- **適している人**: パワーユーザー、貢献者、高度なワークフロー
- **含まれるもの**: すべて + Context7、Sequential、Magic、Playwrightサーバー

### 🎛️ インタラクティブインストール
```bash
SuperClaude install
```
- コンポーネントを選択できます
- 各コンポーネントが何をするかの詳細な説明を表示します
- 何をインストールするかを制御したい場合に適しています

## ステップバイステップのインストール 📋

### 前提条件のセットアップ 🛠️

**Pythonがありませんか？**
```bash
# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows
# https://python.org/downloads/ からダウンロード
# またはコマンドプロンプトやpowershellで
winget install python
```

**Claude CLIがありませんか？**
- インストール手順については https://claude.ai/code をご覧ください
- SuperClaudeはClaude Codeを強化するため、最初にそれが必要です

**Node.jsがありませんか？ (任意)**
```bash
# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install nodejs npm

# macOS
brew install node

# Windows
# https://nodejs.org/ からダウンロード
# またはコマンドプロンプトやpowershellで
winget install nodejs
```

### SuperClaudeの入手 📥

**オプション1: PyPIから（推奨）**
```bash
pip install SuperClaude
```

**オプション2: 最新リリースをダウンロード**
```bash
# 最新リリースをダウンロードして展開
# (URLを実際のリリースURLに置き換えてください)
curl -L <release-url> -o superclaude-v3.zip
unzip superclaude-v3.zip
cd superclaude-v3
pip install .
```

**オプション3: Gitからクローン**
```bash
git clone <repository-url>
cd SuperClaude
pip install .
```

### インストーラーの実行 🎬

インストーラーは非常にスマートで、プロセスをガイドしてくれます:

```bash
# 利用可能なすべてのオプションを表示
SuperClaude install --help

# クイックインストール（推奨）
SuperClaude install --quick

# 何が起こるかまず確認したい場合
SuperClaude install --quick --dry-run

# すべてをインストール
SuperClaude install --profile developer

# 静かなインストール（最小限の出力）
SuperClaude install --quick --quiet

# 強制インストール（確認をスキップ）
python3 SuperClaude.py install --quick --force
```

### インストール中 📱

インストール中に起こること:

1. **システムチェック** - 必要な依存関係があるか検証します
2. **ディレクトリ設定** - `~/.claude/` ディレクトリ構造を作成します
3. **コアファイル** - フレームワークのドキュメントファイルをコピーします
4. **コマンド** - スラッシュコマンドの定義をインストールします（選択した場合）
5. **MCPサーバー** - MCPサーバーをダウンロードして設定します（選択した場合）
6. **設定** - `settings.json` をあなたの好みに合わせて設定します
7. **検証** - すべてが機能するかテストします

インストーラーは進捗を表示し、何か問題があれば教えてくれます。

## インストール後 ✅

### クイックテスト 🧪

すべてが機能したか確認しましょう:

```bash
# ファイルがインストールされたか確認
ls ~/.claude/

# CLAUDE.md, COMMANDS.md, settings.jsonなどが表示されるはずです
```

**Claude Codeでテスト:**
1. Claude Codeを開きます
2. `/help`と入力してみてください - SuperClaudeのコマンドが表示されるはずです
3. `/analyze --help`と試してみてください - コマンドのオプションが表示されるはずです

### 何がインストールされたか 📂

SuperClaudeはデフォルトで `~/.claude/` にインストールされます。そこには以下のものがあります:

```
~/.claude/
├── CLAUDE.md              # メインフレームワークのエントリーポイント
├── COMMANDS.md             # 利用可能なスラッシュコマンド
├── FLAGS.md                # コマンドのフラグとオプション
├── PERSONAS.md             # スマートペルソナシステム
├── PRINCIPLES.md           # 開発原則
├── RULES.md                # 運用ルール
├── MCP.md                  # MCPサーバー統合
├── MODES.md                # 運用モード
├── ORCHESTRATOR.md         # インテリジェントルーティング
├── settings.json           # 設定ファイル
└── commands/               # 個々のコマンド定義
    ├── analyze.md
    ├── build.md
    ├── improve.md
    └── ... (14 more)
```

**各ファイルがすること:**
- **CLAUDE.md** - SuperClaudeについてClaude Codeに伝え、他のファイルを読み込みます
- **settings.json** - 設定（MCPサーバー、フックなど）
- **commands/** - 各スラッシュコマンドの詳細な定義

### 最初のステップ 🎯

始めるには、これらのコマンドを試してみてください:

```bash
# Claude Codeで、これらを試してみてください:
/sc:help                    # 利用可能なコマンドを表示
/sc:analyze README.md       # ファイルを分析
/sc:build --help           # ビルドオプションを表示
/sc:improve --help         # 改善オプションを表示
```

**圧倒されても心配しないでください** - SuperClaudeは徐々にClaude Codeを強化します。好きなだけ使ってください。

## インストールの管理 🛠️

### アップデート 📅

SuperClaudeを最新の状態に保ちます:

```bash
# アップデートを確認
SuperClaude update

# 強制アップデート（ローカルの変更を上書き）
SuperClaude update --force

# 特定のコンポーネントのみをアップデート
SuperClaude update --components core,commands

# 何がアップデートされるか確認
SuperClaude update --dry-run
```

**いつアップデートするか:**
- 新しいSuperClaudeのバージョンがリリースされた時
- 問題が発生している場合（アップデートにはしばしば修正が含まれます）
- 新しいMCPサーバーが利用可能になった時

### バックアップ 💾

大きな変更の前にバックアップを作成します:

```bash
# バックアップを作成
SuperClaude backup --create

# 既存のバックアップを一覧表示
SuperClaude backup --list

# バックアップから復元
SuperClaude backup --restore

# カスタム名でバックアップを作成
SuperClaude backup --create --name "before-update"
```

**いつバックアップするか:**
- SuperClaudeをアップデートする前
- 設定を試す前
- アンインストールする前
- 大幅にカスタマイズした場合は定期的に

### アンインストール 🗑️

SuperClaudeを削除する必要がある場合:

```bash
# SuperClaudeを削除（バックアップは保持）
SuperClaude uninstall

# 完全削除（すべてを削除）
SuperClaude uninstall --complete

# 何が削除されるか確認
SuperClaude uninstall --dry-run
```

**何が削除されるか:**
- `~/.claude/` 内のすべてのファイル
- MCPサーバーの設定
- Claude CodeからのSuperClaude設定

**何が残るか:**
- バックアップ（`--complete`を使用しない限り）
- Claude Code自体（SuperClaudeは触れません）
- あなたのプロジェクトや他のファイル

## トラブルシューティング 🔧

### 一般的な問題 🚨

**"Python not found"**
```bash
# python3の代わりにpythonを試す
python --version

# またはインストールされているがPATHにないか確認
which python3
```

**"Claude CLI not found"**
- 最初にClaude Codeがインストールされていることを確認してください
- `claude --version`で確認してみてください
- インストールヘルプについては https://claude.ai/code をご覧ください

**"Permission denied"**
```bash
# 明示的なPythonパスで試す
/usr/bin/python3 SuperClaude.py install --quick

# または異なる権限が必要か確認
ls -la ~/.claude/
```

**"MCP servers won't install"**
- Node.jsがインストールされているか確認: `node --version`
- npmが利用可能か確認: `npm --version`
- まずMCPなしでインストールしてみてください: `--minimal` または `--quick`

**MCPサーバーが動作しない、または問題がある場合 (If MCP servers are not working or have issues)**
- まずは `SuperClaude diagnose_mcp` を実行してください。このコマンドは、依存関係、設定、サーバーの応答性など、一般的な問題を自動でチェックします。
- `First, run "SuperClaude diagnose_mcp". This command automatically checks for common issues, including dependencies, configuration, and server responsiveness.`

**"Installation fails partway through"**
```bash
# 何が起こっているか詳細な出力で試す
SuperClaude install --quick --verbose

# またはまずドライランを試す
SuperClaude install --quick --dry-run
```

### プラットフォーム固有の問題 🖥️

**Windows:**
- "command not found"と表示されたら `python3` の代わりに `python` を使用してください
- 権限エラーが表示されたらコマンドプロンプトを管理者として実行してください
- PythonがPATHに含まれていることを確認してください

**macOS:**
- セキュリティとプライバシー設定でSuperClaudeを承認する必要があるかもしれません
- Python 3.8+がない場合は `brew install python3` を使用してください
- `python` の代わりに `python3` を明示的に使用してみてください

**Linux:**
- `python3-pip` がインストールされていることを確認してください
- 一部のパッケージインストールには `sudo` が必要かもしれません
- `~/.local/bin` がPATHに含まれていることを確認してください

### まだ問題がありますか？ 🤔

**トラブルシューティングリソースを確認してください:**
- GitHub Issues: https://github.com/SuperClaude-Org/SuperClaude_Framework/issues
- あなたの問題に似た既存のイシューを探してください
- 解決策が見つからない場合は新しいイシューを作成してください

**バグを報告する際は、以下を含めてください:**
- オペレーティングシステムとバージョン
- Pythonのバージョン（`python3 --version`）
- Claude CLIのバージョン（`claude --version`）
- 実行した正確なコマンド
- 完全なエラーメッセージ
- 何が起こると期待したか

**助けを得る:**
- 一般的な質問はGitHub Discussionsへ
- 最新情報はREADME.mdを確認してください
- あなたの問題が既知かどうかROADMAP.mdを見てください

## 高度なオプション ⚙️

### カスタムインストールディレクトリ

```bash
# カスタムの場所にインストール
SuperClaude install --quick --install-dir /custom/path

# 環境変数を使用
export SUPERCLAUDE_DIR=/custom/path
SuperClaude install --quick
```

### コンポーネントの選択

```bash
# 利用可能なコンポーネントを表示
SuperClaude install --list-components

# 特定のコンポーネントのみをインストール
SuperClaude install --components core,commands

# 特定のコンポーネントをスキップ
SuperClaude install --quick --skip mcp
```

### 開発セットアップ

SuperClaudeに貢献したり、変更したりする予定がある場合:

```bash
# すべてのコンポーネントを含む開発者向けインストール
SuperClaude install --profile developer

# 開発モードでインストール（コピーの代わりにシンボリックリンクを使用）
SuperClaude install --profile developer --dev-mode

# 開発用のgitフックと共にインストール
SuperClaude install --profile developer --dev-hooks
```

## 次は？ 🚀

**SuperClaudeがインストールされた今（簡単でしたよね？）:**

1. **とにかく使い始める** - `/analyze some-file.js` や `/build` を試して何が起こるか見てみましょう ✨
2. **学ぶことにストレスを感じないで** - SuperClaudeは通常、あなたが必要なものを理解します
3. **自由に実験する** - `/improve` や `/troubleshoot` のようなコマンドはかなり寛容です
4. **興味があればガイドを読む** - 何が起こったか理解したい時に `Docs/` を確認してください
5. **フィードバックを送る** - 何が機能して何が機能しないか教えてください

**本当の秘密**: SuperClaudeは、あなたがたくさんの新しいことを学ばなくても、既存のワークフローを強化するように設計されています。通常のClaude Codeのように使うだけで、どれだけ賢くなるかに気づくでしょう！ 🎯

**まだ不安ですか？** `/help` と `/analyze README.md` だけで始めてみてください - それがどれほど威圧的でないかわかるでしょう。

---

## 最後の注意点 📝

- **インストールには1〜5分かかります**（選択によります）
- **必要なディスク容量: 20〜100MB**（それほど多くありません！）
- **既存のツールと連携して動作します** - あなたのセットアップを妨げません
- **気が変わっても簡単にアンインストールできます**
- **コミュニティによってサポートされています** - 私たちは実際にイシューを読んで対応します
- ### ⚠️ 重要事項
**SuperClaudeをインストールした後。**
**`SuperClaude <コマンド>`、`python3 -m SuperClaude <コマンド>`、または `python3 SuperClaude <コマンド>` が使用できます**

SuperClaudeをお試しいただきありがとうございます！あなたの開発ワークフローが少しでもスムーズになることを願っています。 🙂

---

*最終更新: 2024年7月 - このガイドに間違いや紛らわしい点があればお知らせください！*
