# LC-16. Evaluating DeepAgents CLI on Terminal Bench 2.0

- **著者**: Vivek Trivedy, Eugene Yurtsev
- **公開日**: 2025-12-05
- **URL**: https://blog.langchain.com/evaluating-deepagents-cli-on-terminal-bench-2-0/
- **重要度**: ★★
- **関連章**: 第7章

## 概要

DeepAgents CLIをTerminal Bench 2.0で評価した結果報告。Claude Sonnet 4.5使用時に42.65%を達成し、「Claude Code自体と同等」のパフォーマンスを記録。

## DeepAgents CLIとは

「ターミナル駆動のコーディングエージェントで、オープンソース、Python製、モデル非依存」

機能:
- ファイル操作
- シェルコマンド実行
- ウェブ検索
- タスク計画
- 永続メモリストレージ

## 評価の技術的課題と解決策

**課題**: テスト環境の分離確保

**解決策**: Harbor フレームワーク
- Docker、Modal、Daytona、E2B、Runloopをサンドボックスプロバイダーとしてサポート
- コンテナ化されたエージェント評価のスケーリング

## Terminal Bench 2.0 ベンチマーク

- 89タスクで構成
- 対象領域: ソフトウェアエンジニアリング、バイオロジー、セキュリティ、ゲーミング
- タスク例: Cプログラムのリバースエンジニアリング、チェスエンジン最適化、複雑なgit操作
- タスク複雑性: 素早い完了から「10分近く、100以上のツール呼び出し」を要するものまで

## 結果

- Claude Sonnet 4.5使用
- 2回のトライアル: 44.9%、40.4%
- 平均: 42.65%
- 「Claude Code自体と同等」のポジション

## 技術実装

HarborSandbox: シェルコマンドの上にファイルシステムツールを実装するバックエンドラッパー
