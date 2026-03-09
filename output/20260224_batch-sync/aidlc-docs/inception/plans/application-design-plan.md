# Application Design Plan - 情報同期バッチ処理（2方式）

## Design Plan Checklist

- [x] コンポーネント識別と責務定義
- [x] コンポーネントメソッド定義
- [x] サービス層設計（オーケストレーション）
- [x] コンポーネント依存関係マッピング
- [x] 設計の整合性検証

---

## Design Questions

既存のclaude -p版パターンとAgent SDK版の設計について、いくつか確認が必要です。

### Question 1
Agent SDK版のプロンプト管理方針は？

既存のclaude -p版は `scripts/prompts/sync-*.md` にプロンプトファイルを持ち、`claude -p "$(cat "$PROMPT_FILE")"` で渡しています。Agent SDK版はどうしますか？

A) 同じプロンプトファイルを共用する（DRY原則優先。Agent SDK版も同じmdファイルを読み込んでsystem promptとして使う）
B) Agent SDK版は専用のプロンプトを持つ（SDK版に最適化した指示を書ける。タスク定義をPythonコード内に埋め込む）
C) 共通部分はプロンプトファイルで共有し、SDK固有の追加指示だけPythonコードに持つ（ハイブリッド）
D) Other (please describe after [Answer]: tag below)

[Answer]:A

### Question 2
Pythonプロジェクトの構成は？

A) フラットスクリプト（`scripts/agent-sdk/` に.pyファイルを配置。pipで依存関係管理。シンプル優先）
B) Pythonパッケージ（`scripts/agent-sdk/` にpyproject.toml + src構成。テスト容易性・再利用性優先）
C) リポジトリルートにPythonパッケージ（`agent_sync/` として独立パッケージ化）
D) Other (please describe after [Answer]: tag below)

[Answer]:A

### Question 3
MCPサーバー設定の管理方法は？

Agent SDK版からMCPサーバーに接続するには、サーバーの起動コマンドと引数が必要です。

A) 既存の `.claude/` 設定ファイルを解析して自動取得する（Claude Code設定と常に同期）
B) Agent SDK版専用の設定ファイルを作る（例: `scripts/agent-sdk/mcp-config.json`。独立管理で安定）
C) Pythonコード内にハードコードする（最もシンプル。サーバー数が少ないため管理可能）
D) Other (please describe after [Answer]: tag below)

[Answer]:A
