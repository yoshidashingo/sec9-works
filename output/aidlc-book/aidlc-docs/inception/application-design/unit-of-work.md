# Unit of Work - 実践AI-DLC入門

## 概要

書籍「実践AI-DLC入門」を6ユニット（パート）に分解する。各ユニットはConstructionフェーズで独立して Functional Design → Code Generation サイクルを実行する。

**執筆順序（Q1: B - コア部分を先に）**:
1. Unit 3: Part III（Inceptionフェーズ）
2. Unit 4: Part IV（Constructionフェーズ）
3. Unit 1: Part I（AI-DLC概念）
4. Unit 2: Part II（環境構築）
5. Unit 5: Part V（カスタマイズ）
6. Unit 6: Part VI（実践事例）

**チュートリアル題材（Q2: B）**: ECサイト
**実事例の粒度（Q3: B）**: 業界・課題・適用プロセスを具体的に記載（企業名以外）

---

## Unit 3: Part III - Inceptionフェーズ（計画編）

**執筆順序**: 1番目（コア部分 - 最初に執筆）

### 責務
- AI-DLCのInceptionフェーズ全7ステージを実践チュートリアル形式で解説
- ECサイトを題材に Workspace Detection から Units Generation までをウォークスルー

### 章構成

| 章 | タイトル | 内容 |
|----|---------|------|
| Chapter 7 | Workspace Detection — プロジェクトの起点 | GreenfieldとBrownfieldの判定、aidlc-state.md初期化 |
| Chapter 8 | Reverse Engineering — 既存コードベースの理解 | BrownfieldプロジェクトのREパターン |
| Chapter 9 | Requirements Analysis — 適応型の要件分析 | 適応型深度の考え方、質問生成フロー |
| Chapter 10 | User Stories と Workflow Planning | ストーリーマッピング、実行計画の設計 |
| Chapter 11 | Application Design と Units Generation | アーキテクチャ設計、ユニット分解 |

### 想定ボリューム
- 5章構成、60〜70ページ

### 既存アセット
- `output/shingo/blog-aidlc-complete-guide/` 内のInceptionフェーズ関連ブログ記事
- `.steering/aws-aidlc-rule-details/inception/` 配下の全ルールファイル
- `output/ga/20260202_hirogin/aidlc-docs/inception/` の実例成果物

### サンプルコード・図表方針
- ECサイトを題材としたCLAUDE.md例、aidlc-state.md例
- 各ステージの入力→処理→出力フロー図（Mermaid）
- 実際のプロンプトと応答例（コードブロック）

---

## Unit 4: Part IV - Constructionフェーズ（構築編）

**執筆順序**: 2番目（コア部分）

### 責務
- AI-DLCのConstructionフェーズ全6ステージを実践チュートリアル形式で解説
- Unit 3のECサイト設計を引き継いで、実際のコード生成・テストまでをウォークスルー

### 章構成

| 章 | タイトル | 内容 |
|----|---------|------|
| Chapter 12 | Functional Design — ビジネスロジックの設計 | functional-spec.md生成、ステートマシン設計 |
| Chapter 13 | NFR Requirements & Design — 非機能要件への対応 | パフォーマンス・セキュリティ・スケーラビリティ設計 |
| Chapter 14 | Infrastructure Design — インフラ設計 | AWS構成、IaC（CDK/Terraform）設計 |
| Chapter 15 | Code Generation — AIによるコード生成 | 計画→生成の2段階プロセス、コードレビュー |
| Chapter 16 | Build and Test — 品質保証 | ビルド・テスト指示生成、CI/CD連携 |

### 想定ボリューム
- 5章構成、65〜75ページ

### 既存アセット
- `.steering/aws-aidlc-rule-details/construction/` 配下の全ルールファイル
- `output/ga/20260202_hirogin/aidlc-docs/construction/` の実例成果物

### サンプルコード・図表方針
- ECサイトのfunctional-spec.md実例
- インフラ構成図（Mermaid）
- 実際のコード生成プロンプト→生成コードの例

---

## Unit 1: Part I - AI-DLCの世界へ（概念編）

**執筆順序**: 3番目（Part III・IV を参照して整合させる）

### 責務
- AI-DLCの哲学・設計思想・位置付けを解説
- 読者がAI-DLCを選ぶ理由と適用シーンを理解する

### 章構成

