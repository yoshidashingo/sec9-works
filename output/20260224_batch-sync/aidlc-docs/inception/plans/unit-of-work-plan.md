# Unit of Work Plan - 情報同期バッチ処理（2方式）

## Decomposition Checklist

- [x] ユニット定義と責務の決定
- [x] ユニット間依存関係の分析
- [x] 要件→ユニットのマッピング
- [x] コード配置戦略の決定
- [x] ユニット境界の検証

## Decomposition Strategy

Application Design で設計した5コンポーネントを2つのユニットに分割する。

**分割の基準:**
- Unit 1 は Agent SDK の新規 Python コードすべて（ビジネスロジックの実装）
- Unit 2 は既存インフラとの統合（シェルスクリプト、cron設定）

**依存関係:**
- Unit 2 は Unit 1 の完成を前提とする（Unit 1 の Python コードを呼び出す）
- Unit 1 は既存の共有リソース（prompts/*.md, .mcp.json, _sync-state.json）に依存

## Code Organization (Greenfield)

```
scripts/
  agent-sdk/                    ← Unit 1: Agent SDK Core
    sync_agent.py               ← エントリポイント (C5: SyncOrchestrator)
    mcp_config.py               ← C1: MCPConfigLoader
    mcp_client.py               ← C2: MCPClientManager
    agent_loop.py               ← C3: AgentLoop
    sync_state.py               ← C4: SyncStateManager
    requirements.txt            ← Python依存関係
    tests/                      ← ユニットテスト
      test_mcp_config.py
      test_sync_state.py
      test_agent_loop.py
  sync-agent-sdk-cron.sh        ← Unit 2: cron wrapper for Agent SDK
  sync-all-cron.sh              ← Unit 2: 既存更新（Agent SDK版の追加）
```
