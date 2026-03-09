# 要件定義書 - 実践AI-DLC入門

## インテント分析

| 項目 | 評価 |
|------|------|
| **ユーザーリクエスト** | AI-DLCを活用して「実践AI-DLC入門」という書籍を執筆する |
| **リクエストタイプ** | New Project（書籍コンテンツ制作） |
| **スコープ推定** | System-wide（書籍全体：300ページ以上、6パート構成） |
| **複雑度推定** | Complex（商業出版レベルの品質、網羅的な章構成） |
| **要件深度** | Comprehensive |

---

## 1. プロジェクト概要

### 1.1 書籍情報

| 項目 | 内容 |
|------|------|
| **タイトル（仮）** | 実践AI-DLC入門 |
| **著者** | shingo（個人プロジェクト） |
| **出版形態** | 商業出版（技術書出版社からのリリース） |
| **想定ページ数** | 300ページ以上（網羅的・詳細） |
| **執筆スケジュール** | 3〜6ヶ月 |

### 1.2 書籍の位置付け

- **AI-DLC（AI-Driven Development Life Cycle）フレームワークの公式的な解説書**
- **日本のIT現場に特化**した文脈・事例で解説
- シニアエンジニア・アーキテクトが自社・自チームにAI-DLCを導入・展開できることをゴールとする

---

## 2. ターゲット読者

### 2.1 主要読者像（ペルソナ）

**シニアエンジニア・アーキテクト**
- 実務経験5年以上
- ソフトウェア開発のライフサイクル全般を理解している
- AI/LLMの基礎知識はあるが、AI-DLCは未経験
- 組織やチームへの新手法導入のリーダーシップを取る立場

### 2.2 前提知識

- ソフトウェア開発ライフサイクル（ウォーターフォール、アジャイル等）の実務経験
- Git、CLI操作の基本スキル
- AI/LLMの概念的理解（プロンプトエンジニアリングの基礎程度）
- Claude Codeの操作経験は不問（書籍内で環境構築からカバー）

---

## 3. 機能要件（書籍コンテンツ要件）

### FR-01: AI-DLC概念の解説

- AI-DLCとは何か（概念・哲学・設計思想）
- 従来の開発手法（ウォーターフォール、アジャイル、DevOps）との比較
- AI-DLCが解決する課題と適用シーン
- AI-DLCの三層構造（INCEPTION → CONSTRUCTION → OPERATIONS）

### FR-02: 環境構築・セットアップガイド

- Claude Codeのインストールと初期設定
- MCPサーバーの概念と設定方法
- `.steering/` ディレクトリの構造と役割
- CLAUDE.mdの書き方とベストプラクティス
- ワークスペースの準備

### FR-03: Inceptionフェーズの実践ガイド

- Workspace Detection の仕組みと実行フロー
- Reverse Engineering（Brownfieldプロジェクト対応）
- Requirements Analysis（適応型深度の考え方）
- User Stories の作成と活用
- Workflow Planning の実践
- Application Design の手法
- Units Generation によるタスク分解

### FR-04: Constructionフェーズの実践ガイド

- Functional Design（ビジネスロジック設計）
- NFR Requirements Assessment（非機能要件の評価）
- NFR Design（非機能要件の設計）
- Infrastructure Design（インフラ設計）
- Code Generation（計画→生成の2段階プロセス）
- Build and Test（ビルド・テスト指示の生成）

### FR-05: カスタマイズ・拡張方法

- ベースレイヤー（aws-aidlc-rule-details）の理解
- 拡張レイヤー（独自rule-details）の構築方法
- ルール読み込み手順と優先順位の設計
- 業界・組織固有のカスタマイズ事例
- テンプレートの作成と運用

### FR-06: 実プロジェクト事例（E2Eウォークスルー）

- Greenfieldプロジェクトの完全ウォークスルー
- Brownfieldプロジェクトの完全ウォークスルー
- 日本のIT現場における適用事例（匿名化済み）
- 失敗パターンとその対処法
- チーム導入のベストプラクティス

---

## 4. 非機能要件

### NFR-01: 品質基準（商業出版レベル）

