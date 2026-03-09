# Functional Design Plan - Unit 4: Part IV（Constructionフェーズ・構築編）

## ユニット概要

- **対象**: Part IV - Constructionフェーズ（構築編）
- **章構成**: Chapter 12〜16（5章）
- **想定ページ数**: 65〜75ページ
- **執筆順序**: 2番目（Unit 3の次）
- **前提**: Unit 3で完了したBookCart（TypeScript + Next.js）のINCEPTIONを引き継ぐ

## 設計ステップ

### Step 1: ユニットコンテキスト分析
- [x] unit-of-work.md から Unit 4 の定義・責務を確認
- [x] unit-of-work-story-map.md から FR-04 の全要件項目を確認

### Step 2: 詳細目次の設計（節・項レベル）
- [ ] Chapter 12: Functional Design の節構成を定義
- [ ] Chapter 13: NFR Requirements & Design の節構成を定義
- [ ] Chapter 14: Infrastructure Design の節構成を定義
- [ ] Chapter 15: Code Generation の節構成を定義
- [ ] Chapter 16: Build and Test の節構成を定義

### Step 3: チュートリアル設計（BookCartのCONSTRUCTIONシナリオ）
- [ ] どのユニットのCONSTRUCTIONを例として使うかを確定
- [ ] Chapter 13（NFR）と実行計画（NFRスキップ）の整合方針を確定
- [ ] Chapter 14（インフラ）と実行計画（インフラスキップ）の整合方針を確定
- [ ] Chapter 15のコードサンプル方針を確定

### Step 4: 章の構成スタイルを確定
- [ ] Unit 3と同じフォーマットで統一（この章で学ぶこと/まとめ/チェックリスト/コラム）

### Step 5: 成果物生成
- [ ] `business-logic-model.md` — 各章の詳細目次・コンテンツフロー
- [ ] `business-rules.md` — 執筆ルール・スタイルガイド（Unit 4向け）
- [ ] `domain-entities.md` — 登場概念・用語定義・相互関係

---

## 質問

### Q1: CONSTRUCTIONのハンズオンで扱うユニット

Part IV（Constructionフェーズ）のチュートリアルで、BookCartの4ユニット（Unit 3で定義）のうち、どれを例として使いますか？

A) Unit 1（商品・カタログ）— 最もシンプル。Functional Design → Code Generation の流れを学ぶのに最適
B) Unit 2（カート・注文）— ビジネスロジックが豊富。NFRや状態管理の説明にも使いやすい
C) 各章でそれぞれ違うユニットを使う（Ch12はUnit 1、Ch13はUnit 2など）
D) Unit 1のFunctional Designを示した後、Code Generationの段階ではUnit 1のProductServiceを完全実装する

[Answer]:

---

### Q2: Chapter 13（NFR Requirements & Design）の教え方

BookCartの実行計画ではNFRをスキップしていますが、書籍としてはNFRの扱い方を教える必要があります。どう整合させますか？

A) 「BookCartのMVP段階ではスキップしたが、本来は実施すべき」と明記し、仮想のNFR定義と設計を示す（実際には適用しないが教育目的で記述）
B) BookCartとは別のサンプル（本番サービスの例）を使って、NFRの定義・設計方法を解説する
C) NFRの概念解説とルールファイルの説明に特化し、ハンズオンは最小限にする（「実際にはこのコマンドを実行する」程度）

[Answer]:

---

### Q3: Chapter 14（Infrastructure Design）の教え方

同様にBookCartの実行計画ではInfrastructure Designをスキップしています。どう扱いますか？

A) Vercelデプロイという選択をした理由を逆説的に解説（「Vercelを使うとInfra Designが不要になる」という観点）し、AWSを使う場合のInfra Designを参考として示す
B) Chapter 13と同様に、仮想の本番環境（AWS）を想定してInfra Designのハンズオンを行う
C) インフラ設計の概念解説のみ行い、ハンズオンは行わない

[Answer]:

---

### Q4: Chapter 15（Code Generation）のコードサンプル方針

Code Generationの「計画→生成の2段階プロセス」を示すにあたり、コードサンプルの方針を教えてください。

A) 2段階プロセスの流れ（計画ファイル生成→コード生成の指示）を示し、生成されるコードは抜粋のみ（プロセスの理解を優先）
B) ProductServiceの実装コードを完全に示す（コードの品質・パターンを確認できる）
C) Claude Codeへの指示プロンプトと、それに対するレスポンス例を中心に示す（AIとの対話パターンを学ぶ）

[Answer]:

---

### Q5: Chapter 16（Build and Test）のテスト対象

Build and Testで示すテストの種類と対象を教えてください（複数選択可）。

A) ユニットテスト（ProductService等のビジネスロジック）
B) 統合テスト（APIルートとDBの結合）
C) E2Eテスト（Playwrightでの画面操作テスト）
D) テスト指示の生成フロー（「テストを書いて」という指示からテストコードが生成される様子）
E) CI/CD連携（GitHub Actionsでのテスト自動化）

複数の場合はカンマ区切りで（例：A,D）

[Answer]:

---

**回答方法**: 各質問の `[Answer]:` タグの後に回答を記入してください。
