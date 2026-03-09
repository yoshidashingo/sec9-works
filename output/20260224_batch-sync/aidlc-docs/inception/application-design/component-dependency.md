# Component Dependencies - 情報同期バッチ処理（Agent SDK版）

## Dependency Matrix

| Component | Depends On | Depended By |
|-----------|-----------|-------------|
| C1: MCPConfigLoader | (none) | C2, C5 |
| C2: MCPClientManager | C1 (config) | C3, C5 |
| C3: AgentLoop | C2 (tool calls), anthropic SDK | C5 |
| C4: SyncStateManager | (none) | C5 |
| C5: SyncOrchestrator | C1, C2, C3, C4, git-sync-helper.sh | (entry point) |

---

## Data Flow Diagram

```
+------------------+
|  .mcp.json       |---> [C1: MCPConfigLoader] ---> server configs
+------------------+                                      |
                                                          v
+------------------+     +----------------------------+
| MCP Servers      |<--->| C2: MCPClientManager       |
| - tldv-ga        |     | - connect/disconnect       |
| - circleback     |     | - list_tools -> tool defs  |
| - gws-ga         |     | - call_tool -> results     |
| - gws-sec9       |     +----------------------------+
+------------------+          ^          |
                              |          v
+------------------+     +----------------------------+
| Claude API       |<--->| C3: AgentLoop              |
| (anthropic SDK)  |     | - messages + tool_use loop |
+------------------+     +----------------------------+
                              ^
                              |
+------------------+     +----------------------------+
| prompts/*.md     |---->| C5: SyncOrchestrator       |
+------------------+     | - task selection           |
                         | - sequential execution     |
+------------------+     | - error isolation          |
| _sync-state.json |<--->| - logging                  |
+------------------+  ^  +----------------------------+
                      |          |
               [C4: SyncState   |
                Manager]        v
                         +----------------------------+
                         | git-sync-helper.sh         |
                         | - commit & push            |
                         +----------------------------+
```

---

## Communication Patterns

### C5 → C1: 設定読み込み（同期）
- SyncOrchestrator が起動時に MCPConfigLoader を呼び出す
- `.mcp.json` のパスはリポジトリルートから相対的に解決

### C5 → C2: サーバー接続管理（非同期）
- タスクごとに必要なサーバーのみ接続
- タスク完了後に切断
- async context manager パターン

### C5 → C3: エージェント実行（非同期）
- プロンプトファイルを読み込んでsystem promptとして渡す
- AgentLoop が MCPClientManager を通じてツール呼び出し

### C5 → C4: 状態管理（同期）
- タスク実行前後にバリデーション
- context manager で自動バックアップ/復元

### C3 ↔ C2: ツール呼び出し（非同期）
- AgentLoop が tool_use レスポンスを受け取り MCPClientManager に転送
- MCPClientManager がMCPプロトコルで実行し結果を返す

### C5 → git-sync-helper.sh: git操作（subprocess）
- 既存シェルスクリプトを subprocess.run で呼び出す
- ロック機構・リトライロジックは既存実装を再利用

---

## External Dependencies

### Python Packages

| Package | Purpose | Version |
|---------|---------|---------|
| anthropic | Claude API クライアント | latest stable |
| mcp | MCP Python SDK（サーバー接続） | latest stable |

### Shared Infrastructure（既存）

| Resource | Usage |
|----------|-------|
| scripts/prompts/*.md | claude -p版と共用するプロンプトファイル |
| scripts/git-sync-helper.sh | git commit & push の排他制御 |
| .mcp.json | MCPサーバー設定（Claude Code と共用） |
| output/**/\_sync-state.json | 増分同期の状態管理ファイル |

---

## Task-to-Server Mapping

各同期タスクが接続するMCPサーバー:

| Task | MCP Servers | Prompt File |
|------|------------|-------------|
| meetings-ga | tldv-ga | scripts/prompts/sync-ga.md |
| meetings-sec9 | circleback | scripts/prompts/sync-sec9.md |
| paulo | google-workspace-sec9 | scripts/prompts/sync-paulo.md |
| market-hack | google-workspace-sec9 | scripts/prompts/sync-market-hack.md |
