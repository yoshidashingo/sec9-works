# LC-18. Debugging Deep Agents with LangSmith

- **著者**: LangChain Accounts
- **公開日**: 2025-12-10
- **URL**: https://blog.langchain.com/debugging-deep-agents-with-langsmith/
- **重要度**: ★★
- **関連章**: 第7章

## 概要

Deep AgentsのデバッグがシンプルなLLMアプリケーションとどう異なるかを解説。「数十から数百のステップ」を含む長時間操作と複数のユーザーインタラクションにより、大量のトレースデータが生成される課題に対処。

## Deep Agentsの主要課題

- **長大なプロンプト**: ペルソナ、ツール指示、ガイドライン、例示が数百行に及ぶ
- **長い実行トレース**: 完了に数分を要する
- **マルチターン会話**: 複数のインタラクションにまたがる

## 導入されたソリューション

### 1. Polly
LangSmithに統合されたAIアシスタント:
- トレースとスレッドを分析
- 「エージェントはミスをしたか」などの質問に回答
- 自然言語による説明を通じたプロンプト改善の提案

### 2. LangSmith Fetch CLI
コーディングエージェント（Claude Code、DeepAgents）を使用する開発者向けのCLIツール:
- IDEから直接LangSmithのトレースにアクセス
- `langsmith-fetch traces --project-uuid <uuid> --format json`で最近のトレースを取得
- データセットのエクスポート

## コアコンセプト

「トレーシング」（実行データのロギング）がラン、トレース、スレッドをキャプチャし、複雑なエージェント動作のデバッグに必要な可視性を提供。
