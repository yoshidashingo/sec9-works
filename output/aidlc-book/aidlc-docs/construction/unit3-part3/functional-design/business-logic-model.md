# Business Logic Model - Unit 3: Part III（Inceptionフェーズ・計画編）

## 前提条件

- **ECサイトシナリオ**: シンプルなB2C物販サイト（書籍・雑貨等を販売する中小企業）
- **テックスタック**: TypeScript + Next.js（フルスタック）
- **Chapter 8サブシナリオ**: 「レガシーECサイトを引き継いだ場合」（Brownfield想定）
- **章フォーマット**: 冒頭「この章で学ぶこと」、末尾「まとめ」「チェックリスト」、章中コラム1〜2個
- **解説:ハンズオン比率**: トータル 解説6:ハンズオン4（章ごとに調整）

---

## Chapter 7: Workspace Detection — プロジェクトの起点

**比率**: 解説7 : ハンズオン3（概念理解が重要な導入章）
**想定ページ数**: 12〜14ページ

### 詳細目次

```
この章で学ぶこと
  ・Workspace Detectionがなぜ必要か
  ・GreenfieldとBrownfieldの違い
  ・aidlc-state.mdの役割と構造
  ・ECサイトプロジェクトの初期化の流れ

7.1 Workspace Detectionとは
  7.1.1 AI-DLCワークフローの「起点」としての役割
  7.1.2 GreenfieldとBrownfieldの定義
  7.1.3 なぜ最初にワークスペースを検出するのか

7.2 検出プロセスのしくみ
  7.2.1 Claude Codeがワークスペースを読み取るメカニズム
  7.2.2 aidlc-state.mdの構造と各フィールドの意味
  7.2.3 audit.mdによるトレーサビリティの確保

[コラム] aidlc-state.md はなぜ必要か — Claude Codeのコンテキスト管理の仕組み

7.3 ハンズオン: ECサイトプロジェクトの初期化
  7.3.1 サンプルリポジトリのセットアップ
       （目標: Next.jsプロジェクトを作成し、AI-DLCを開始できる状態にする）
       1. GitHubリポジトリの作成
       2. Next.jsプロジェクトの初期化（npx create-next-app）
       3. .steering/ディレクトリの配置
       4. CLAUDE.mdの作成
  7.3.2 Workspace Detectionの実行
       （目標: Claude Codeが自動的にGreenfieldと判定する流れを観察する）
       1. Claude Codeに「AI-DLCを開始して」と指示
       2. 生成されるaidlc-state.mdを確認
       3. audit.mdへの記録を確認
  7.3.3 生成成果物のレビュー
       ・aidlc-state.mdの各フィールドを読み解く
       ・Greenfieldと判定された根拠の確認

まとめ
チェックリスト
  □ .steering/ディレクトリを配置した
  □ CLAUDE.mdを作成した
  □ Workspace Detectionを実行した
  □ aidlc-state.mdが生成されたことを確認した
  □ audit.mdへの記録を確認した
```

---

## Chapter 8: Reverse Engineering — 既存コードベースの理解

**サブシナリオ**: レガシーECサイトの引き継ぎ（Brownfield）
**比率**: 解説5 : ハンズオン5（体験が理解を深める）
**想定ページ数**: 12〜14ページ

### 詳細目次

