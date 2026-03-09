# LC-17. Introducing Open SWE: An Open-Source Asynchronous Coding Agent

- **著者**: LangChain Accounts
- **公開日**: 2025-08-06（最終更新: 2026-01-15）
- **URL**: https://blog.langchain.com/introducing-open-swe-an-open-source-asynchronous-coding-agent/
- **重要度**: ★★
- **関連章**: 第6章, 第8章

## 概要

クラウド上で非同期に動作するオープンソースのコーディングエージェント「Open SWE」の発表。「長時間実行される、より自律的なエージェント」としてのAIの進化を示す。

## 主要機能

### 統合とアクセス方法
- GitHubリポジトリと直接統合
- GitHubイシューまたはカスタムUIから作業を委譲可能
- チームメンバーのような動作（コード作成、テスト実行、自己レビュー、PR作成）

### 制御機能
- **人間介入（Human-in-the-Loop）**: 計画段階で承認、編集、変更リクエストが可能
- **継続的フィードバック**: 実行中のエージェントへのメッセージ送信対応

## 技術アーキテクチャ: 3段階エージェント構造

1. **Manager**: ユーザーインタラクション処理と担当振り分け
2. **Planner**: コード分析前の詳細計画作成
3. **Programmer & Reviewer**: サンドボックスでのコード実行とQA検証

### 基盤技術
- LangGraphによる複雑なワークフロー管理
- LangGraph Platformで長時間実行対応
- Daytona隔離サンドボックスで安全性確保

## 制約と今後

- 「シンプルな1行修正には最適でない」と認識
- ローカルCLI版の開発が進行中
