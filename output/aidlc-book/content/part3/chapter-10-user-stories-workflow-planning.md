# Chapter 10: User Stories と Workflow Planning

---

**この章で学ぶこと**

- AI-DLCにおけるUser Storiesの役割と「ストーリー」と「タスク」の違い
- 良いユーザーストーリーの3要素（Who / What / Why）
- Workflow Planningで実行計画を設計する方法
- スキップ判断の基準 — どのステージを省略してよいか

---

## 10.1 User Storiesの役割

### 10.1.1 AI-DLCにおけるUser Storiesの位置付け

User Storiesはアジャイル開発でおなじみの概念です。AI-DLCでも同様に、**ユーザーの視点からシステムに求める機能を表現する**ために使います。

ただし、AI-DLCでのUser Storiesには追加の役割があります。

> **ユーザーストーリーは、後のコード生成の「要件トレーサビリティ」の起点になる。**

CONSTRUCTIONフェーズで実際にコードを生成するとき、各コードが「どのストーリーを実現するために書かれたか」を追跡できます。これにより、「この機能は本当に必要か？」「どのストーリーに対応しているか？」を後から確認できます。

### 10.1.2 ストーリー vs タスク — 粒度の違い

混同しやすい「ストーリー」と「タスク」の違いを整理します。

| 観点 | ストーリー | タスク |
|------|---------|------|
| **主語** | ユーザー | 開発者 |
| **視点** | 「何を達成したいか」 | 「何を実装するか」 |
| **例** | 「商品をカートに追加したい」 | 「CartServiceのaddItemメソッドを実装する」 |
| **AI-DLCでの位置付け** | Inceptionフェーズ（What） | Constructionフェーズ（How） |

AI-DLCでは、**INCEPTIONでストーリーを定義し、CONSTRUCTIONでタスクに分解する**という2段構造を取ります。User Storiesはあくまで「何を作るか」の定義にとどめ、「どう作るか」はConstructionに委ねます。

### 10.1.3 良いユーザーストーリーの3要素

優れたユーザーストーリーは以下の構造を持ちます。

```
As a [Who: 誰が],
I want to [What: 何をしたいか],
So that [Why: なぜそれが必要か].
```

**BookCartの例**:

```
As a guest shopper（ゲスト購入者）,
I want to add products to my cart without registering（登録なしで商品をカートに追加したい）,
So that I can experience the purchase flow before deciding to create an account（アカウント作成を決める前に購入フローを体験できるように）.
```

「So that（なぜ）」を書くことが特に重要です。理由が明確だと、実装の優先度やUXの設計指針が定まります。

---

## 10.2 ハンズオン: BookCartのUser Stories生成

**目標**: 要件から自動生成されるストーリーを観察し、レビュー・修正する

### 10.2.1 User Stories自動生成の実行

Chapter 9でrequirements.mdを承認した状態から続けます。

Claude Codeに指示します。

```
User Storiesを生成してください。
```

Claude Codeが`requirements.md`の各機能要件からストーリーを自動生成します。

`aidlc-docs/inception/user-stories/user-stories.md`（抜粋）:

```markdown
# User Stories - BookCart

## US-01: 商品閲覧

**Story**: As a shopper, I want to browse products by category, so that I can discover items relevant to my interests.

**Acceptance Criteria**:
- カテゴリ一覧が表示される
- カテゴリを選択すると、該当商品が一覧表示される
- 各商品に名前・価格・在庫状況が表示される

---

## US-02: 商品検索

**Story**: As a shopper, I want to search for products by keyword, so that I can quickly find a specific item.

**Acceptance Criteria**:
- キーワードを入力すると検索結果が表示される
- 検索はタイトル・説明文を対象とする
- 検索結果がゼロ件の場合、適切なメッセージを表示する

---

## US-03: カート操作

**Story**: As a guest shopper, I want to add products to my cart, so that I can proceed to purchase.

**Acceptance Criteria**:
- 商品詳細ページから「カートに追加」できる
- 在庫切れ商品はカートに追加できない
- カートの合計金額がリアルタイムで更新される
```

### 10.2.2 ストーリーのレビューと修正

生成されたストーリーを読んで、以下の点を確認します。

**確認チェックリスト**:
- [ ] 重要な機能が抜け落ちていないか
- [ ] 不要なストーリーが含まれていないか（MVPスコープ外）
- [ ] Acceptance Criteriaが具体的で測定可能か
- [ ] 1ストーリーが大きすぎないか（分割が必要か）

**修正が必要な場合**:

```
US-05の「管理画面」ストーリーは今回のMVPスコープ外です。削除してください。
US-03の「カート操作」にAcceptance Criteriaを追加してください：
「カート内の商品数量を変更できる」
「カートから商品を削除できる」
```

---