| 章 | タイトル | 内容 |
|----|---------|------|
| Chapter 1 | なぜAI-DLCか | ソフトウェア開発の進化とAIの役割 |
| Chapter 2 | AI-DLCフレームワーク概論 | 三層構造と適応型ワークフロー |
| Chapter 3 | 従来手法との比較 | ウォーターフォール、アジャイル、DevOpsからの進化 |

### 想定ボリューム
- 3章構成、35〜45ページ

### 既存アセット
- `output/shingo/blog-aidlc-complete-guide/` 内の概念解説ブログ記事
- `.steering/aws-aidlc-rules/core-workflow.md` の設計思想

---

## Unit 2: Part II - 環境構築（セットアップ編）

**執筆順序**: 4番目（Part III・IVで使ったツール・環境を正確に記述）

### 責務
- 読者が書籍の手順を手元で再現するための環境を構築できるようにする
- Claude Code、MCPサーバー、ワークスペース設計の実践ガイド

### 章構成

| 章 | タイトル | 内容 |
|----|---------|------|
| Chapter 4 | Claude Codeのセットアップ | インストール、初期設定、基本操作 |
| Chapter 5 | MCPサーバーとエコシステム | MCPの概念、主要MCPの設定方法 |
| Chapter 6 | ワークスペースの設計 | .steering/、CLAUDE.md、ディレクトリ構造のベストプラクティス |

### 想定ボリューム
- 3章構成、35〜45ページ

### 既存アセット
- Claude Code公式ドキュメント（参照）
- このリポジトリの `.steering/`・`CLAUDE.md` の実例

---

## Unit 5: Part V - カスタマイズと拡張（応用編）

**執筆順序**: 5番目（Part III・IVの実践後に拡張方法を解説）

### 責務
- AI-DLCフレームワークの拡張方法を解説
- 組織・業界固有のカスタマイズを自分で設計できるようにする

### 章構成

| 章 | タイトル | 内容 |
|----|---------|------|
| Chapter 17 | ベースレイヤーと拡張レイヤーの仕組み | rule-detailsの構造、優先順位の設計 |
| Chapter 18 | 独自ルールの構築 | 業界・組織固有のカスタマイズ事例 |
| Chapter 19 | テンプレートとパターンライブラリ | 再利用可能なテンプレートの作成と運用 |

### 想定ボリューム
- 3章構成、35〜45ページ

### 既存アセット
- `.steering/ga-aidlc-rule-details/` — GA社カスタマイズ実例
- `.steering/sec9-aidlc-rule-details/` — Sec9社カスタマイズ実例

---

## Unit 6: Part VI - 実践事例と導入ガイド（導入編）

**執筆順序**: 6番目（全ユニット完成後に執筆）

### 責務
- E2Eウォークスルーと実事例で書籍全体の知識を統合
- 組織導入のロードマップを提供

### 章構成

| 章 | タイトル | 内容 |
|----|---------|------|
| Chapter 20 | GreenfieldプロジェクトのE2Eウォークスルー | ECサイトの完全ウォークスルー（Inception〜Construction） |
| Chapter 21 | BrownfieldプロジェクトのE2Eウォークスルー | 既存システム改修の完全ウォークスルー |
| Chapter 22 | 組織導入のロードマップ | 段階的導入計画、ROI算出、チェックリスト |
| Chapter 23 | FAQ・トラブルシューティング | よくある失敗パターンと対処法 |

### 想定ボリューム
- 4章構成、55〜65ページ

### 実事例の方針（Q3: B）
- 業界・課題・AI-DLC適用プロセスを具体的に記載
- 企業名・個人名は匿名化（「ある金融系SaaS企業（従業員200名）」程度の記述）
- `output/ga/`、`output/sec9/` の実際の成果物を匿名化して活用

### 既存アセット
- `output/ga/20260202_hirogin/aidlc-docs/` — 実事例成果物（要匿名化）
- `output/ga/`、`output/sec9/` 配下の各案件成果物

---

## 書籍全体ボリューム見積もり

| ユニット | 章数 | 想定ページ数 |
|---------|------|------------|
| Unit 1: Part I（概念編） | 3章 | 35〜45p |
| Unit 2: Part II（セットアップ編） | 3章 | 35〜45p |
| Unit 3: Part III（計画編） | 5章 | 60〜70p |
| Unit 4: Part IV（構築編） | 5章 | 65〜75p |
| Unit 5: Part V（応用編） | 3章 | 35〜45p |
| Unit 6: Part VI（導入編） | 4章 | 55〜65p |
| **付録** | — | 20〜30p |
| **合計** | **23章** | **305〜375p** |