- 技術的正確性：AI-DLCフレームワークの公式解説として信頼性のある内容
- 文章品質：プロの技術書ライティング基準に準拠
- コード例：実行可能でコピー&ペーストして動作するサンプル
- 図表：Mermaid図やASCII図を適切に使用し、ワークフローを視覚化

### NFR-02: 構成・可読性

- 各章は独立して読めるが、通読しても一貫したストーリーがある
- チュートリアル形式：ステップバイステップで手を動かしながら進められる
- 各章末にまとめ・チェックリストを配置
- 用語集・索引を充実させる

### NFR-03: 再現性

- 読者が手元の環境で書籍の手順を再現できること
- バージョン依存の内容は明記し、将来のアップデートに対応しやすい構造
- サンプルプロジェクトのリポジトリを提供

### NFR-04: 組織導入支援

- チーム導入のためのチェックリスト・テンプレート
- 段階的導入ロードマップ（個人→チーム→組織）
- ROI算出の参考指標

---

## 5. 書籍構成案（6パート）

### Part I: AI-DLCの世界へ（概念編）
- Chapter 1: なぜAI-DLCか — ソフトウェア開発の進化とAIの役割
- Chapter 2: AI-DLCフレームワーク概論 — 三層構造と適応型ワークフロー
- Chapter 3: 従来手法との比較 — ウォーターフォール、アジャイル、DevOpsからの進化

### Part II: 環境構築（セットアップ編）
- Chapter 4: Claude Codeのセットアップ
- Chapter 5: MCPサーバーとエコシステム
- Chapter 6: ワークスペースの設計 — .steering/、CLAUDE.md、ディレクトリ構造

### Part III: Inceptionフェーズ（計画編）
- Chapter 7: Workspace Detection — プロジェクトの起点
- Chapter 8: Reverse Engineering — 既存コードベースの理解
- Chapter 9: Requirements Analysis — 適応型の要件分析
- Chapter 10: User Stories と Workflow Planning
- Chapter 11: Application Design と Units Generation

### Part IV: Constructionフェーズ（構築編）
- Chapter 12: Functional Design — ビジネスロジックの設計
- Chapter 13: NFR Requirements & Design — 非機能要件への対応
- Chapter 14: Infrastructure Design — インフラ設計
- Chapter 15: Code Generation — AIによるコード生成
- Chapter 16: Build and Test — 品質保証

### Part V: カスタマイズと拡張（応用編）
- Chapter 17: ベースレイヤーと拡張レイヤーの仕組み
- Chapter 18: 独自ルールの構築 — 業界・組織に合わせた拡張
- Chapter 19: テンプレートとパターンライブラリ

### Part VI: 実践事例と導入ガイド（導入編）
- Chapter 20: Greenfieldプロジェクト E2Eウォークスルー
- Chapter 21: Brownfieldプロジェクト E2Eウォークスルー
- Chapter 22: 組織導入のロードマップ
- Chapter 23: FAQ・トラブルシューティング

### 付録
- 用語集
- ルールファイル一覧・リファレンス
- サンプルプロジェクト案内

---

## 6. 既存アセット・参照資料

| アセット | パス | 活用方法 |
|---------|------|---------|
| AI-DLCブログ記事群 | `output/shingo/blog-aidlc-complete-guide/` | 概念説明・各フェーズ解説のベースコンテンツ |
| AI-DLCルールファイル | `.steering/aws-aidlc-rule-details/` | フレームワーク仕様の正確な参照元 |
| GA拡張レイヤー | `.steering/ga-aidlc-rule-details/` | カスタマイズ事例の実例 |
| コアワークフロー | `.steering/aws-aidlc-rules/core-workflow.md` | ワークフロー解説の正確な参照元 |
| クライアントワーク成果物 | `output/ga/`, `output/sec9/` | 実事例（匿名化前提）の参照 |

---

## 7. 制約事項

- AI-DLCフレームワークの公式解説として、`aws-aidlc-rule-details` の内容を正確に反映すること
- クライアントワーク事例は完全に匿名化すること（企業名・業務内容を特定できないレベル）
- 商業出版の品質基準を満たすこと（誤字脱字ゼロ、技術的正確性、図表の美しさ）
- 3〜6ヶ月の執筆スケジュールを考慮した章ごとのマイルストーン管理
