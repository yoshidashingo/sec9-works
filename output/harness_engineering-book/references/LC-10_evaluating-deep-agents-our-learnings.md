# LC-10. Evaluating Deep Agents: Our Learnings

- **著者**: LangChain Accounts
- **公開日**: 2025-12-03
- **URL**: https://blog.langchain.com/evaluating-deep-agents-our-learnings/
- **重要度**: ★★
- **関連章**: 第7章

## 概要

LangChainが1ヶ月間でDeep Agents技術を使った4つのアプリケーション（DeepAgents CLI、LangSmith Assist、Personal Email Assistant、Agent Builder）を出荷した際の評価パターンの知見をまとめた記事。

## 5つの主要評価パターン

### 1. Bespoke Test Logic Per Datapoint（データポイントごとのカスタムテストロジック）
- Deep Agentsは各テストケースにカスタムの成功基準が必要
- 従来のLLM評価（同一ロジックを全データポイントに適用）とは異なる
- トラジェクトリ、最終レスポンス、状態変更を検査するアサーション
- regexとLLM-as-judgeアプローチの併用

### 2. Single-Step Evaluations（シングルステップ評価）
- 「テストケースの約半分がシングルステップ評価」
- 即時のエージェント判断を検証
- 正しいツール選択とパラメータの検証
- トークン消費を抑制
- LangGraphの中断機能で実行前にツール呼び出しを検査

### 3. Full Agent Turns（完全なエージェントターン）
完全な実行で3つの次元のエンドツーエンド動作を検証:
- **Trajectory（トラジェクトリ）**: 実行中に呼び出されたツールシーケンス
- **Final Response（最終レスポンス）**: 最終出力の品質
- **Other State（その他の状態）**: ファイルやリサーチソースなどの生成された成果物

### 4. Multi-Turn Conversations（マルチターン会話）
- 順次インタラクションのテストには条件付きロジックが必要
- 厳格なシーケンスのハードコーディングではなく、中間出力をチェックして分岐
- エージェントの逸脱からのカスケード失敗を防止

### 5. Environment Setup（環境セットアップ）
- 「各評価ランごとにクリーンな環境」を確保し再現性を維持
- コーディングエージェントはDockerサンドボックスが有効
- シンプルな実装では一時ディレクトリを使用
- VCRなどのツールによるAPIモッキングで速度とデバッグ性を改善

## 追加の推奨事項

- 外部APIリクエストをモックしてコストと複雑さを削減
- LangSmithのPytestおよびVitest統合を活用した柔軟なテストフレームワーク
