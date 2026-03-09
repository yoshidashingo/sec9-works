# Chapter 8: Reverse Engineering — 既存コードベースの理解

---

**この章で学ぶこと**

- Reverse Engineeringが必要なシーンとその目的
- REで生成される3つの成果物と、それぞれの使い方
- Brownfieldプロジェクトでのワークスペース検出の違い
- レガシーECサイト引き継ぎシナリオでREを実際に実行する手順

---

> **シナリオ切り替え**
>
> ここからChapter 8の終わりまでは、**Brownfieldシナリオ**（レガシーECサイトの引き継ぎ）で進めます。Chapter 9からはGreenfieldシナリオ（BookCart新規開発）に戻ります。

---

## 8.1 Reverse Engineeringとは

### 8.1.1 BrownfieldプロジェクトでREが必要な理由

既存のコードベースを持つBrownfieldプロジェクトにAI-DLCを適用するとき、最初にぶつかる課題があります。

> **「AIがコードの文脈を理解していない」**

AIへの指示が「新機能を追加して」というシンプルなものであっても、AIは以下を知っておく必要があります。

- 現在のシステムはどういうアーキテクチャか
- どのファイルがどの役割を担っているか
- 既存の命名規則・パターンは何か
- どこに手を入れれば目的の機能が追加できるか

これらを「人間がすべて口頭で説明する」のは現実的ではありません。REはこの課題を解決します。AIが自律的にコードベースを分析して、構造を文書化します。その文書を以降のすべてのAI操作の「地図」として使います。

### 8.1.2 REで生成される3つの成果物

REを実行すると、以下の3ファイルが自動生成されます。

| ファイル | 内容 | 主な用途 |
|---------|------|---------|
| `code-map.md` | ディレクトリ構造とファイルの役割一覧 | 「どこに何があるか」の地図 |
| `dependency-analysis.md` | モジュール間の依存関係グラフ | 「変更の影響範囲」の把握 |
| `architecture-overview.md` | システム全体のアーキテクチャ概要 | 「全体像」の把握と引き継ぎドキュメント |

### 8.1.3 REの「深度」設定

REにはどこまで掘り下げるかを指示できます。

| 深度 | 内容 | 推奨シーン |
|------|------|----------|
| **浅い（Shallow）** | ディレクトリ構造と主要ファイルの概要のみ | 大規模コードベース、まず全体像だけ把握したいとき |
| **標準（Standard）** | ファイルの役割 + 主要関数・クラスの一覧 | 通常のBrownfieldプロジェクト |
| **深い（Deep）** | 関数レベルの分析 + 依存関係の詳細グラフ | 複雑なレガシーシステム、大規模リファクタリング前 |

Claude Codeへの指示例:
```
Reverse Engineeringを「標準深度」で実行してください。
```

---

## 8.2 サブシナリオ: レガシーECサイトを引き継いだ場合

### 8.2.1 シナリオ設定

あなたは新しいチームにアサインされました。引き継ぐのは3年前にリリースされた自社ECサイト「LegacyShop」です。

**状況**:
- 前任の開発者はすでに退職し、引き継ぎドキュメントはほとんどない
- テストコードは少なく、カバレッジは20%程度
- 新しい要件として「ポイントシステム」の追加を命じられた
- まず既存コードを理解することが急務

**テックスタック（レガシー）**:
```
LegacyShop/
├── src/
│   ├── routes/         # Express ルーティング
│   ├── controllers/    # コントローラー
│   ├── models/         # Sequelize ORM モデル
│   └── services/       # ビジネスロジック
├── migrations/         # データベースマイグレーション
├── package.json        # Node.js 16 + Express 4
└── .env.example
```

### 8.2.2 引き継ぎプロジェクトの主要ファイル概説

コードを触る前に、主要なファイルの役割を頭に入れておきましょう。

**`src/routes/`** — URLとコントローラーのマッピング

```typescript
// src/routes/products.ts
import { Router } from 'express'
import { ProductController } from '../controllers/ProductController'

const router = Router()
router.get('/', ProductController.list)
router.get('/:id', ProductController.findById)
router.post('/', ProductController.create)

export default router
```

**`src/models/`** — データベースのテーブル定義（Sequelize）

```typescript
// src/models/Order.ts
import { Model, DataTypes } from 'sequelize'

class Order extends Model {
  public id!: number
  public customerId!: number
  public totalAmount!: number
  public status!: 'pending' | 'paid' | 'shipped' | 'delivered'
}

Order.init({
  id: { type: DataTypes.INTEGER, primaryKey: true, autoIncrement: true },
  customerId: { type: DataTypes.INTEGER, allowNull: false },
  totalAmount: { type: DataTypes.DECIMAL(10, 2), allowNull: false },
  status: { type: DataTypes.ENUM('pending', 'paid', 'shipped', 'delivered') },
}, { sequelize, tableName: 'orders' })
```

---

