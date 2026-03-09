# Content Summary - Unit 3: Part III（Inceptionフェーズ・計画編）

## 生成完了ファイル

| ファイル | パス | カバーした要件 |
|---------|------|-------------|
| README.md | `content/part3/README.md` | Part III 概要・索引 |
| Chapter 7 | `content/part3/chapter-07-workspace-detection.md` | FR-03（Workspace Detection） |
| Chapter 8 | `content/part3/chapter-08-reverse-engineering.md` | FR-03（Reverse Engineering） |
| Chapter 9 | `content/part3/chapter-09-requirements-analysis.md` | FR-03（Requirements Analysis） |
| Chapter 10 | `content/part3/chapter-10-user-stories-workflow-planning.md` | FR-03（User Stories / Workflow Planning） |
| Chapter 11 | `content/part3/chapter-11-application-design-units-generation.md` | FR-03（Application Design / Units Generation） |

## 各章の要点サマリー

### Chapter 7: Workspace Detection（12〜14ページ相当）
- GreenfieldとBrownfieldの定義と違い
- aidlc-state.md・audit.mdの構造と役割
- BookCart（ECサイト）の初期化ハンズオン
- コラム: Claude Codeのコンテキスト管理の仕組み

### Chapter 8: Reverse Engineering（12〜14ページ相当）
- Brownfieldサブシナリオ（LegacyShop引き継ぎ）
- REで生成される3成果物（code-map / dependency-analysis / architecture-overview）
- 深度設定（浅い/標準/深い）
- コラム: 技術的負債をAI-DLCでどう扱うか

### Chapter 9: Requirements Analysis（12〜14ページ相当）
- 適応型深度（Minimal/Standard/Comprehensive）
- [Answer]:タグフォーマットと良い回答の条件
- BookCartの要件定義ハンズオン（requirements.md生成）
- コラム: 要件の粒度 — WhatはAIに、HowはAIに任せる

### Chapter 10: User Stories と Workflow Planning（11〜13ページ相当）
- ストーリー vs タスクの違い（What vs How）
- 良いストーリーの3要素（Who / What / Why）
- スキップ可能なステージの判断基準
- per-unit loopの設計
- コラム: ストーリーのスキップ — いつ省略してよいか

### Chapter 11: Application Design と Units Generation（13〜15ページ相当）
- 過剰設計しない原則（YAGNI）
- モノリス vs マイクロサービスの選択基準
- ユニット粒度の目安（User Stories 3〜8本 = 1ユニット）
- BookCartのユニット分解ハンズオン（4ユニット）
- INCEPTIONフェーズ完了の確認手順

## 章横断チェック

| 確認項目 | 結果 |
|---------|------|
| FR-03の全サブ要件がカバーされているか | ✅（全7項目カバー） |
| ECサイト（BookCart）シナリオが一貫しているか | ✅ |
| Chapter 8のBrownfieldシナリオ切り替えが明示されているか | ✅ |
| 章フォーマット（冒頭・まとめ・チェックリスト・コラム）が統一されているか | ✅ |
| コードサンプルがTypeScript + Next.jsで統一されているか | ✅ |
| ハンズオンが「目標→ステップ→確認ポイント」の構造を持っているか | ✅ |

## 推定ボリューム

| 章 | 推定ページ数 |
|----|-----------|
| Chapter 7 | 13p |
| Chapter 8 | 13p |
| Chapter 9 | 13p |
| Chapter 10 | 12p |
| Chapter 11 | 14p |
| **合計** | **65p** |
