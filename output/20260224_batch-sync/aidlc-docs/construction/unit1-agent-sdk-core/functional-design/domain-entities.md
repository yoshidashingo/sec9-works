# Domain Entities - Unit 1: Agent SDK Core

## Entity Relationship

```
MCPServerConfig ----< MCPClientManager >---- ClientSession
                                                   |
                                              Tool (MCP)
                                                   |
AgentLoop --------< ToolRegistry >---------- Tool (Local)
    |
    +--- AgentResult
    |
    +--- CostTracker

SyncTask ----< SyncOrchestrator
    |
    +--- SyncState
    +--- TaskResult
```

---

## E1: MCPServerConfig

MCPサーバーの接続設定を表すデータ構造。

```python
@dataclass
class MCPServerConfig:
    name: str                       # サーバー名（例: "tldv-ga"）
    transport: str                  # "stdio" | "http"
    command: str | None = None      # stdio: 実行コマンド
    args: list[str] = field(default_factory=list)  # stdio: コマンド引数
    env: dict[str, str] = field(default_factory=dict)  # stdio: 環境変数
    url: str | None = None          # http: エンドポイントURL
```

---

## E2: AgentResult

エージェントループの実行結果。

```python
@dataclass
class AgentResult:
    final_response: str             # 最終テキストレスポンス
    total_input_tokens: int         # 合計入力トークン数
    total_output_tokens: int        # 合計出力トークン数
    turns_used: int                 # 使用ターン数
    tools_called: list[str]         # 呼び出されたツール名リスト
    stop_reason: str                # "end_turn" | "max_turns" | "cost_exceeded"
    estimated_cost_usd: float       # 推定コスト（USD）
```

---

## E3: SyncState

増分同期の状態を表すデータ構造。

```python
@dataclass
class SyncState:
    last_sync_date: str             # "YYYY/MM/DD" or ISO 8601
    synced_ids: list[str]           # synced_meeting_ids or synced_message_ids
    provider: str                   # "tldv" | "circleback" | "gmail-sec9"
```

`_sync-state.json` との対応:
- meetings: `{"last_sync": "...", "synced_meeting_ids": [...], "provider": "tldv"}`
- articles: `{"last_sync_date": "...", "synced_message_ids": [...], "provider": "gmail-sec9"}`

---

## E4: SyncTask

同期タスクの定義。各データソースに1つ。

```python
@dataclass
class SyncTask:
    name: str                       # タスク名（例: "meetings-ga"）
    prompt_path: str                # プロンプトファイルパス
    mcp_servers: list[str]          # 必要なMCPサーバー名リスト
    state_path: str                 # _sync-state.json パス
    output_paths: list[str]         # git add 対象パス
    max_cost_usd: float             # コスト上限
    max_turns: int                  # ターン上限
    model: str                      # 使用モデル
```

**定義済みタスク:**

```python
SYNC_TASKS = {
    "meetings-ga": SyncTask(
        name="meetings-ga",
        prompt_path="scripts/prompts/sync-ga.md",
        mcp_servers=["tldv-ga"],
        state_path="output/ga/meetings/_sync-state.json",
        output_paths=["output/ga/meetings/"],
        max_cost_usd=1.00,
        max_turns=50,
        model="claude-sonnet-4-20250514",
    ),
    "meetings-sec9": SyncTask(
        name="meetings-sec9",
        prompt_path="scripts/prompts/sync-sec9.md",
        mcp_servers=["circleback"],
        state_path="output/sec9/meetings/_sync-state.json",
        output_paths=["output/sec9/meetings/"],
        max_cost_usd=1.00,
        max_turns=50,
        model="claude-sonnet-4-20250514",
    ),
    "paulo": SyncTask(
        name="paulo",
        prompt_path="scripts/prompts/sync-paulo.md",
        mcp_servers=["google-workspace-sec9"],
        state_path="output/shingo/paulo-newsletter/references/_sync-state.json",
        output_paths=["output/shingo/paulo-newsletter/"],
        max_cost_usd=0.50,
        max_turns=15,
        model="claude-sonnet-4-20250514",
    ),
    "market-hack": SyncTask(
        name="market-hack",
        prompt_path="scripts/prompts/sync-market-hack.md",
        mcp_servers=["google-workspace-sec9"],
        state_path="output/shingo/market-hack-magazine/references/_sync-state.json",
        output_paths=["output/shingo/market-hack-magazine/"],
        max_cost_usd=0.50,
        max_turns=15,
        model="claude-sonnet-4-20250514",
    ),
}
```

---

## E5: TaskResult

個別タスクの実行結果。

```python
@dataclass
class TaskResult:
    task_name: str
    success: bool
    agent_result: AgentResult | None  # 成功時のみ
    error: str | None                 # 失敗時のエラーメッセージ
    state_restored: bool              # sync-state の復元が行われたか
    duration_seconds: float           # 実行時間
```

---

## E6: CostTracker

コスト追跡。AgentLoop 内部で使用。

```python
@dataclass
class CostTracker:
    input_tokens: int = 0
    output_tokens: int = 0
    input_price_per_m: float = 3.00    # USD per 1M tokens
    output_price_per_m: float = 15.00  # USD per 1M tokens
    max_cost_usd: float = 1.00

    @property
    def estimated_cost(self) -> float:
        return (self.input_tokens * self.input_price_per_m +
                self.output_tokens * self.output_price_per_m) / 1_000_000

    @property
    def exceeded(self) -> bool:
        return self.estimated_cost > self.max_cost_usd
```
