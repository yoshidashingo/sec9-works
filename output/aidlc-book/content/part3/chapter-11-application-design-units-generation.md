# Chapter 11: Application Design と Units Generation

---

**この章で学ぶこと**

- Application Designの役割と「過剰設計しない」原則
- Units Generationによるシステムの単位分解の考え方
- マイクロサービス vs モノリス — どちらを選ぶか
- BookCartをユニットに分解してCONSTRUCTIONフェーズの準備を整える
- INCEPTIONフェーズの完了とCONSTRUCTIONへの引き継ぎ

---

## 11.1 Application Designの役割

### 11.1.1 高レベルコンポーネント設計とは

Application Designは、システム全体の「見取り図」を作るステージです。

ここで設計するのは **高レベル** のコンポーネント構成です。クラスの詳細、メソッドのシグネチャ、データベースのカラム定義といった細かい部分は、CONSTRUCTIONフェーズのFunctional DesignとCode Generationで決まります。

Application Designで決めること：
- システムはどのコンポーネント（サービス・モジュール）で構成されるか
- 各コンポーネントの責務は何か
- コンポーネント間のインターフェース（APIエンドポイント等）の概要

### 11.1.2 AI-DLCにおける「過剰設計しない」原則

ソフトウェア開発には「YAGNI（You Aren't Gonna Need It）」という原則があります。今必要でない機能を事前に作り込むな、という意味です。AI-DLCはこの原則を設計にも適用します。

> **「今決める必要がないことは、決めない。」**

Application Designの段階でデータベースのインデックス設計やキャッシュ戦略を細かく決める必要はありません。それはCONSTRUCTIONフェーズで、実際に実装しながら決めれば良いのです。

過剰設計を避けることで：
- 設計の変更コストが下がる（詳細を決めるほど変更が難しくなる）
- CONSTRUCTIONフェーズでAIが柔軟に最適解を選べる
- INCEPTIONフェーズの時間を短縮できる

### 11.1.3 Application Designで設計する対象の範囲

BookCartの場合、以下を設計します。

| 設計対象 | 内容 |
|---------|------|
| アーキテクチャパターン | モノリス or マイクロサービス |
| 主要コンポーネント | ページ、APIルート、サービス層、データ層 |
| 外部サービス連携 | 決済、メール、ストレージ |
| データフローの概要 | 商品閲覧→カート→注文→決済の主要フロー |

---

## 11.2 ハンズオン: BookCartのApplication Design

**目標**: コンポーネント設計が自動生成される流れを観察する

### 11.2.1 Application Designの実行

Claude Codeに指示します。

```
Application Designを実行してください。
BookCartはNext.jsのフルスタックアプリ（モノリス）として設計します。
外部サービスはStripe（決済）とSendGrid（メール通知）を使います。
```

Claude Codeがコンポーネント設計を生成します。

`aidlc-docs/inception/application-design/application-design.md`（抜粋）:

```markdown
# Application Design - BookCart

## アーキテクチャ

**パターン**: モノリシック（Next.js フルスタック）
**デプロイ**: Vercel（フロント + APIルート）+ Vercel Postgres

## コンポーネント構成

### フロントエンド（Next.js App Router Pages）
- `/` — トップページ（商品フィーチャー）
- `/products` — 商品一覧
- `/products/[id]` — 商品詳細
- `/cart` — カート
- `/checkout` — 注文確認・決済
- `/orders` — 注文履歴（会員のみ）
- `/admin` — 管理画面（管理者のみ）

### APIルート（Next.js Route Handlers）
- `GET /api/products` — 商品一覧取得
- `POST /api/cart/items` — カートアイテム追加
- `POST /api/orders` — 注文作成
- `POST /api/orders/[id]/payment` — 決済処理

### サービス層
- ProductService — 商品・在庫管理
- CartService — カート操作
- OrderService — 注文処理・ステータス管理
- PaymentService — Stripe連携

### データ層
- Vercel Postgres + Prisma ORM
- 主要テーブル: products, customers, carts, cart_items, orders, order_items

### 外部サービス
- **Stripe** — クレジットカード決済
- **SendGrid** — 購入確認メール・注文更新通知
```

### 11.2.2 成果物のレビュー

生成されたApplication Designを確認します。

