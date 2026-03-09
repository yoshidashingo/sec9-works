# AI-DLCを完全理解する 第11回: constructionディレクトリ徹底解説 ― 実装フェーズの6ファイル

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - constructionの最初の5ファイルは「per-unit」で実行され、Per-Unit Loopの骨格を形成する
> - code-generation.mdは「Brownfieldではコピーファイル禁止」という明確なルールを持つ
> - build-and-test.mdは6種類のテスト (unit / integration / performance / e2e / contract / security) を定義する
> - Per-Unit Loopの5ファイルに「標準化された2択メッセージ」が規定されている

---

## constructionディレクトリの概観

constructionディレクトリには、CONSTRUCTIONフェーズの6つのステージに対応する6つのルールファイルが格納されています。

| # | ファイル | 行数 | ステップ数 | 分類 |
|---|---------|------|----------|------|
| 1 | functional-design.md | 113 | 9 | CONDITIONAL |
| 2 | nfr-requirements.md | 100 | 9 | CONDITIONAL |
| 3 | nfr-design.md | 91 | 9 | CONDITIONAL |
| 4 | infrastructure-design.md | 95 | 9 | CONDITIONAL |
| 5 | code-generation.md | 208 | 16 | ALWAYS |
| 6 | build-and-test.md | 355 | 10 | ALWAYS |

inceptionディレクトリと比べて2つの特徴があります。1つ目は**ファイルサイズの均一性**です。inceptionが94行〜480行と大きな幅があったのに対し、constructionは91行〜355行と差が小さくなっています。2つ目は**ステップ数の9ステップ収束**です。最初の4ファイルはすべて9ステップで構成されています。この均一性は、Per-Unit Loop内で同じリズムが繰り返される設計を反映していると考えられます。

---

## Per-Unit Loopの内側

第5回と第8回で解説したPer-Unit Loopの構造を、ルールファイルの視点から見直してみましょう。

```
ユニットA → [functional-design → nfr-requirements → nfr-design → infrastructure-design → code-generation]
ユニットB → [functional-design → nfr-requirements → nfr-design → infrastructure-design → code-generation]
全ユニット完了 → build-and-test
```

最初の4ファイル (functional-design〜infrastructure-design) は、すべてCONDITIONALでありper-unitで実行されます。code-generationはALWAYSかつper-unit。build-and-testはALWAYSですがper-unitではなく、全ユニットの完了後に1回だけ実行されます。

---

## 1. functional-design.md: 技術非依存のビジネスロジック

### 9ステップの構造

functional-design.mdは9ステップで構成されます:

1. ユニットコンテキストの分析
2. Functional Design計画の作成
3. コンテキスト適応型の質問生成
4. 計画の保存
5. 回答の収集と分析
6. 成果物の生成
7. 完了メッセージの提示
8. 明示的承認の待機
9. 承認記録と進捗更新

この9ステップはnfr-requirements.md、nfr-design.md、infrastructure-design.mdでもほぼ同一です。

### 3つの成果物

第5回で概念的に解説した3つの成果物が、ここでファイルパス付きで定義されています:

- `{unit-name}/functional-design/business-logic-model.md`
- `{unit-name}/functional-design/business-rules.md`
- `{unit-name}/functional-design/domain-entities.md`

### 7つの質問カテゴリ

質問カテゴリは7つ定義されています:

1. **Business Logic Modeling** ― コアエンティティ、ワークフロー、データ変換
2. **Domain Model** ― ドメイン概念、エンティティ関係、データ構造
3. **Business Rules** ― 決定ルール、バリデーションロジック、制約
4. **Data Flow** ― データの入出力、変換、永続化
5. **Integration Points** ― 外部システムとの連携
6. **Error Handling** ― エラーシナリオ、バリデーション失敗、例外処理
7. **Business Scenarios** ― エッジケース、代替フロー、複雑な状況

各カテゴリには「evaluate ALL categories」と指示されています。第9回で解説したoverconfidence-prevention.mdと同様の「すべてのカテゴリを評価せよ」という方針が、functional-design.md自身にも記述されています。

---

## 2-3. nfr-requirements.md と nfr-design.md: 品質の2段階設計

### NFR Requirements (9ステップ) 

第5回で解説した8つの質問カテゴリが、ルールファイルでは以下のように定義されています:

1. Scalability Requirements
2. Performance Requirements
3. Availability Requirements
4. Security Requirements
5. Tech Stack Selection
6. Reliability Requirements
7. Maintainability Requirements
8. Usability Requirements

成果物は2つ:
- `{unit-name}/nfr-requirements/nfr-requirements.md`
- `{unit-name}/nfr-requirements/tech-stack-decisions.md`

### NFR Design (9ステップ) 

NFR Designの質問カテゴリは5つ:

1. Resilience Patterns
2. Scalability Patterns
3. Performance Patterns
4. Security Patterns
5. Logical Components

