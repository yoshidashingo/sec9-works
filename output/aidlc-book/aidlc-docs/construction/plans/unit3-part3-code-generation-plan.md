# Code Generation Plan - Unit 3: Part III（Inceptionフェーズ・計画編）

## ユニット概要

- **対象**: Part III - Inceptionフェーズ（計画編）
- **章構成**: Chapter 7〜11（5章）
- **プロジェクト種別**: Greenfield（書籍コンテンツ）
- **Workspace Root**: `output/shingo/aidlc-book/`
- **コンテンツ配置先**: `output/shingo/aidlc-book/content/part3/`
- **ドキュメント配置先**: `aidlc-docs/construction/unit3-part3/code/`

## 設計参照

- **Functional Design**: `aidlc-docs/construction/unit3-part3/functional-design/`
  - `business-logic-model.md` — 各章の詳細目次・コンテンツフロー
  - `business-rules.md` — 執筆ルール・スタイルガイド
  - `domain-entities.md` — 登場概念・用語・ECサイトドメイン定義

## 要件トレーサビリティ

| 要件 | 章 |
|-----|-----|
| FR-03: Workspace Detection | Chapter 7 |
| FR-03: Reverse Engineering | Chapter 8 |
| FR-03: Requirements Analysis | Chapter 9 |
| FR-03: User Stories / Workflow Planning | Chapter 10 |
| FR-03: Application Design / Units Generation | Chapter 11 |

---

## 実行ステップ

### Step 1: コンテンツディレクトリ構造のセットアップ
- [x] `output/shingo/aidlc-book/content/part3/` ディレクトリを作成
- [x] `output/shingo/aidlc-book/content/part3/README.md`（Part III の概要インデックス）を作成

### Step 2: Chapter 7 — Workspace Detection の執筆
- [x] `output/shingo/aidlc-book/content/part3/chapter-07-workspace-detection.md` を作成
- 構成: この章で学ぶこと → 7.1 → 7.2 → コラム → 7.3（ハンズオン） → まとめ → チェックリスト
- 解説:ハンズオン = 7:3
- 比率参考ページ数: 12〜14ページ相当

### Step 3: Chapter 8 — Reverse Engineering の執筆
- [x] `output/shingo/aidlc-book/content/part3/chapter-08-reverse-engineering.md` を作成
- 構成: この章で学ぶこと → シナリオ切り替え宣言 → 8.1 → 8.2 → コラム → 8.3（ハンズオン） → シナリオ終了宣言 → まとめ → チェックリスト
- 解説:ハンズオン = 5:5

### Step 4: Chapter 9 — Requirements Analysis の執筆
- [x] `output/shingo/aidlc-book/content/part3/chapter-09-requirements-analysis.md` を作成
- 構成: この章で学ぶこと → 9.1 → 9.2 → コラム → 9.3（ハンズオン） → 9.4 → まとめ → チェックリスト
- 解説:ハンズオン = 5:5

### Step 5: Chapter 10 — User Stories と Workflow Planning の執筆
- [x] `output/shingo/aidlc-book/content/part3/chapter-10-user-stories-workflow-planning.md` を作成
- 構成: この章で学ぶこと → 10.1 → 10.2（ハンズオン） → コラム → 10.3 → 10.4（ハンズオン） → まとめ → チェックリスト
- 解説:ハンズオン = 6:4

### Step 6: Chapter 11 — Application Design と Units Generation の執筆
- [x] `output/shingo/aidlc-book/content/part3/chapter-11-application-design-units-generation.md` を作成
- 構成: この章で学ぶこと → 11.1 → 11.2（ハンズオン） → 11.3 → コラム → 11.4（ハンズオン） → 11.5 → まとめ → チェックリスト
- 解説:ハンズオン = 5:5

### Step 7: コンテンツサマリーの生成（ドキュメント）
- [x] `aidlc-docs/construction/unit3-part3/code/content-summary.md` を作成
  - 各章の要点・ページ数・カバーした要件のサマリー

---

## 注意事項

- 各章は `business-logic-model.md` の詳細目次に忠実に執筆すること
- コードサンプルは TypeScript + Next.js で記述し、コードブロックに言語タグを付ける
- ハンズオンセクションは「目標」→「ステップ」→「確認ポイント」の構造を守ること
- Chapter 8 はBrownfieldシナリオへの「切り替え宣言」と「終了宣言」を必ず含めること
- ECサイトのプロジェクト名は「BookCart」で統一すること
- Brownfieldサブシナリオのプロジェクト名は「LegacyShop」で統一すること
