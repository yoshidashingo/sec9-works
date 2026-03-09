# Unit of Work Dependencies

## Dependency Matrix

| Unit | Depends On | Type | Notes |
|------|-----------|------|-------|
| Unit 1: Agent SDK Core | (external) anthropic, mcp packages | Build-time | pip install |
| Unit 1: Agent SDK Core | scripts/prompts/*.md | Runtime | 既存プロンプトファイル共用 |
| Unit 1: Agent SDK Core | .mcp.json | Runtime | MCPサーバー設定の読み込み |
| Unit 1: Agent SDK Core | output/**/_sync-state.json | Runtime | 同期状態の読み書き |
| Unit 2: Orchestration | Unit 1: Agent SDK Core | Runtime | Python スクリプトの呼び出し |
| Unit 2: Orchestration | scripts/git-sync-helper.sh | Runtime | git操作 |

## Implementation Order

```
Unit 1: Agent SDK Core
  |
  v
Unit 2: Orchestration & Cron Integration
```

**Critical Path**: Unit 1 → Unit 2（厳密な順序依存）

Unit 2 は Unit 1 の `sync_agent.py` を呼び出すため、Unit 1 が完成しテスト済みでなければ Unit 2 の実装に進めない。

## Integration Points

| Integration Point | Unit 1 | Unit 2 |
|-------------------|--------|--------|
| Python実行 | sync_agent.py を提供 | subprocess で呼び出し |
| ログ出力 | stdout/stderr に出力 | ファイルにリダイレクト |
| 終了コード | 0=成功, 1=失敗 | 終了コードで成否判定 |
| git操作 | --no-git フラグで抑制 | git-sync-helper.sh を呼び出し |