> **[コラム] 「技術的負債」をAI-DLCでどう扱うか**
>
> 引き継いだコードベースには、しばしば「技術的負債」が溜まっています。命名が一貫していない、テストがない、ドキュメントがない、といった問題です。
>
> AI-DLCのREは、こうした技術的負債を「可視化」します。code-map.mdを見れば、ドキュメントのないモジュールがどこかわかります。dependency-analysis.mdを見れば、スパゲッティ状の依存関係が浮かび上がります。
>
> REの目的は「コードを完璧にすること」ではありません。「AIが安全に作業できる地図を作ること」です。負債の返済はCONSTRUCTIONフェーズのリファクタリングタスクとして計画するのが正しいアプローチです。

---

## 8.3 ハンズオン: Reverse Engineeringの実行

### 8.3.1 BrownfieldとしてWorkspace Detectionを実行する

**目標**: Claude CodeがBrownfieldと判定し、REを提案する流れを観察する

LegacyShopのリポジトリをクローンして、Claude Codeを起動します。

```bash
git clone https://github.com/your-username/legacyshop.git
cd legacyshop
```

CLAUDE.mdを作成します。

```markdown
# CLAUDE.md - LegacyShop

## プロジェクト概要

既存ECサイト（Node.js + Express + MySQL）。新機能追加中。

## AI-DLC 設定

- ワークフロー: `.steering/aws-aidlc-rules/core-workflow.md`
```

Claude Codeに指示します。

```
AI-DLCを開始してください。このリポジトリは既存のECサイトです。
```

**確認ポイント**:
- `Project Type: Brownfield`と判定されるか
- `Reverse Engineering Needed: Yes`と記録されるか
- 「次はReverse Engineeringを実行しますか？」と提案されるか

もしGreenfieldと誤判定された場合は、明示的に伝えます。

```
このプロジェクトはBrownfieldです。既存コードのReverse Engineeringを実行してください。
```

### 8.3.2 生成成果物の確認

**目標**: REで生成された3ファイルを読み、コードベースへの理解を深める

REの実行を指示します。

```
Reverse Engineeringを標準深度で実行してください。
```

Claude Codeがコードベースを分析し、以下のファイルを生成します。

**`aidlc-docs/inception/reverse-engineering/code-map.md` の例**:

```markdown
# Code Map - LegacyShop

## ディレクトリ構造

src/
├── routes/         # ルーティング（5ファイル）
│   ├── products.ts    # 商品一覧・詳細・作成
│   ├── orders.ts      # 注文作成・一覧・詳細
│   ├── customers.ts   # 顧客登録・ログイン
│   ├── cart.ts        # カート操作
│   └── payments.ts    # 決済処理
├── controllers/    # コントローラー（5ファイル）
├── models/         # Sequelizeモデル（6ファイル）
│   ├── Product.ts, Order.ts, OrderItem.ts
│   ├── Customer.ts, Cart.ts, CartItem.ts
└── services/       # ビジネスロジック（4ファイル）
    ├── ProductService.ts   # 在庫管理含む
    ├── OrderService.ts     # 注文処理・ステータス管理
    ├── CartService.ts      # カート操作
    └── PaymentService.ts   # 外部決済API連携
```

**`aidlc-docs/inception/reverse-engineering/dependency-analysis.md` の例**:

```markdown
# Dependency Analysis - LegacyShop

## 依存関係グラフ（主要）

routes → controllers → services → models

## 高依存モジュール（注意が必要）

OrderService:
  - 依存先: ProductService（在庫確認）, CartService（カート取得）,
            PaymentService（決済実行）, Order, OrderItem（DB操作）
  - 変更時の影響範囲: 広い（注文処理全体）

## 外部依存

PaymentService → Stripe API（外部決済）
OrderService → nodemailer（メール通知）
```

### 8.3.3 REの結果をRequirements Analysisに活かす

ポイントシステムを追加するにあたり、REの成果物から以下が判明しました。

- `Customer`モデルに`pointBalance`フィールドを追加する必要がある
- `OrderService`が注文確定後にポイントを付与する責務を持つべき
- 外部依存（Stripe, nodemailer）があるため、テストのモック設計が必要

この情報を元に、Requirements Analysisで「ポイントシステムの要件」を定義します。

---

> **シナリオ終了**
>
> Chapter 9からはGreenfieldシナリオ（BookCart新規開発）に戻ります。

---

## まとめ

- **Reverse Engineering** はBrownfieldプロジェクト専用のステージ。AIが安全に作業するための「地図」を作る。
- REで生成される **`code-map.md`・`dependency-analysis.md`・`architecture-overview.md`** の3ファイルが、以降のすべてのAI操作のベースラインとなる。
- **深度設定**（浅い/標準/深い）によって分析の詳細度をコントロールできる。
- REの目的は「技術的負債を完璧に解消すること」ではなく、「AIが安全に作業できる状態にすること」である。
- REの成果物はRequirements Analysisで引き継がれ、新機能の影響範囲判断に使われる。

---

## チェックリスト

- [ ] BrownfieldとしてWorkspace Detectionを実行し、`Project Type: Brownfield`を確認した
- [ ] Reverse Engineeringを実行して`code-map.md`を生成した
- [ ] `dependency-analysis.md`で高依存モジュールを特定した
- [ ] `architecture-overview.md`でシステム全体像を把握した
- [ ] REの結果から、新機能追加の影響範囲を判断できた
