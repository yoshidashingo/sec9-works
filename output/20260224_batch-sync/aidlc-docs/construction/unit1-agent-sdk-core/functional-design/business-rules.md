# Business Rules - Unit 1: Agent SDK Core

## BR-1: コスト制御ルール

### BR-1.1: タスク別コスト上限

| Task | max_cost_usd | max_turns | Model |
|------|-------------|-----------|-------|
| meetings-ga | 1.00 | 50 | claude-sonnet-4-20250514 |
| meetings-sec9 | 1.00 | 50 | claude-sonnet-4-20250514 |
| paulo | 0.50 | 15 | claude-sonnet-4-20250514 |
| market-hack | 0.50 | 15 | claude-sonnet-4-20250514 |

既存 claude -p 版の `--max-budget-usd` / `--max-turns` と同一値。

### BR-1.2: コスト推定ロジック

```
estimated_cost = (input_tokens * input_price + output_tokens * output_price) / 1_000_000

# Sonnet 4 pricing (2026-02 時点)
input_price = 3.00   # per 1M tokens
output_price = 15.00  # per 1M tokens
```

### BR-1.3: コスト超過時の動作

- エージェントループを即座に中断
- 最後のテキストレスポンスを最終結果として扱う
- ログに `COST_EXCEEDED` を記録
- タスク自体は「部分的成功」として扱い、_sync-state.json の更新はLLMが行った分まで有効

---

## BR-2: sync-state バリデーションルール

### BR-2.1: 事前バリデーション

タスク実行前に `_sync-state.json` を検証:

1. **JSON構文チェック**: パースできなければエラー → タスクスキップ
2. **未来日チェック**: `last_sync_date` or `last_sync` が今日より未来ならエラー → タスクスキップ
3. **ファイル不在**: 正常（初回実行）→ デフォルト値で続行

### BR-2.2: 事後バリデーション

エージェントループ完了後に `_sync-state.json` を再検証:

1. **JSON構文チェック**: パースできなければ → バックアップから復元
2. **未来日チェック**: 未来日なら → バックアップから復元
3. **正常**: そのまま続行

### BR-2.3: バックアップ/復元

- タスク実行前にメモリ上にバックアップ（ファイルコピーではなく辞書保持）
- 事後バリデーション失敗時にバックアップから Write で復元
- 復元したことをログに記録

---

## BR-3: エラー隔離ルール

### BR-3.1: タスク間隔離

- 1つのタスクが失敗しても、他のタスクは実行を継続する
- 各タスクは独立した try/except ブロックで実行
- 失敗タスクはサマリーに記録

### BR-3.2: MCP接続エラー

- サーバー接続失敗: 当該タスクをスキップ、次のタスクへ
- ツール呼び出し失敗: エラーメッセージを tool_result として返し、LLMに判断させる
- サーバープロセスクラッシュ: 当該タスクを中断、MCP接続をクリーンアップ

### BR-3.3: Claude API エラー

- 429 (Rate Limit): 指数バックオフで最大3回リトライ
- 500/502/503 (Server Error): 指数バックオフで最大3回リトライ
- 400 (Bad Request): 即座にエラー、タスクスキップ
- 認証エラー: 即座にエラー、全タスク中断

---

## BR-4: セキュリティルール

### BR-4.1: ファイルアクセス制限

ローカルツール（Read/Write/Edit/Glob）は以下の制約を持つ:

- **許可パス**: `REPO_DIR`（/Users/shingo/Documents/GitHub/assessment）配下のみ
- **禁止パス**: `REPO_DIR` 外、シンボリックリンクによる脱出
- **禁止パターン**: `.env`, `credentials`, `secrets` を含むファイルへの書き込み

### BR-4.2: MCP企業分離

- 各タスクは定義されたMCPサーバーのみに接続
- meetings-ga: tldv-ga のみ
- meetings-sec9: circleback のみ
- paulo / market-hack: google-workspace-sec9 のみ

### BR-4.3: APIキー管理

- ANTHROPIC_API_KEY: 環境変数から取得
- MCPサーバーの認証情報: `.mcp.json` の env セクションから取得（コードにハードコードしない）

---

## BR-5: ログ記録ルール

### BR-5.1: ログ出力先

- ファイル: `logs/sync-agent-sdk_{YYYYMMDD_HHMMSS}.log`
- 形式: `[{ISO8601 timestamp}] {level} {message}`

### BR-5.2: ログレベル

- **INFO**: タスク開始/完了、同期件数、トークン使用量
- **WARNING**: タスク部分成功、コスト超過、sync-state復元
- **ERROR**: タスク失敗、MCP接続エラー、API エラー

### BR-5.3: ログ保持

- 30日以上前のログファイルを自動削除（既存パターン踏襲）
