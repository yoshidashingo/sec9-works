# TLDV-02. LangChain Community VIPs: Call with OSS and LangSmith Teams

- **日時**: 2025-10-02 15:00 UTC
- **参加者**: Sydney Runkle (LangChain), Chester, Mason, Eugene, 吉田真吾, 西見公宏, Colin McNamara, Gal Peretz 他
- **重要度**: ★★★
- **関連章**: 第3章, 第4章, 第5章

## 概要

Middleware（ミドルウェア）とContext Engineering（コンテキストエンジニアリング）の具体的な技術議論が行われたミーティング。ガードレールの実装パターンについても議論あり。

---

## Middleware と Context Engineering

### Sydney Runkle（LangChainオープンソースエンジニア）

Middlewareの概念とContext Engineeringの関係を明確に説明:

> "it also exposes another core hook, which we're calling modify model request. And that is really critical in the **context engineering** space. Modifying your model request allows you to change basically anything under the sun related to the upcoming LLM call. So that's like your model, your tools, your prompt or your system prompt, your message history, your model settings."

- **modify model request** フックがcontext engineeringの中核
- 変更可能な項目:
  - モデル
  - ツール
  - システムプロンプト
  - メッセージ履歴
  - モデル設定
- **プリビルトmiddlewares**:
  - human-in-the-loop
  - summarization
  - planning/todoパターン
  - file systemパターン

## Guardrails（ガードレール）に関する議論

### Colin McNamara
- guardrails をmiddleware で実装し、abuse（悪用）検出のための統計的プロセス制御として活用する提案
- 「you got guardrails on the agent maybe you're using middleware to establish a guardrail」
- セキュリティ・anti-abuseレポートとしてのInsights機能の活用を提案

## エージェントフレームワークの進化

- `create_react_agent` から `create_agent` + middleware パターンへの移行
- Deep Agents ライブラリのリリースとmiddlewareとしての機能提供

### Gal Peretz
- ShadCN的アプローチ（コードを直接取得してカスタマイズ）vs middleware パターンの議論
- どちらが開発者体験として優れているかのトレードオフ
