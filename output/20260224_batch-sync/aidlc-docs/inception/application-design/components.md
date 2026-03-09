# Components - 情報同期バッチ処理（Agent SDK版）

## Component Overview

```
scripts/agent-sdk/
  sync_agent.py          ← エントリポイント（全同期タスクのオーケストレーション）
  mcp_config.py          ← MCPConfigLoader: .mcp.json 解析
  mcp_client.py          ← MCPClientManager: MCP接続・ツール呼び出し
  agent_loop.py          ← AgentLoop: anthropic SDK エージェントループ
  sync_state.py          ← SyncStateManager: _sync-state.json 管理
  requirements.txt       ← Python依存関係
```

---

## C1: MCPConfigLoader (`mcp_config.py`)

**Purpose**: `.mcp.json` を解析し、MCPサーバーの起動設定を取得する

**Responsibilities**:
- `.mcp.json` ファイルの読み込みとパース
- サーバー名をキーとした設定辞書の提供
- stdio型（command + args + env）とHTTP型（url）の両方をサポート
- 環境変数のマージ（サーバー固有env + プロセスenv）

**Interfaces**:
- Input: `.mcp.json` ファイルパス
- Output: `dict[str, MCPServerConfig]`（サーバー名 → 設定）

---

## C2: MCPClientManager (`mcp_client.py`)

**Purpose**: MCP Python SDKを使い、MCPサーバーへの接続とツール呼び出しを管理する

**Responsibilities**:
- MCPサーバーのライフサイクル管理（起動・接続・切断）
- stdio型サーバーの subprocess 起動
- HTTP型サーバーへのHTTP接続（circleback用）
- ツール一覧の取得（`tools/list`）→ anthropic SDK の tool 定義に変換
- ツール呼び出しの実行（`tools/call`）→ 結果の返却
- 複数サーバーの同時管理（サーバー名でルーティング）

**Interfaces**:
- Input: `MCPServerConfig`、ツール呼び出しリクエスト
- Output: ツール定義リスト、ツール呼び出し結果

---

## C3: AgentLoop (`agent_loop.py`)

**Purpose**: anthropic Python SDK を使ったエージェントループの実行

**Responsibilities**:
- Claude API へのメッセージ送信（system prompt + user message）
- tool_use レスポンスの検出とMCPClientManagerへの転送
- ツール結果をtool_resultとしてAPIに返送
- ループの終了判定（end_turn, max_turns, stop_reason）
- トークン使用量のトラッキングとコスト制限

**Interfaces**:
- Input: system prompt（str）、user message（str）、ツール定義リスト、コスト制限
- Output: 最終レスポンス（str）、トークン使用量

---

## C4: SyncStateManager (`sync_state.py`)

**Purpose**: `_sync-state.json` の読み書きとバリデーション

**Responsibilities**:
- 同期状態ファイルの読み込み（存在しない場合はデフォルト生成）
- JSON構文バリデーション
- 未来日チェック（ハルシネーション検出）
- 同期状態の更新と書き出し
- 事前・事後のバリデーション比較（LLM破損検出）

**Interfaces**:
- Input: `_sync-state.json` ファイルパス
- Output: `SyncState` データ、バリデーション結果

---

## C5: SyncOrchestrator (`sync_agent.py`)

**Purpose**: 全同期タスクの順次実行を制御するエントリポイント

**Responsibilities**:
- コマンドライン引数の解析（実行対象タスクの選択、方式切替）
- 同期タスクの順次実行
- タスク間のエラー隔離（1タスク失敗が他に影響しない）
- ログ管理（`logs/` ディレクトリへの出力）
- 実行結果のサマリー出力
- git-sync-helper.sh の呼び出し（commit & push）

**Interfaces**:
- Input: CLI引数（タスク選択、ログパス等）
- Output: 実行ログ、終了コード
