# LC-08. Improving Deep Agents with Harness Engineering

- **著者**: LangChain Accounts
- **公開日**: 2026-02-17
- **URL**: https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- **重要度**: ★★★
- **関連章**: 第3章, 第6章, 第7章

## 概要

LangChainチームがコーディングエージェント（DeepAgents CLI）をTerminal Bench 2.0でTop 30からTop 5に改善した事例報告。モデル（GPT-5.2-Codex）を一切変更せず、ハーネスの変更のみでスコアを52.8から66.5へ13.7ポイント向上させた。

## 核心メッセージ

「Harness Engineering is about systems, you're building tooling around the model to optimize goals like task performance, token efficiency, latency, etc.」（ハーネスエンジニアリングはシステムに関するものであり、タスク性能・トークン効率・レイテンシなどの目標を最適化するためにモデルの周囲にツーリングを構築する）

## 3つの主要最適化領域

### 1. Build & Self-Verification Loop（構築と自己検証ループ）
- エージェントに計画・構築・検証・修正のフェーズを実施させるガイダンス
- `PreCompletionChecklistMiddleware`を追加し、タスク完了前に検証パスを強制
- ハッピーパスとエッジケースのテスト作成を強調

### 2. Environmental Context Delivery（環境コンテキストの配信）
- `LocalContextMiddleware`がディレクトリ構造をマッピングし、利用可能なツールを発見
- 時間予算の警告を注入し、エージェントの時間見積もりを改善
- テスト可能なコード基準と厳格な評価基準についてエージェントに教育

### 3. Reasoning Compute Allocation（推論計算の割り当て）
- 「推論サンドイッチ」パターンの実装:
  - 計画フェーズ: extra-high
  - 実装フェーズ: high
  - 検証フェーズ: extra-high
- 最大推論のみのアプローチは53.9%、バランス型割り当ては63.6%を達成
- バランス型アプローチがタイムアウト失敗を防止

## 追加改善

- **LoopDetectionMiddleware**: ファイル編集を追跡し、繰り返しの「破滅ループ」を検出・中断。N回以上の同一ファイル編集後に「...consider reconsidering your approach」などのコンテキストを追加
- **トレース分析**: 実験ランにわたるエラー検出の自動化
- **コンテキスト化された指示**: 環境発見エラーの削減

## 一般原則

- エージェントに代わってコンテキストエンジニアリングを実施
- 積極的な自己検証プロンプティング
- トレーシングベースのフィードバック
- 現在のモデルの限界に対するパターン検出
- モデル固有のハーネスカスタマイゼーション