```
この章で学ぶこと
  ・Reverse Engineeringが必要なシーンとは
  ・REで生成される成果物と使い方
  ・Brownfieldプロジェクトでのワークスペース検出の違い
  ・レガシーECサイト引き継ぎのシナリオ

[シナリオ切り替え宣言]
ここからChapter 8の終わりまでは、Brownfieldシナリオ（レガシーECサイトの引き継ぎ）で進めます。
Chapter 9からGreenfieldシナリオ（ECサイト新規開発）に戻ります。

8.1 Reverse Engineeringとは
  8.1.1 BrownfieldプロジェクトでREが必要な理由
  8.1.2 REで生成される成果物（code-map.md / dependency-analysis.md / architecture-overview.md）
  8.1.3 REの「深度」設定 — どこまで分析するか

8.2 サブシナリオ: レガシーECサイトを引き継いだ場合
  8.2.1 シナリオ設定
       ・3年前にリリースした自社ECサイト（Node.js + MySQL）を引き継いだ
       ・ドキュメントはほぼない、テストも不十分
       ・新機能（ポイントシステム）追加を命じられた
  8.2.2 引き継ぎプロジェクトのサンプルコード概説
       ・ディレクトリ構造の紹介
       ・主要ファイルの役割

[コラム] 「技術的負債」をAI-DLCでどう扱うか

8.3 ハンズオン: Reverse Engineeringの実行
  8.3.1 BrownfieldとしてWorkspace Detectionを実行する
       （目標: Claude Codeが自動的にBrownfieldと判定し、REを提案する流れを観察する）
       1. 既存コードが存在するリポジトリでClaude Codeを起動
       2. Brownfield判定の根拠を確認
       3. REの実行を指示
  8.3.2 生成成果物の確認
       （目標: REで生成されたドキュメントを読み、コードベースへの理解を深める）
       1. code-map.mdを読む
       2. dependency-analysis.mdを読む
       3. architecture-overview.mdを読む
  8.3.3 REの結果をRequirements Analysisに活かす
       ・「ポイントシステム追加」という要件への適用

[シナリオ終了宣言]
Chapter 9からはGreenfieldシナリオ（ECサイト新規開発）に戻ります。

まとめ
チェックリスト
  □ Brownfield判定の仕組みを理解した
  □ REを実行してcode-map.mdを生成した
  □ architecture-overview.mdで既存システムの全体像を把握した
  □ REの深度設定を調整した経験を積んだ
```

---

## Chapter 9: Requirements Analysis — 適応型の要件分析

**比率**: 解説5 : ハンズオン5（質問生成の観察と回答が中心）
**想定ページ数**: 12〜14ページ

```
この章で学ぶこと
  ・Requirements Analysisの役割とプロセス
  ・適応型深度とは何か
  ・質問生成のしくみと「良い質問」の条件
  ・ECサイトの要件を定義する

9.1 Requirements Analysisの役割
  9.1.1 なぜAI-DLCは質問を自動生成するのか
  9.1.2 適応型深度の概念 — プロジェクト規模・複雑度に応じた調整
  9.1.3 requirements.mdの構造と各セクションの意味

9.2 質問生成メカニズムの理解
  9.2.1 Claude Codeはどのように質問を設計するか
  9.2.2 [Answer]:タグのしくみ
  9.2.3 良い回答が設計品質を決める — 「具体的に答える」重要性

[コラム] 要件の粒度 — どこまで詳細にすべきか

9.3 ハンズオン: ECサイトの要件分析
  9.3.1 Requirements Analysisの実行
       （目標: 質問ファイルが生成される流れを観察し、内容を理解する）
       1. Claude Codeに「ECサイトを作りたい」と伝える
       2. 質問ファイルの生成を確認
       3. 各質問の意図を読み解く
  9.3.2 質問への回答（サンプル回答付き）
       （目標: 適切な粒度・具体性で回答することを体験する）
       1. 各[Answer]:タグに回答を記入
       2. 曖昧な回答を避ける方法を実践
  9.3.3 requirements.mdの生成と確認
       （目標: 回答から要件定義書が生成されることを確認する）
       1. requirements.mdの生成を確認
       2. 各セクションの内容をレビュー
       3. 承認プロセスの実行

9.4 要件の承認と次ステージへの移行
  9.4.1 「承認」とは何か — AI-DLCにおける合意形成の意味
  9.4.2 aidlc-state.mdの更新確認

まとめ
チェックリスト
  □ 質問ファイルが生成されることを確認した
  □ 全質問に具体的な回答を記入した
  □ requirements.mdを生成・レビューした
  □ 要件を承認してaidlc-state.mdが更新されることを確認した
```

---

## Chapter 10: User Stories と Workflow Planning

**比率**: 解説6 : ハンズオン4
**想定ページ数**: 11〜13ページ

