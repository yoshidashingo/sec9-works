# LC-14. On Agent Frameworks and Agent Observability

- **著者**: LangChain Accounts
- **公開日**: 2026-02-12（最終更新: 2026-02-15）
- **URL**: https://blog.langchain.com/on-agent-frameworks-and-agent-observability/
- **重要度**: ★★
- **関連章**: 第3章, 第5章, 第7章

## 概要

言語モデルの改善に伴いエージェントフレームワークが依然として有用であるかを論じた記事。フレームワークは技術の進化と同じ速度で進化する場合に限り有用であると主張。

## フレームワークの3世代

1. **Chaining（2023年）**: LLMをデータとAPIに接続する初期アプローチ
2. **LangGraph（2024年）**: 耐久性とステートフルネスのためのランタイムサポートを備えた低レベルフレームワーク
3. **DeepAgents（2025年）**: 計画、ツール呼び出しループ、サブエージェントオーケストレーションをサポートする「バッテリー込み」ハーネス

> 「Agent frameworks are still useful, but only if they evolve as fast as the models do.」

## エージェントオブザーバビリティ戦略

- LangSmithはLangChainのOSSツールから意図的に独立して構築
- どのフレームワークを選択してもオブザーバビリティが機能
- AutoGen、Claude Agent SDK、CrewAIなどと統合
- OpenTelemetryベースのトレーシングをサポート

## コア哲学

- トレース（コードではなく）がエージェントの動作を記録
- デバッグ、テスト、モニタリングがエージェント開発の後付けではなく不可欠な要素
