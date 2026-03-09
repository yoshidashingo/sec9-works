# 要件定義書 - 情報同期バッチ処理（2方式）

## Intent Analysis

- **User Request**: 毎晩25時に起動する情報同期バッチ処理を、claude -p と Claude Agent SDK（Python）の2方式で実装する
- **Request Type**: New Project（既存インフラの拡張）
- **Scope**: Multiple Components（claude -p版 + Agent SDK版 + cron統合）
- **Complexity**: Moderate（既存パターンの踏襲 + 新技術スタックの導入）

---

## 1. プロジェクト概要

### 1.1 背景

本リポジトリには既に以下のバッチ同期インフラが存在する：

| スクリプト | データソース | MCPサーバー | 出力先 |
|-----------|-------------|------------|--------|
| sync-meetings-cron.sh | tldv（GA）, circleback（Sec9） | tldv-ga, circleback | output/ga/meetings/, output/sec9/meetings/ |
| sync-paulo-cron.sh | Gmail → Paulo記事 | google-workspace-sec9 | output/shingo/paulo-newsletter/ |
| sync-market-hack-cron.sh | Gmail → Market Hack記事 | google-workspace-sec9 | output/shingo/market-hack-magazine/ |

これらは全て `claude -p`（Claude Code CLI のパイプモード）で実装されている。

### 1.2 目的

同じデータソース群に対して、**Claude Agent SDK（Python）** による代替実装を追加する。用途に応じて `claude -p` と Agent SDK を使い分けられるようにする。

### 1.3 使い分けの方針

| 観点 | claude -p | Agent SDK（Python） |
|------|----------|-------------------|
| 強み | セットアップ不要、MCPサーバー統合が簡単、プロンプトファイルで宣言的に定義 | プログラマティックな制御、エラーハンドリングの柔軟性、テスト容易性 |
| 適する場面 | 定型的な同期処理、プロンプトの変更だけで対応できるケース | 複雑な条件分岐、リトライロジック、データ変換が必要なケース |

---

## 2. 機能要件

### FR-1: claude -p版バッチ同期

既存の同期処理と同等の機能を持つ claude -p 版スクリプト。

**対象データソース（既存と同一）:**

- **FR-1.1**: GA社ミーティング議事録同期（tldv経由）
- **FR-1.2**: Sec9社ミーティング議事録同期（circleback経由）
- **FR-1.3**: Pauloニュースレター記事同期（Gmail経由）
- **FR-1.4**: Market Hack Magazine記事同期（Gmail経由）

**注**: FR-1は既存スクリプトが既に実装済み。新規追加が必要な場合のテンプレートとして定義。

### FR-2: Agent SDK版バッチ同期

Python（anthropic-sdk-python）を使用した Agent SDK 版の同期処理。

- **FR-2.1**: GA社ミーティング議事録同期（tldv経由）
- **FR-2.2**: Sec9社ミーティング議事録同期（circleback経由）
- **FR-2.3**: Pauloニュースレター記事同期（Gmail経由）
- **FR-2.4**: Market Hack Magazine記事同期（Gmail経由）

**Agent SDK版の要件:**

- **FR-2.5**: MCPサーバー接続 — 既存のMCPサーバー（tldv-ga, circleback, google-workspace-sec9等）にAgent SDKから接続し、ツールとして利用できること
- **FR-2.6**: 同期状態管理 — `_sync-state.json` を用いた増分同期（既存パターン踏襲）
- **FR-2.7**: ファイル出力 — 既存と同一の出力先・フォーマットでmdファイルを生成すること
- **FR-2.8**: git操作 — 同期完了後に変更をcommit & pushすること

### FR-3: スケジューリングと統合

- **FR-3.1**: 毎晩25時（1:00 AM）に自動実行されること
- **FR-3.2**: 既存の `sync-all-cron.sh` との統合方針は設計段階で決定する
- **FR-3.3**: claude -p版とAgent SDK版の切り替えが容易であること（設定変更のみで切替可能）

### FR-4: 共通機能

- **FR-4.1**: ロギング — 実行ログを `logs/` ディレクトリに保存すること
- **FR-4.2**: 重複実行防止 — ロックファイルによる排他制御
- **FR-4.3**: sync-state バリデーション — 事前・事後の `_sync-state.json` 整合性チェック
- **FR-4.4**: git操作の安全性 — `git-sync-helper.sh` またはそれに相当する仕組みを使用

---

## 3. 非機能要件

### NFR-1: 実行環境

- **NFR-1.1**: ローカルmacOS（現在のcronと同一環境）で実行
- **NFR-1.2**: Python 3.11以上（macOSのHomebrewまたはpyenvでインストール済み前提）
- **NFR-1.3**: anthropic-sdk-python の最新安定版を使用

### NFR-2: 信頼性

- **NFR-2.1**: 個別同期タスクの失敗が他のタスクに影響しないこと
- **NFR-2.2**: LLMハルシネーションによる `_sync-state.json` 破損を検出・復旧できること
- **NFR-2.3**: ネットワーク障害時のリトライ（最大3回）

### NFR-3: コスト

- **NFR-3.1**: 各同期タスクの1回あたりAPIコストを制限できること（claude -p: --max-budget-usd、Agent SDK: トークン数制限）
- **NFR-3.2**: 既存のコスト水準（ミーティング: $1.00/回、記事: $0.50/回）を大きく超えないこと

### NFR-4: 保守性

- **NFR-4.1**: claude -p版とAgent SDK版で同一のプロンプト/同期ロジックを共有できること（DRY原則）
- **NFR-4.2**: 新しいデータソースの追加が容易なアーキテクチャ
- **NFR-4.3**: Agent SDK版のPythonコードはテスト可能な構造（関数分離、依存性注入）

### NFR-5: セキュリティ

- **NFR-5.1**: APIキーは環境変数で管理（ハードコードしない）
- **NFR-5.2**: MCPサーバーのアクセスは企業別に厳格に分離（CLAUDE.mdのマルチテナントルール準拠）

---

## 4. 技術的制約

### 4.1 既存インフラとの互換性

- 出力先ディレクトリ・ファイルフォーマットは既存と完全互換
- `_sync-state.json` のスキーマは既存と同一
- `git-sync-helper.sh` のロック機構と共存

### 4.2 MCPサーバー接続（Agent SDK版）

- Agent SDKからMCPサーバーに接続するためのアダプター層が必要
- MCPサーバーの設定は既存の `.claude/` 配下の設定を参照
- MCP Python SDK（`mcp` パッケージ）を使用してstdio接続

### 4.3 claude -p版の既存制約

- `--allowedTools` でツールアクセスを制限
- `--max-turns` と `--max-budget-usd` でコスト制御
- `--output-format json` でログ出力
- `unset CLAUDECODE` でネストセッション回避

---

## 5. 成果物

| 成果物 | 説明 |
|--------|------|
| 設計文書 | アーキテクチャ設計、データフロー図、API仕様 |
| claude -p版スクリプト | 既存パターン踏襲のシェルスクリプト + プロンプトファイル（新規追加分がある場合） |
| Agent SDK版Pythonコード | anthropic-sdk-python + MCP接続を使ったバッチ同期プログラム |
| cron統合スクリプト | sync-all-cron.sh の更新または新規エントリポイント |
| テスト | Agent SDK版のユニットテスト・統合テスト |
