# Business Logic Model - Unit 1: Agent SDK Core

## 1. Agent Execution Flow

Agent SDK版の中核ビジネスロジック。既存プロンプトファイルを system prompt として使い、Claude API のエージェントループで同期処理を実行する。

### 1.1 Main Execution Flow

```
sync_agent.py main()
  |
  +-- parse CLI args (--tasks, --log-dir, --dry-run, --no-git)
  |
  +-- for each task in tasks:
  |     |
  |     +-- [1] load_sync_state(state_path)
  |     |     +-- validate (JSON parse, future date check)
  |     |     +-- backup current state
  |     |
  |     +-- [2] load_mcp_config(".mcp.json")
  |     |     +-- filter to task-required servers only
  |     |
  |     +-- [3] connect MCP servers (async)
  |     |     +-- stdio: subprocess spawn + MCP handshake
  |     |     +-- http: HTTP connection + MCP handshake
  |     |
  |     +-- [4] collect tools
  |     |     +-- MCP tools: list_tools() from each server
  |     |     +-- Local tools: Read, Write, Edit, Glob
  |     |     +-- merge into unified tool list
  |     |
  |     +-- [5] run agent loop
  |     |     +-- system_prompt = read(prompt_file)
  |     |     +-- user_message = "同期処理を実行してください"
  |     |     +-- loop: messages.create -> tool_use -> tool_result -> ...
  |     |     +-- exit: end_turn / max_turns / cost limit
  |     |
  |     +-- [6] post-validation
  |     |     +-- reload _sync-state.json
  |     |     +-- validate (JSON parse, future date check)
  |     |     +-- if invalid: restore backup
  |     |
  |     +-- [7] disconnect MCP servers
  |     +-- [8] log result (success/failure, tokens used, turns)
  |
  +-- if not --no-git: git_commit_push()
  +-- print summary
```

### 1.2 Agent Loop Detail

```
agent_loop.run(system_prompt, user_message):
  messages = [{"role": "user", "content": user_message}]
  total_input_tokens = 0
  total_output_tokens = 0
  turns = 0

  while turns < max_turns:
    response = client.messages.create(
      model=model,
      system=system_prompt,
      messages=messages,
      tools=all_tools,        # MCP tools + local tools
      max_tokens=4096
    )

    total_input_tokens += response.usage.input_tokens
    total_output_tokens += response.usage.output_tokens
    turns += 1

    # cost check
    if estimated_cost(total_input_tokens, total_output_tokens) > max_cost:
      break with cost_exceeded

    # tool_use handling
    tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
    if not tool_use_blocks:
      # no tool calls = done
      break with final text

    # process each tool call
    tool_results = []
    for tool_use in tool_use_blocks:
      if is_local_tool(tool_use.name):
        result = execute_local_tool(tool_use.name, tool_use.input)
      else:
        result = await mcp.call_tool(tool_use.name, tool_use.input)
      tool_results.append({"tool_use_id": tool_use.id, "content": result})

    # append assistant response + tool results to messages
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

  return AgentResult(...)
```

### 1.3 Tool Routing Logic

ツール呼び出しのルーティング:

```
tool_use.name
  |
  +-- "Read" / "Write" / "Edit" / "Glob" --> Local Tool Handler
  |
  +-- MCP tool name --> MCPClientManager
        |
        +-- tool_name_to_server_map[name] --> specific MCP server
        +-- server.call_tool(name, arguments)
```

**ツール名の一意性保証:**
- ローカルツール名（Read, Write, Edit, Glob）はMCPツール名と衝突しない（MCPツールは通常 snake_case でプレフィックス付き）
- 同一タスク内で接続するMCPサーバー間でツール名が重複する場合はエラー（実運用では発生しない）

---

## 2. Local Tool Implementations

LLM が tool_use で呼び出すカスタムツール。Claude Code の Read/Write/Edit/Glob と同等の機能を提供。

### 2.1 Read Tool

```
name: "Read"
input_schema:
  file_path: string (required) - 読み込むファイルの絶対パス
  offset: integer (optional) - 開始行番号
  limit: integer (optional) - 読み込む行数

logic:
  1. file_path の存在チェック
  2. セキュリティチェック: REPO_DIR 配下のみ許可
  3. ファイル読み込み（offset/limit対応）
  4. 行番号付きで返却（cat -n 形式）
```

### 2.2 Write Tool

```
name: "Write"
input_schema:
  file_path: string (required) - 書き込むファイルの絶対パス
  content: string (required) - 書き込む内容

logic:
  1. セキュリティチェック: REPO_DIR 配下のみ許可
  2. 親ディレクトリが存在しなければ作成
  3. ファイルに content を書き込み（上書き）
  4. 結果メッセージを返却
```

### 2.3 Edit Tool

```
name: "Edit"
input_schema:
  file_path: string (required) - 編集するファイルの絶対パス
  old_string: string (required) - 置換対象の文字列
  new_string: string (required) - 置換後の文字列

logic:
  1. セキュリティチェック: REPO_DIR 配下のみ許可
  2. ファイル読み込み
  3. old_string の出現箇所を検索
  4. 一意でなければエラー（複数箇所にマッチ）
  5. old_string を new_string に置換
  6. ファイル書き込み
  7. 結果メッセージを返却
```

### 2.4 Glob Tool

```
name: "Glob"
input_schema:
  pattern: string (required) - globパターン
  path: string (optional) - 検索ディレクトリ

logic:
  1. セキュリティチェック: REPO_DIR 配下のみ許可
  2. pathlib.Path.glob() でマッチするファイルを検索
  3. マッチしたファイルパスのリストを返却
```

---

## 3. MCP Connection Flow

### 3.1 stdio型サーバー接続

```
connect_stdio(config):
  1. env = {**os.environ, **config.env}  # マージ
  2. process = subprocess.Popen(
       [config.command] + config.args,
       stdin=PIPE, stdout=PIPE, stderr=PIPE,
       env=env
     )
  3. transport = StdioClientTransport(process.stdin, process.stdout)
  4. session = ClientSession(transport)
  5. await session.initialize()
  6. tools = await session.list_tools()
  7. return (session, process, tools)
```

### 3.2 HTTP型サーバー接続（circleback）

```
connect_http(config):
  1. transport = StreamableHTTPClientTransport(url=config.url)
  2. session = ClientSession(transport)
  3. await session.initialize()
  4. tools = await session.list_tools()
  5. return (session, None, tools)
```

### 3.3 ツール形式変換

MCP tools → anthropic SDK tools:

```
convert_mcp_tool_to_anthropic(mcp_tool):
  return {
    "name": mcp_tool.name,
    "description": mcp_tool.description,
    "input_schema": mcp_tool.inputSchema  # JSON Schema そのまま
  }
```
