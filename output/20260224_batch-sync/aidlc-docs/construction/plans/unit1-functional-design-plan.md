# Functional Design Plan - Unit 1: Agent SDK Core

## Checklist

- [x] エージェント実行フローのビジネスロジック設計
- [x] MCP統合のデータフロー設計
- [x] 同期状態管理のビジネスルール設計
- [x] エラーハンドリングシナリオ設計
- [x] ドメインエンティティ定義

## Design Questions

既存プロンプト（sync-ga.md等）がビジネスロジック本体を定義しているため、Agent SDK固有の実行制御ロジックに関する質問のみ。

### Question 1
Agent SDK版でLLMが直接ファイル操作（Read/Write/Edit）をする仕組みはどうしますか？

既存の claude -p 版では Claude Code が Read/Write/Edit ツールを内蔵しています。Agent SDK版ではこれらが使えません。

A) LLMにファイル操作をさせず、Pythonコードでファイル操作を行う（LLMはデータの取得・変換のみ担当し、ファイル書き出しはPythonで制御）
B) カスタムツールとしてファイル操作を実装し、LLMに tool_use で呼ばせる（Claude Code と同様のアプローチ）
C) MCP File System サーバーを追加して、ファイル操作をMCP経由で行う
D) Other (please describe after [Answer]: tag below)

[Answer]:B