```
この章で学ぶこと
  ・User Storiesの役割とAI-DLCにおける位置付け
  ・ストーリーの粒度と書き方
  ・Workflow Planningで実行計画を設計する方法
  ・スキップ判断の基準

10.1 User Storiesの役割
  10.1.1 AI-DLCにおけるUser Storiesの位置付け
  10.1.2 ストーリー vs タスク — 粒度の違い
  10.1.3 良いユーザーストーリーの3要素（Who / What / Why）

10.2 ハンズオン: ECサイトのUser Stories生成
  10.2.1 Claude Codeによるストーリー自動生成
       （目標: 要件から自動生成されるストーリーを観察する）
       1. 「User Storiesを生成して」と指示
       2. user-stories.mdの生成を確認
  10.2.2 ストーリーのレビューと修正
       ・不要なストーリーの削除
       ・粒度の調整
       ・抜け漏れの追加

[コラム] ストーリーのスキップ — いつ省略してよいか

10.3 Workflow Planningとは
  10.3.1 実行計画（execution-plan.md）の設計思想
  10.3.2 スキップ可能なステージの判断基準
       ・書籍プロジェクト・小規模・フロントエンドのみ など
  10.3.3 per-unit loopの設計

10.4 ハンズオン: ECサイトの実行計画策定
  10.4.1 Workflow Planningの実行
       （目標: execution-plan.mdが生成される流れを観察する）
       1. 「Workflow Planningを実行して」と指示
       2. execution-plan.mdの生成を確認
       3. スキップ・実行ステージの根拠を確認

まとめ
チェックリスト
  □ user-stories.mdを生成した
  □ ストーリーのレビュー・修正を実施した
  □ execution-plan.mdを生成した
  □ スキップ・実行ステージの判断根拠を確認した
```

---

## Chapter 11: Application Design と Units Generation

**比率**: 解説5 : ハンズオン5（設計とユニット分解は実践で理解する）
**想定ページ数**: 13〜15ページ

```
この章で学ぶこと
  ・Application Designの役割と「過剰設計しない」原則
  ・ユニット分解の考え方（マイクロサービス vs モノリス）
  ・Units Generationで生成される3つの成果物
  ・INCEPTIONフェーズの完了とCONSTRUCTIONへの引き継ぎ

11.1 Application Designの役割
  11.1.1 高レベルコンポーネント設計とは
  11.1.2 AI-DLCにおける「過剰設計しない」原則
  11.1.3 Application Designで設計する対象の範囲

11.2 ハンズオン: ECサイトのApplication Design
  11.2.1 Application Designの実行
       （目標: コンポーネント設計が自動生成される流れを観察する）
       1. 「Application Designを実行して」と指示
       2. application-design.mdの生成を確認
  11.2.2 成果物のレビュー
       ・コンポーネント構成の確認
       ・ECサイトのアーキテクチャを読み解く

11.3 Units Generation によるタスク分解
  11.3.1 ユニット分解の考え方
       ・マイクロサービス vs モノリス — どちらを選ぶか
       ・ユニットの粒度と境界の設計
  11.3.2 依存関係の整理
       ・unit-of-work-dependency.mdの役割
       ・依存関係が開発順序を決める

[コラム] ユニットの粒度 — 大きすぎず小さすぎず

11.4 ハンズオン: ECサイトのユニット分解
  11.4.1 Units Generationの実行
       （目標: ユニット分解計画と成果物を生成する）
       1. Units Generationの計画作成を指示
       2. 質問に回答してユニットを確定
       3. unit-of-work.mdの生成を確認
       4. unit-of-work-dependency.mdで依存関係を確認
       5. unit-of-work-story-map.mdでマッピングを確認

11.5 INCEPTIONフェーズの完了
  11.5.1 CONSTRUCTIONフェーズへの引き継ぎチェックリスト
  11.5.2 aidlc-state.mdの最終確認
  11.5.3 Part IIIのまとめ — INCEPTIONで何を準備したか

まとめ
チェックリスト
  □ application-design.mdを生成してレビューした
  □ unit-of-work.mdを生成した
  □ unit-of-work-dependency.mdで依存関係を確認した
  □ unit-of-work-story-map.mdでマッピングを確認した
  □ aidlc-state.mdでINCEPTION完了を確認した
```

---

## コンテンツフロー概要

```
Chapter 7（Greenfield起点）
  → ECサイト新規開発プロジェクトを初期化

Chapter 8（Brownfieldサブシナリオ）
  → レガシーECサイト引き継ぎシナリオに切り替え
  → REを実行してコードベースを理解
  → Greenfieldシナリオに戻る

Chapter 9（Greenfield継続）
  → ECサイトの要件定義
  → requirements.mdを生成・承認

Chapter 10（Greenfield継続）
  → User Stories生成・整理
  → Workflow Planning で実行計画を確定

Chapter 11（Greenfield継続）
  → Application Design でアーキテクチャ設計
  → Units Generation でユニット分解
  → INCEPTIONフェーズ完了 → CONSTRUCTIONへ
```