ここで興味深い違いがあります。NFR RequirementsではALL categoriesの評価が求められますが、NFR Designでは「Use the categories below as inspiration, NOT as a mandatory checklist. Skip entire categories if not applicable」と書かれています。要件段階ではすべてのカテゴリについて体系的に聞き、設計段階では必要なパターンだけを選びます。この非対称性は、要件段階ではすべてのカテゴリを評価し、設計段階では該当するものだけを選ぶという使い分けによるものです。

成果物は2つ:
- `{unit-name}/nfr-design/nfr-design-patterns.md`
- `{unit-name}/nfr-design/logical-components.md`

---

## 4. infrastructure-design.md: 論理から物理へ

### 「推奨」という前提条件

infrastructure-design.mdの前提条件に注目してください:

```markdown
- Functional Design must be complete for the unit
- NFR Design recommended (provides logical components to map)
```

Functional Designは「must be complete」ですが、NFR Designは「recommended」です。つまり、NFR DesignをスキップしてもInfrastructure Designは実行できます。この違いは、機能設計がインフラ設計の論理的な前提であるのに対し、NFR設計は品質面の補強であり必須ではないことを意味します。Per-Unit Loop内のステージは固定順序ですが、CONDITIONALステージのスキップにより実際の経路は変わりえます。

### 成果物

成果物は2〜3つ:
- `{unit-name}/infrastructure-design/infrastructure-design.md`
- `{unit-name}/infrastructure-design/deployment-architecture.md`
- `shared-infrastructure.md` (共有インフラがある場合のみ) 

3つ目の`shared-infrastructure.md`はユニット固有ではなくconstruction/直下に配置されます。複数ユニットが共通のインフラ (VPC、ロードバランサーなど) を使う場合の設計を一元管理するためです。

---

## 5. code-generation.md: 計画→承認→生成

### 2部構成

code-generation.mdもuser-stories.md、units-generation.mdと同じくPart 1 (Planning: Step 1〜9) とPart 2 (Generation: Step 10〜16) の2部構成です。

### 計画の具体性

Step 2の計画作成では、生成するコードの種類が具体的に列挙されています:

1. Project Structure Setup (Greenfieldのみ) 
2. Business Logic Generation
3. Business Logic Unit Testing
4. Business Logic Summary
5. API Layer Generation
6. API Layer Unit Testing
7. API Layer Summary
8. Repository Layer Generation
9. Repository Layer Unit Testing
10. Repository Layer Summary
11. Database Migration Scripts
12. Documentation Generation
13. Deployment Artifacts Generation

各層 (Business Logic / API Layer / Repository Layer) が「生成→テスト→サマリー」の3点セットで構成されています。

テストはCode Generationの段階で生成され、Build and Testの段階で実行されます。「テストを書く」と「テストを走らせる」が分離されている設計です。

### Brownfieldの「コピーファイル禁止」ルール

code-generation.mdで最も注目すべきルールがこれです:

```markdown
- **If file exists**: Modify it in-place
  (never create `ClassName_modified.java`, `ClassName_new.java`, etc.)
- **If file doesn't exist**: Create new file
```

Brownfieldプロジェクトで既存ファイルを変更する場合、ファイルを「その場で修正」します。`ClassName_modified.java`や`ClassName_new.java`のようなコピーファイルを作ってはなりません。

なぜこのルールが必要なのか。AIによるコード生成では、既存ファイルの変更を避けて新しいファイルにコピーを作り、そこで変更を加えるという「安全な」パターンに陥りがちです。しかしこのパターンは、元のファイルとコピーの二重管理を生み、ビルドの混乱やテストの不整合を引き起こします。「その場で修正」をルールとして規定することで、これらの問題を抑制する設計になっています (ただしプロンプト指示であるため、AIの振る舞いを技術的に保証するものではありません) 。

Step 12にも検証ルールがあります: 「Brownfield only: Verify no duplicate files created (Brownfieldのみ: 重複ファイルが作成されていないことを検証せよ) 」。生成後のチェックまで含めた2段階のルールです。

### コード配置のルール

Code Location Rulesとして、プロジェクトタイプ別のディレクトリ構造が定義されています:

| プロジェクトタイプ | コード配置 |
|-----------------|---------|
| **Brownfield** | 既存構造をそのまま使用 |
| **Greenfield単一ユニット** | `src/`, `tests/`, `config/` |
| **Greenfieldマイクロサービス** | `{unit-name}/src/`, `{unit-name}/tests/` |
| **Greenfieldモノリス** | `src/{unit-name}/`, `tests/{unit-name}/` |

マイクロサービスとモノリスでディレクトリの階層が逆になる点に注意してください。マイクロサービスはユニットがトップレベルで、その下にsrc/tests。モノリスはsrc/testsがトップレベルで、その下にユニット。

---

