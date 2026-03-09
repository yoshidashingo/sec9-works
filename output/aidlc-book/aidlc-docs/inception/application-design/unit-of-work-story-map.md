# Unit of Work Story Map - 実践AI-DLC入門

## 概要

機能要件（FR-01〜FR-06）→ ユニット → 章 のマッピング。全要件がいずれかのユニットにカバーされていることを確認する。

---

## 要件→ユニット→章 マッピング

### FR-01: AI-DLC概念の解説

| 要件項目 | ユニット | 章 |
|---------|---------|-----|
| AI-DLCとは何か（概念・哲学・設計思想） | Unit 1 | Chapter 2 |
| 従来手法との比較（ウォーターフォール、アジャイル、DevOps） | Unit 1 | Chapter 3 |
| AI-DLCが解決する課題と適用シーン | Unit 1 | Chapter 1, 2 |
| 三層構造（INCEPTION → CONSTRUCTION → OPERATIONS） | Unit 1 | Chapter 2 |

### FR-02: 環境構築・セットアップガイド

| 要件項目 | ユニット | 章 |
|---------|---------|-----|
| Claude Codeのインストールと初期設定 | Unit 2 | Chapter 4 |
| MCPサーバーの概念と設定方法 | Unit 2 | Chapter 5 |
| .steering/ディレクトリの構造と役割 | Unit 2 | Chapter 6 |
| CLAUDE.mdの書き方とベストプラクティス | Unit 2 | Chapter 6 |
| ワークスペースの準備 | Unit 2 | Chapter 6 |

### FR-03: Inceptionフェーズの実践ガイド

| 要件項目 | ユニット | 章 |
|---------|---------|-----|
| Workspace Detection の仕組みと実行フロー | Unit 3 | Chapter 7 |
| Reverse Engineering（Brownfieldプロジェクト対応） | Unit 3 | Chapter 8 |
| Requirements Analysis（適応型深度の考え方） | Unit 3 | Chapter 9 |
| User Stories の作成と活用 | Unit 3 | Chapter 10 |
| Workflow Planning の実践 | Unit 3 | Chapter 10 |
| Application Design の手法 | Unit 3 | Chapter 11 |
| Units Generation によるタスク分解 | Unit 3 | Chapter 11 |

### FR-04: Constructionフェーズの実践ガイド

| 要件項目 | ユニット | 章 |
|---------|---------|-----|
| Functional Design（ビジネスロジック設計） | Unit 4 | Chapter 12 |
| NFR Requirements Assessment（非機能要件の評価） | Unit 4 | Chapter 13 |
| NFR Design（非機能要件の設計） | Unit 4 | Chapter 13 |
| Infrastructure Design（インフラ設計） | Unit 4 | Chapter 14 |
| Code Generation（計画→生成の2段階プロセス） | Unit 4 | Chapter 15 |
| Build and Test（ビルド・テスト指示の生成） | Unit 4 | Chapter 16 |

### FR-05: カスタマイズ・拡張方法

| 要件項目 | ユニット | 章 |
|---------|---------|-----|
| ベースレイヤー（aws-aidlc-rule-details）の理解 | Unit 5 | Chapter 17 |
| 拡張レイヤー（独自rule-details）の構築方法 | Unit 5 | Chapter 18 |
| ルール読み込み手順と優先順位の設計 | Unit 5 | Chapter 17 |
| 業界・組織固有のカスタマイズ事例 | Unit 5 | Chapter 18 |
| テンプレートの作成と運用 | Unit 5 | Chapter 19 |

### FR-06: 実プロジェクト事例（E2Eウォークスルー）

| 要件項目 | ユニット | 章 |
|---------|---------|-----|
| Greenfieldプロジェクトの完全ウォークスルー | Unit 6 | Chapter 20 |
| Brownfieldプロジェクトの完全ウォークスルー | Unit 6 | Chapter 21 |
| 日本のIT現場における適用事例（匿名化済み） | Unit 6 | Chapter 22 |
| 失敗パターンとその対処法 | Unit 6 | Chapter 23 |
| チーム導入のベストプラクティス | Unit 6 | Chapter 22 |

---

## 網羅性検証

| 要件 | カバーユニット | カバー章 | 状態 |
|------|-------------|---------|------|
| FR-01 | Unit 1 | Ch 1, 2, 3 | ✅ |
| FR-02 | Unit 2 | Ch 4, 5, 6 | ✅ |
| FR-03 | Unit 3 | Ch 7, 8, 9, 10, 11 | ✅ |
| FR-04 | Unit 4 | Ch 12, 13, 14, 15, 16 | ✅ |
| FR-05 | Unit 5 | Ch 17, 18, 19 | ✅ |
| FR-06 | Unit 6 | Ch 20, 21, 22, 23 | ✅ |

**全要件（FR-01〜FR-06）が各ユニットにカバーされていることを確認。漏れなし。**

---

## ユニット境界検証

| 検証項目 | 結果 |
|---------|------|
| 重複なし（同じ章が複数ユニットに割り当てられていないか） | ✅ なし |
| 漏れなし（全23章がいずれかのユニットに割り当てられているか） | ✅ なし |
| 付録の帰属 | Unit 6に付随（整合性確認時に一緒に作成） |
