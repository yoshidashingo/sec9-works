# Component Methods - 情報同期バッチ処理（Agent SDK版）

## C1: MCPConfigLoader

```python
class MCPServerConfig:
    name: str
    transport: Literal["stdio", "http"]
    # stdio
    command: str | None
    args: list[str]
    env: dict[str, str]
    # http
    url: str | None

def load_mcp_config(config_path: str) -> dict[str, MCPServerConfig]
    """
    .mcp.json を読み込み、サーバー名→設定の辞書を返す。
    stdio型（command + args）とHTTP型（url）を自動判別。
    """

def filter_servers(configs: dict[str, MCPServerConfig], names: list[str]) -> dict[str, MCPServerConfig]
    """指定されたサーバー名のみにフィルタリング"""
```

## C2: MCPClientManager

```python
class MCPClientManager:
    async def connect(self, config: MCPServerConfig) -> None
        """MCPサーバーに接続（stdio: subprocess起動、http: HTTP接続）"""

    async def disconnect(self) -> None
        """全MCPサーバーとの接続を切断・プロセス終了"""

    async def list_tools(self) -> list[dict]
        """接続中の全サーバーからツール一覧を取得し、anthropic SDK形式に変換"""

    async def call_tool(self, tool_name: str, arguments: dict) -> str
        """ツール名からサーバーを特定し、ツールを呼び出す。結果を文字列で返す"""

    def get_anthropic_tools(self) -> list[dict]
        """anthropic SDK の messages API に渡す tools パラメータ形式で返す"""
```

## C3: AgentLoop

```python
class AgentLoop:
    def __init__(self, client: anthropic.Anthropic, mcp: MCPClientManager,
                 model: str = "claude-sonnet-4-20250514",
                 max_turns: int = 15, max_tokens_total: int = 100000)

    async def run(self, system_prompt: str, user_message: str) -> AgentResult
        """
        エージェントループを実行。
        1. system + user message を送信
        2. tool_use があれば MCPClientManager 経由で実行
        3. tool_result を返送してループ
        4. end_turn または max_turns で終了
        """

class AgentResult:
    final_response: str
    total_input_tokens: int
    total_output_tokens: int
    turns_used: int
    tools_called: list[str]
```

## C4: SyncStateManager

```python
class SyncState:
    last_sync_date: str  # "YYYY/MM/DD" or ISO 8601
    synced_ids: list[str]  # synced_meeting_ids or synced_message_ids
    provider: str

def load_sync_state(state_path: str, default: SyncState) -> SyncState
    """_sync-state.json を読み込む。存在しない場合はdefaultを返す"""

def validate_sync_state(state: SyncState) -> tuple[bool, str | None]
    """バリデーション。未来日チェック等。(ok, error_message)"""

def save_sync_state(state_path: str, state: SyncState) -> None
    """_sync-state.json に書き出す"""

def backup_and_restore(state_path: str) -> contextmanager
    """事前にバックアップし、バリデーション失敗時に復元するコンテキストマネージャ"""
```

## C5: SyncOrchestrator

```python
def main() -> int
    """
    CLI エントリポイント。
    argparse で以下を受け付ける:
      --tasks: 実行するタスク名のリスト（all, meetings-ga, meetings-sec9, paulo, market-hack）
      --log-dir: ログ出力先（default: logs/）
      --dry-run: 実際のAPIコールを行わずにログだけ出力
      --no-git: git commit & push をスキップ
    """

async def run_sync_task(task_name: str, prompt_path: str,
                        mcp_servers: list[str], state_path: str,
                        output_paths: list[str], agent_loop: AgentLoop) -> bool
    """
    個別同期タスクの実行。
    1. SyncStateManager で事前バリデーション
    2. MCPClientManager で必要なサーバーに接続
    3. AgentLoop でプロンプト実行
    4. SyncStateManager で事後バリデーション
    5. 成功/失敗を返す
    """

def git_commit_push(output_paths: list[str], commit_msg: str, log_file: str) -> bool
    """git-sync-helper.sh を subprocess で呼び出す"""
```
