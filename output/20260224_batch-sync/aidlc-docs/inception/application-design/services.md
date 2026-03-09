# Services - 情報同期バッチ処理（Agent SDK版）

## Service Architecture

Agent SDK版は以下のサービス層で構成される。

```
+------------------------------------------------------------------+
|  SyncOrchestrator (sync_agent.py)                                |
|  - タスク選択・順次実行・ログ・git操作                              |
+------------------------------------------------------------------+
       |              |              |              |
       v              v              v              v
+------------+ +------------+ +------------+ +------------+
| meetings   | | meetings   | |  paulo     | | market     |
| GA (tldv)  | | Sec9 (cb)  | | (gmail)    | | hack       |
+------------+ +------------+ +------------+ +------------+
       |              |              |              |
       v              v              v              v
+------------------------------------------------------------------+
|  AgentLoop (agent_loop.py)                                       |
|  - anthropic SDK messages API + tool_use ループ                   |
+------------------------------------------------------------------+
       |                                      ^
       v                                      |
+------------------------------------------------------------------+
|  MCPClientManager (mcp_client.py)                                |
|  - MCP接続管理・ツール呼び出し・サーバールーティング                  |
+------------------------------------------------------------------+
       |              |              |              |
       v              v              v              v
  [tldv-ga]    [circleback]   [gws-sec9]     [gws-ga]
  (stdio)      (http)         (stdio)        (stdio)
```

---

## S1: Sync Orchestration Service

**Provided by**: `SyncOrchestrator` (sync_agent.py)

**Responsibilities**:
- 全同期タスクのライフサイクル管理
- タスク間のエラー隔離
- 統一的なログ出力

**Orchestration Flow**:

```
1. CLI引数解析 → 実行対象タスクの決定
2. ログファイル初期化
3. for each task:
   a. SyncStateManager.load → 事前バリデーション
   b. MCPConfigLoader → 必要なサーバー設定取得
   c. MCPClientManager.connect → サーバー接続
   d. AgentLoop.run → プロンプト実行（同期処理本体）
   e. SyncStateManager.validate → 事後バリデーション（失敗時restore）
   f. MCPClientManager.disconnect → サーバー切断
   g. エラーハンドリング（失敗しても次のタスクへ）
4. git_commit_push → 変更をcommit & push
5. 実行サマリー出力
```

---

## S2: Agent Execution Service

**Provided by**: `AgentLoop` (agent_loop.py)

**Responsibilities**:
- Claude API との通信
- tool_use → MCP tool call の中継
- トークン管理とコスト制限

**Execution Pattern**:

```
1. messages.create(system=prompt, user=message, tools=mcp_tools)
2. while response has tool_use:
   a. for each tool_use block:
      - MCPClientManager.call_tool(name, arguments)
      - 結果を tool_result に格納
   b. messages.create(tool_results)
   c. turns += 1
   d. if turns >= max_turns: break
3. return final text response + usage stats
```

---

## S3: MCP Connection Service

**Provided by**: `MCPClientManager` (mcp_client.py)

**Responsibilities**:
- MCPサーバープロセスの起動・管理
- ツール名 → サーバーのルーティング
- 接続のクリーンアップ

**Connection Management**:

```
connect(config):
  if config.transport == "stdio":
    - subprocess で command + args を起動
    - stdin/stdout で MCP プロトコル通信
    - mcp.ClientSession で接続
  elif config.transport == "http":
    - StreamableHTTP transport で接続
    - mcp.ClientSession で接続

disconnect():
  - 全 ClientSession を close
  - 全 subprocess を terminate
```

**Tool Routing**:
- 各サーバーのツール一覧取得時にプレフィックス付与なし（元のツール名をそのまま使用）
- ツール名からサーバーを逆引きするマッピングテーブルを内部保持
- 同名ツールが複数サーバーに存在する場合はconnect時にエラー（同期タスクごとに必要なサーバーのみ接続するため、実質的に発生しない）

---

## S4: Sync State Service

**Provided by**: `SyncStateManager` (sync_state.py)

**Responsibilities**:
- 増分同期のための状態管理
- LLMハルシネーションの検出・復旧

**State Management Pattern**:

```
with backup_and_restore(state_path):
  state = load_sync_state(state_path, default)
  ok, err = validate_sync_state(state)
  if not ok: raise
  # ... AgentLoop が state ファイルを更新 ...
  state_after = load_sync_state(state_path, default)
  ok, err = validate_sync_state(state_after)
  if not ok: raise  # → backup_and_restore が自動復元
```
