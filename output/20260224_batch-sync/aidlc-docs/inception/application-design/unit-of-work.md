# Unit of Work Definitions

## Unit 1: Agent SDK Core

**Type**: Module（Pythonスクリプト群）

**Description**: anthropic Python SDK + MCP Python SDK を使用した情報同期バッチ処理の実装。既存の claude -p 版と同じデータソースに対して、プログラマティックなエージェントとして同期を実行する。

**Components**:
- C1: MCPConfigLoader (`mcp_config.py`)
- C2: MCPClientManager (`mcp_client.py`)
- C3: AgentLoop (`agent_loop.py`)
- C4: SyncStateManager (`sync_state.py`)
- C5: SyncOrchestrator (`sync_agent.py`) — エントリポイント

**Responsibilities**:
- `.mcp.json` からMCPサーバー設定を読み込み
- MCPサーバーへの接続・ツール呼び出し（stdio/HTTP）
- anthropic SDK によるエージェントループ実行（tool_use中継）
- `_sync-state.json` の管理・バリデーション・ハルシネーション検出
- 4つの同期タスクの順次実行（meetings-ga, meetings-sec9, paulo, market-hack）
- ログ出力、エラー隔離

**Shared Resources** (read-only):
- `scripts/prompts/sync-*.md` — プロンプトファイル
- `.mcp.json` — MCPサーバー設定

**Shared Resources** (read-write):
- `output/**/\_sync-state.json` — 同期状態ファイル
- `output/**/*.md` — 同期結果ファイル

**Code Location**: `scripts/agent-sdk/`

**Dependencies**: anthropic, mcp (Python packages)

---

## Unit 2: Orchestration & Cron Integration

**Type**: Module（シェルスクリプト）

**Description**: Agent SDK版をcronジョブとして統合するためのラッパースクリプト。既存の `sync-all-cron.sh` を更新し、claude -p版とAgent SDK版を切り替えて実行できるようにする。

**Components**:
- cron wrapper script (`sync-agent-sdk-cron.sh`)
- `sync-all-cron.sh` の更新

**Responsibilities**:
- Agent SDK版 Python スクリプトの実行環境設定（PATH, venv等）
- ログファイル管理
- プロセスロック（既存 `/tmp/assessment-sync-all.lock` と共存）
- `sync-all-cron.sh` の方式切替機構（環境変数またはフラグで claude -p / Agent SDK を選択）
- git-sync-helper.sh の呼び出し

**Shared Resources**:
- `scripts/git-sync-helper.sh` — git操作ヘルパー
- `logs/` — ログディレクトリ

**Code Location**: `scripts/`

**Dependencies**: Unit 1 (Agent SDK Core)