> **[コラム] ストーリーのスキップ — いつ省略してよいか**
>
> AI-DLCでは、User Storiesステージをスキップすることができます。以下のケースでは省略を検討してください。
>
> **スキップを検討するケース**:
> - 個人開発・PoC（ストーリーを形式化するコストが効果を上回る）
> - 要件がすでに非常に詳細に定義されている（ストーリーへの変換が形式的になる）
> - 超小規模プロジェクト（ページ数が5以下など）
>
> **スキップしないべきケース**:
> - チーム開発（ストーリーが共通言語になる）
> - 長期プロジェクト（トレーサビリティが重要）
> - 非技術者が要件承認に関わる（ストーリー形式の方が伝わりやすい）

---

## 10.3 Workflow Planningとは

### 10.3.1 実行計画（execution-plan.md）の設計思想

User Storiesが確定したら、次は**Workflow Planning**です。

Workflow Planningでは、INCEPTIONからCONSTRUCTIONにかけてのステージをどの順序で実行するかを決めます。重要なのは、**すべてのステージを実行する必要はない**という点です。

> **「必要なステージだけを実行する」** — これがAI-DLCの「適応型ワークフロー」の本質です。

### 10.3.2 スキップ可能なステージの判断基準

| ステージ | スキップ可能なケース |
|---------|------------------|
| Reverse Engineering | Greenfieldプロジェクト（必須スキップ） |
| User Stories | 要件が自明、個人開発PoC |
| Application Design | 単純なCRUD、フロントエンドのみ |
| NFR Requirements | 非機能要件がほぼない小規模プロジェクト |
| NFR Design | NFR Requirementsをスキップした場合 |
| Infrastructure Design | フルマネージドサービスのみ使用、インフラ設計不要 |

BookCartの場合：

```
スキップ候補:
- Reverse Engineering → Greenfield のため必須スキップ
- NFR Requirements/Design → MVP段階のため、後回し
- Infrastructure Design → Vercelデプロイのためシンプル、スキップ可

実行ステージ:
- Requirements Analysis ✅（完了）
- User Stories ✅（完了）
- Workflow Planning（現在実行中）
- Application Design
- Units Generation
→ CONSTRUCTION フェーズへ
```

### 10.3.3 per-unit loopの設計

Workflow Planningのもうひとつの役割が、**per-unit loop**の設計です。

CONSTRUCTIONフェーズでは、各ユニット（Units Generationで定義するシステムの単位）に対して、以下のループを繰り返します。

```
[Unit N]
  ├── Functional Design（ビジネスロジック設計）
  ├── NFR Design（非機能要件設計、実行する場合）
  ├── Infrastructure Design（インフラ設計、実行する場合）
  └── Code Generation（コード生成）
```

ユニットの数と順序、どのサブステージを実行するかを、execution-plan.mdに明示します。

---

## 10.4 ハンズオン: BookCartの実行計画策定

**目標**: execution-plan.mdが生成される流れを観察し、承認する

### 10.4.1 Workflow Planningの実行

Claude Codeに指示します。

```
Workflow Planningを実行してください。
BookCartはMVPとして、NFR・インフラ設計はスキップします。
```

生成される`aidlc-docs/inception/plans/execution-plan.md`（抜粋）:

```markdown
# Execution Plan - BookCart

## スキップするステージ
- Reverse Engineering: Greenfieldのためスキップ
- NFR Requirements: MVPフェーズのためスキップ
- NFR Design: 同上
- Infrastructure Design: Vercelデプロイのためスキップ

## 実行するステージ

### INCEPTION
1. ✅ Requirements Analysis（完了）
2. ✅ User Stories（完了）
3. 🔵 Workflow Planning（実行中）
4. Application Design
5. Units Generation

### CONSTRUCTION（per-unit loop）
ユニット数: 未定（Units Generationで確定）

各ユニットに対して:
- Functional Design
- Code Generation

### OPERATIONS
- 今回のスコープ外
```

### 10.4.2 実行計画の確認と承認

生成された計画を確認して、スキップ・実行ステージが意図通りになっているか確認します。

問題なければ承認します。

```
確認しました。この計画で進めてください。
```

承認後、`aidlc-state.md`に計画が記録され、次のステージ（Application Design）への遷移が準備されます。

---

## まとめ

- **User Stories** はユーザー視点で「何を達成したいか」を記述する。良いストーリーは「Who / What / Why」の3要素を持つ。
- AI-DLCでは`requirements.md`からUser Storiesが自動生成される。生成後にレビュー・修正して品質を上げる。
- **Workflow Planning** は「どのステージを実行/スキップするか」を決める計画ステージ。すべてのステージを実行する必要はない。
- **per-unit loop** は、CONSTRUCTIONでユニットごとに設計→実装を繰り返すサイクル。ユニットの数と順序をここで定義する。
- 実行計画を承認することで、以降のAI-DLCが計画通りに動作することが保証される。

---

## チェックリスト

- [ ] Claude Codeに「User Storiesを生成して」と指示した
- [ ] 生成されたストーリーをレビューし、不要なものの削除・不足の追加を行った
- [ ] 各ストーリーにAcceptance Criteriaが含まれていることを確認した
- [ ] Workflow Planningを実行して`execution-plan.md`を生成した
- [ ] スキップ・実行ステージが意図通りになっているか確認した
- [ ] 実行計画を承認して`aidlc-state.md`が更新されたことを確認した
