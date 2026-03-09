# TLDV-01. LangChain Community VIPs: Call with Harrison and OSS Team

- **日時**: 2025-12-09 16:00 UTC
- **参加者**: Harrison Chase (LangChain CEO), 吉田真吾, 西見公宏, Git Maxd, Sanjeed Mohammed, Ben McHone, Colin McNamara 他
- **重要度**: ★★★
- **関連章**: 第1章, 第3章, 第5章, 第7章

## 概要

ハーネスエンジニアリングの概念について最も直接的かつ詳細な議論が行われたミーティング。Harrison ChaseがLangChainの3層アーキテクチャ（Framework / Runtime / Harness）を定義し、Deep Agentsをエージェントハーネスとして位置づけた。

---

## Harrison Chase による3層アーキテクチャの定義

> "LangGraph, we think of as like a really low-level kind of like agent runtime. LangChain, we think of as like an agent framework, so the main value there is our abstractions. And then deep agents, we think of as like an **agent harness** on top of it."

- **LangGraph**: 低レベルのエージェントランタイム
- **LangChain**: エージェントフレームワーク（主要な価値は抽象化。1.0でmiddlewareの概念を導入）
- **Deep Agents**: その上に載るエージェントハーネス

## Deep Agents（エージェントハーネス）の詳細

Harrison Chaseによる説明:

> "deep agents, we think of as like an agent harness. We think it's really good for like longer running, more autonomous agents. So it builds on top of LangChain. It's got like built-in planning tools, sub-agents, access to a file system, those automatic kind of like summarization and compaction."

- **用途**: 長時間実行される、より自律的なエージェント向け
- **組み込み機能**:
  - planning tools（計画ツール）
  - sub-agents（サブエージェント）
  - file system access（ファイルシステムアクセス）
  - automatic summarization and compaction（自動要約・圧縮）
- **適用領域**: deep research やcoding スタイルのタスクに適しており、多くのユースケースがこの方向に向かっている
- **ロードマップ**:
  - skills（スキル）の概念追加
  - Deep Agent CLIからSDKへのロジック移行
  - code sandboxes対応
  - Anthropic以外のモデル（OpenAI、Google）への対応強化

## コミュニティからの評価

### Git Maxd（コミュニティVIP）
- Deep Agentsを「the fastest path to value that I have seen in my entire time with LangChain（LangChain歴全体で最も速い価値創出パス）」と評価
- MCP serverの構築・接続が5分でできたと報告

### Harrison Chaseの反応
> "Deep Agents stuff is some of the most exciting stuff that's happened recently. I think it reminds me a lot of like early days of LangChain."

## ハーネスとベンチマーク

### Sanjeed Mohammed
- RKGA（ARC-AGI）ベンチマークで、ハーネスを活用してGemini 3 Proの性能を最大限引き出した事例を紹介
- 「They basically beat the RKGA benchmark using like a bunch of harness and they've open sourced it.」
- Deep Agentsがこの種のハーネスの最適な場所になりうるとHarrison Chaseが同意

## Deep Agents時代の評価・デバッグ

Harrison Chaseが変化を説明:
- Deep Agentsのプロンプトは非常に長い（Claude Codeのプロンプトは約2,000行）
- トレースが複雑化（100ツールコール以上になることもある）
- スレッドビュー、スレッドレベルevals、AI支援によるデバッグを強化中
- CLIからLangSmithのトレースを取得してClaude Codeに渡す仕組みを開発中

## Context Engineering関連

### Ben McHone
- Claude Code styleの「skills markdown directory」の概念について質問
- Agent Builderがvirtual file systemを持っているが、code executionはまだ未対応
- Harrison Chase: 「enterprises from our experience don't love code execution（エンタープライズはコード実行を好まない傾向がある）」