## 6. build-and-test.md: 6種類のテスト戦略

### ループの外側

build-and-test.mdはPer-Unit Loopの外側に位置する唯一のステージです。全ユニットのCode Generationが完了した後、1回だけ実行されます。

### 6種類のテスト

build-and-test.mdが定義するテストは6種類です:

| # | テスト種別 | 成果物 | 備考 |
|---|---------|--------|------|
| 1 | Unit Tests | unit-test-instructions.md | Code Generation段階で生成済み |
| 2 | Integration Tests | integration-test-instructions.md | ユニット間の連携テスト |
| 3 | Performance Tests | performance-test-instructions.md | 負荷・ストレステスト |
| 4 | End-to-End Tests | e2e-test-instructions.md | 完全なユーザーワークフロー |
| 5 | Contract Tests | contract-test-instructions.md | マイクロサービス向け |
| 6 | Security Tests | security-test-instructions.md | 脆弱性スキャン、認証テスト |

1〜3はbuild-and-test.mdの個別ステップ (Steps 2〜5) として定義されており、4〜6はStep 6で「Based on project requirements」として要件に応じて生成されます。

### 5つの成果物

最終的に生成される成果物は5つ (＋要件に応じた追加テスト手順書) :

1. `build-instructions.md` ― ビルド手順 (依存関係インストール〜ビルド実行〜検証) 
2. `unit-test-instructions.md` ― ユニットテスト実行手順
3. `integration-test-instructions.md` ― 結合テスト手順
4. `performance-test-instructions.md` ― パフォーマンステスト手順
5. `build-and-test-summary.md` ― ビルド・テスト結果の総合サマリー

build-and-test-summary.mdの末尾には「Ready for Operations: [Yes/No]」という判定項目があります。すべてのテストが通過すればOPERATIONSフェーズへの準備完了、失敗があれば修正してリビルドします。

---

## constructionディレクトリに共通するパターン

### 統一された完了メッセージ

第8回で解説した「MANDATORY: Present standardized 2-option completion message」が、Per-Unit Loop内の5ファイル (functional-design〜code-generation) に定義されています。完了メッセージの構造は以下の通りです:

1. **Completion Announcement**: `# [emoji] [Stage Name] Complete - [unit-name]`
2. **AI Summary**: 成果物の要約 (箇条書き) 
3. **Formatted Workflow Message**: 2択の選択肢

2択は常に「Request Changes (変更を依頼する) 」と「Continue to Next Stage (次のステージに進む) 」です。第8回で述べた通り、core-workflow.mdの「NO EMERGENT BEHAVIOR」原則と各ステージの実行ステップにより、AIが独自に3択目を作り出すことは認められていません。

なお、build-and-test.mdはPer-Unit Loopの外側にあるため、この2択形式ではなく「Ready to proceed to Operations stage?」という形式の完了メッセージを使用します。

### 前提条件の段階的依存

各ステージの前提条件を追うと、段階的な依存関係が見えます:

```
functional-design    → Units Generation complete, Application Design recommended
nfr-requirements     → Functional Design complete
nfr-design           → NFR Requirements complete
infrastructure-design → Functional Design complete, NFR Design recommended
code-generation      → Unit Design Generation complete, NFR Implementation complete (if executed)
build-and-test       → Code Generation complete for ALL units
```

NFR DesignやInfrastructure Designをスキップしても、Code Generationには到達できる設計になっています。これは「must be complete」と「recommended」の使い分けによるものです。

---

## まとめ

第11回はCONSTRUCTIONフェーズの6つのルールファイルについて説明しました。今回学んだことは以下です。

- constructionディレクトリの6ファイルは、inceptionに比べてサイズが均一で、最初の4つは9ステップに収束しています
- functional-design.mdは技術非依存で7つの質問カテゴリを体系的に評価します
- nfr-requirements.mdとnfr-design.mdは、要件段階では全カテゴリを評価し設計段階では該当するものだけを選ぶ非対称の構造を持ちます
- infrastructure-design.mdの`shared-infrastructure.md`は、ユニット横断の共有インフラを一元管理します
- code-generation.mdの「コピーファイル禁止」ルールと生成後の重複検証は、Brownfieldプロジェクト特有のリスクに対する2段階のルールです
- build-and-test.mdは6種類のテストを定義し、Per-Unit Loopの外側で全ユニットを横断的に検証します
- Per-Unit Loop内の5ファイルに「標準化された2択メッセージ」が規定されており、build-and-test.mdは別の完了メッセージ形式を使用します

---

## 次回予告

最終回 (第12回) では、OPERATIONSフェーズのプレースホルダーが示す将来ビジョン、AI-DLCのカスタマイズ方法 (ベースレイヤー＋拡張レイヤーの二層構造) 、そしてシリーズ全体の総括を行います。AI-DLCはフレームワークの完成品ではなく、拡張可能なプラットフォームです。