**確認ポイント**:
- 要件（requirements.md）のすべての機能が設計に含まれているか
- コンポーネントの責務が明確で、重複していないか
- 外部サービスとの連携方法が適切か

修正が必要な場合は Claude Codeに伝えます。

```
SendGridのかわりにResendを使いたいです。変更してください。
```

---

## 11.3 Units Generation によるタスク分解

### 11.3.1 ユニット分解の考え方

Application Designでシステムの全体像が決まったら、次は**Units Generation**です。

Units Generationでは、システムを「ユニット」に分解します。ユニットとは、CONSTRUCTIONフェーズで独立して設計・実装できる作業の単位です。

ユニットの分解戦略は、アーキテクチャによって異なります。

| アーキテクチャ | ユニットの単位 | 例 |
|-------------|-------------|-----|
| **マイクロサービス** | 独立デプロイ可能なサービス | user-service, product-service, order-service |
| **モノリス（大規模）** | 機能ドメイン | 商品管理, カート・注文, 管理機能 |
| **モノリス（小〜中規模）** | アプリ全体を1ユニット | 全機能をひとつのユニットで扱う |

BookCartはNext.jsのモノリスかつ中規模なので、**機能ドメイン単位**で分解します。

### 11.3.2 依存関係の整理

ユニットを分解したら、ユニット間の依存関係を整理します。

```
Unit 1（商品・カタログ）→ Unit 2（カート・注文）が依存
                         ↓
                    Unit 3（決済・通知）が依存
```

依存関係が明確になると、**実装順序**が決まります。依存される側のユニットを先に実装することで、後のユニットがそれを利用できます。

### 11.3.3 実装順序の決定

依存関係を元に実装順序を決めます。

```
1番目: Unit 1（商品・カタログ）← 依存なし
2番目: Unit 2（カート・注文）← Unit 1完成後
3番目: Unit 3（決済・通知）← Unit 2完成後
4番目: Unit 4（管理機能）← Unit 1完成後（Unit 2・3と並行可能）
```

---

> **[コラム] ユニットの粒度 — 大きすぎず小さすぎず**
>
> ユニット分解でよく起きる失敗が「粒度の誤り」です。
>
> **粒度が大きすぎる場合**: 1ユニットが大きすぎると、Functional DesignとCode Generationが長大になり、進捗が見えにくくなります。Claude Codeのコンテキストウィンドウを圧迫する可能性もあります。
>
> **粒度が小さすぎる場合**: ユニット間のインターフェース設計が複雑になり、かえって管理コストが増えます。
>
> **目安**: 1ユニットのCode Generationが「1〜2セッション（1〜3時間）で完了する」くらいの粒度が適切です。機能の数で言うと、ユーザーストーリー3〜8本程度が1ユニットに対応するイメージです。

---

## 11.4 ハンズオン: BookCartのユニット分解

**目標**: ユニット分解の計画と成果物を生成する

### 11.4.1 Units Generationの実行

Claude Codeに指示します。

```
Units Generationを実行してください。
機能ドメイン単位で分解し、User Storiesとのマッピングも作成してください。
```

Claude Codeがユニット分解計画（質問ファイル）を生成します。

```markdown
# Unit of Work Plan - BookCart

### Q1: ユニット分解の方針

BookCartを何ユニットに分解しますか？

A) 3ユニット（商品/カート・注文/決済・通知）
B) 4ユニット（商品/カート/注文/決済・通知・管理）
C) 2ユニット（ショッピング機能/管理機能）

[Answer]:
```

回答例:

```markdown
[Answer]:B
（管理機能を独立ユニットにして、後から追加しやすくしたい）
```

### 11.4.2 生成成果物の確認

承認後、以下の3ファイルが生成されます。

**`unit-of-work.md`**（抜粋）:

```markdown
# Unit of Work - BookCart

## Unit 1: 商品・カタログ（Product Catalog）

**責務**: 商品データの管理、カテゴリ管理、商品検索
**User Stories**: US-01（商品閲覧）, US-02（商品検索）
**ページ数見積もり**: 約30ページ相当のコード

---

## Unit 2: カート・注文（Cart & Order）

**責務**: カート操作、注文作成、注文履歴
**User Stories**: US-03（カート操作）, US-04（注文確定）, US-07（注文履歴）
**ページ数見積もり**: 約40ページ相当のコード

---
```

**`unit-of-work-dependency.md`**（抜粋）:

```markdown
# Unit Dependency

| ユニット | 依存するユニット | 実装順序 |
|---------|-------------|--------|
| Unit 1（商品） | なし | 1番目 |
| Unit 2（カート・注文） | Unit 1 | 2番目 |
| Unit 3（決済・通知） | Unit 2 | 3番目 |
| Unit 4（管理機能） | Unit 1 | 2番目（Unit 2と並行可） |
```

**`unit-of-work-story-map.md`** で、全User StoriesがいずれかのUnitに割り当てられていることを確認します。

## 11.5 INCEPTIONフェーズの完了

### 11.5.1 CONSTRUCTIONへの引き継ぎチェックリスト

INCEPTIONフェーズで作成した成果物が、すべてCONSTRUCTIONフェーズに引き継がれます。

| 成果物 | パス | CONSTRUCTIONでの役割 |
|-------|------|-------------------|
| `requirements.md` | `inception/requirements/` | 機能要件の参照元 |
| `user-stories.md` | `inception/user-stories/` | 要件トレーサビリティの基点 |
| `execution-plan.md` | `inception/plans/` | 実行するステージの指針 |
| `application-design.md` | `inception/application-design/` | コンポーネント設計の参照元 |
| `unit-of-work.md` | `inception/application-design/` | 各ユニットの定義・責務 |
| `unit-of-work-dependency.md` | `inception/application-design/` | 実装順序の根拠 |

### 11.5.2 aidlc-state.mdの最終確認

`aidlc-state.md`でINCEPTIONフェーズのすべてのステージが完了していることを確認します。

```markdown
### 🔵 INCEPTION PHASE
- [x] Workspace Detection
- [x] Requirements Analysis
- [x] User Stories
- [x] Workflow Planning
- [x] Application Design
- [x] Units Generation
```

すべてに`[x]`がついていれば、INCEPTIONフェーズ完了です。

Claude Codeに伝えます。

```
Units Generationの成果物を承認します。CONSTRUCTIONフェーズに進んでください。
```

### 11.5.3 Part IIIのまとめ — INCEPTIONで何を準備したか

Part IIIを通じて、BookCartプロジェクトのINCEPTIONフェーズを完了しました。

**INCEPTIONで決めたこと**:

```
1. プロジェクトの種別 → Greenfield（新規開発）
2. 要件 → 商品・カート・注文・決済・ゲスト購入・管理機能
3. ユーザーストーリー → 12本のUser Stories
4. 実行計画 → NFR・インフラ設計はスキップ、4ユニットで開発
5. アーキテクチャ → Next.jsモノリス + Vercel + Stripe + Resend
6. ユニット分解 → 4ユニット（商品/カート・注文/決済・通知/管理）
```

Part IVでは、これらの成果物を元に、実際にコードを生成するCONSTRUCTIONフェーズに入ります。

---

## まとめ

- **Application Design** はシステムの「見取り図」を作るステージ。詳細設計はCONSTRUCTIONに委ねる「過剰設計しない」原則が重要。
- **Units Generation** は、システムをCONSTRUCTIONで独立して実装できる「ユニット」に分解する。粒度はUser Stories 3〜8本 = 1ユニットが目安。
- 依存関係（`unit-of-work-dependency.md`）が実装順序を決める。依存される側のユニットを先に実装する。
- INCEPTIONで作成した成果物（requirements.md, user-stories.md, unit-of-work.md等）は、すべてCONSTRUCTIONの各ステージで参照される。
- `aidlc-state.md`の全ステージが`[x]`になったことを確認して、正式にCONSTRUCTIONへ移行する。

---

## チェックリスト

- [ ] Application Designを実行して`application-design.md`を生成した
- [ ] アーキテクチャパターン（モノリス）と主要コンポーネントが設計に含まれていることを確認した
- [ ] Units Generationを実行してユニット分解計画の質問に回答した
- [ ] `unit-of-work.md`でユニットの定義・責務を確認した
- [ ] `unit-of-work-dependency.md`で依存関係と実装順序を確認した
- [ ] `unit-of-work-story-map.md`で全User StoriesがいずれかのUnitに割り当てられていることを確認した
- [ ] `aidlc-state.md`でINCEPTIONフェーズの全ステージが完了（`[x]`）していることを確認した
- [ ] Claude Codeに「CONSTRUCTIONフェーズに進んでください」と指示した
