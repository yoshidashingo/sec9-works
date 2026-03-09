# AI-DLCを完全理解する 第10回: inceptionディレクトリ徹底解説 ― 計画フェーズの7ファイル

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - workspace-detection.mdは唯一「承認不要」かつ最短 (94行) のステージ。6ステップでBrownfield/Greenfieldを判定する
> - reverse-engineering.mdはBrownfieldプロジェクトで「常に再実行」 (Always rerun) のポリシーを持ち、8種の成果物テンプレートを定義する
> - user-stories.mdは最多ステップ (328行・23ステップ) で、Planning→Generationの2部構成を持つ
> - workflow-planning.mdはMermaidフローチャートの生成指示とBrownfield向けのモジュール連携分析を含む

---

## inceptionディレクトリの概観

inceptionディレクトリには、Inceptionフェーズの7つのステージに対応する7つのルールファイルが格納されています。

| # | ファイル | 行数 | ステップ数 | 分類 |
|---|---------|------|----------|------|
| 1 | workspace-detection.md | 94 | 6 | ALWAYS |
| 2 | reverse-engineering.md | 312 | 12※ | CONDITIONAL |
| 3 | requirements-analysis.md | 169 | 9 | ALWAYS |
| 4 | user-stories.md | 328 | 23 | CONDITIONAL |
| 5 | workflow-planning.md | 480 | 11 | ALWAYS |
| 6 | application-design.md | 146 | 15 | CONDITIONAL |
| 7 | units-generation.md | 184 | 19 | CONDITIONAL |

※reverse-engineering.mdはStep 1の見出しが2つあるため、ステップ見出しの総数は13個。詳細は後述。

ファイルのボリュームには大きな差があります。最短のworkspace-detection.md (94行) から最長のworkflow-planning.md (480行) まで、5倍以上の開きがあります。この差はステージの複雑さやBrownfield向け分析の有無を反映していると考えられます。

---

## 1. workspace-detection.md: 唯一「承認不要」のステージ

第8回で「Automatically proceed to next phase」と記述されていることを紹介しましたが、workspace-detection.mdの全体を見ると、その簡潔さが際立ちます。

### 6ステップの全容

| Step | 内容 |
|------|------|
| 1 | `aidlc-state.md`の存在チェック (既存プロジェクトの検出)  |
| 2 | ワークスペースの既存コードスキャン |
| 3 | Brownfield/Greenfieldの判定と次ステージの決定 |
| 4 | aidlc-state.mdの初期作成 |
| 5 | 完了メッセージの提示 |
| 6 | 自動的に次ステージへ進行 |

Step 2のスキャン対象は具体的です。ソースファイルには`.java`, `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.kt`, `.kts`, `.scala`, `.groovy`, `.go`, `.rs`, `.rb`, `.php`, `.c`, `.h`, `.cpp`, `.hpp`, `.cc`, `.cs`, `.fs`など主要言語の拡張子と、`pom.xml`, `package.json`, `build.gradle`などのビルドファイルが列挙されています。さらに「Workspace Root」を特定し、「NOT aidlc-docs/」と明記してドキュメントディレクトリとアプリケーションコードの混同を防ぐ意図です。

Step 4で作成されるaidlc-state.mdの初期テンプレートには「Code Location Rules」が含まれています:

```markdown
## Code Location Rules
- **Application Code**: Workspace root (NEVER in aidlc-docs/)
- **Documentation**: aidlc-docs/ only
- **Structure patterns**: See code-generation.md Critical Rules
```

このルールは第8回で解説したディレクトリ構造の「分離原則」を、プロジェクトの最初期から適用するものです。

---

## 2. reverse-engineering.md: 8種の成果物テンプレート

### 「常に再実行」ポリシー

冒頭に注目すべき一文があります:

```markdown
**Rerun behavior**: Always rerun when brownfield project detected,
even if artifacts exist. This ensures artifacts reflect current code state
```

「成果物が既に存在していても、Brownfieldプロジェクトが検出されたら常に再実行する。これにより成果物が現在のコードの状態を反映することを意図している (原文: ensures) 。」

一方、core-workflow.md上のSkip条件は「Greenfieldプロジェクト、または既存のリバースエンジニアリング成果物がある場合にスキップ」と定めています。reverse-engineering.md自身の「常に再実行」ポリシーとは方向性が異なります。これはcore-workflow.mdがステージ全体のスキップ判断を扱い、個別のルールファイルがステージ内の振る舞いを詳細に定義するという「二層構造の粒度の違い」として読み取れますが、両ルール間に潜在的な矛盾がある可能性にも留意が必要です。

### 8つの成果物

reverse-engineering.mdが生成する成果物は以下の8つです:

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | business-overview.md | ビジネスコンテキスト図、ビジネス説明、ビジネストランザクション |
| 2 | architecture.md | システム概要、アーキテクチャ図、コンポーネント説明、データフロー |
| 3 | code-structure.md | ビルドシステム、クラス/モジュール階層、既存ファイルの一覧 |
| 4 | api-documentation.md | REST API、内部API、データモデル |
| 5 | component-inventory.md | パッケージの種類別インベントリ |
| 6 | technology-stack.md | プログラミング言語、フレームワーク、インフラ、ビルドツール |
| 7 | dependencies.md | 内部依存関係図、外部依存関係 |
| 8 | code-quality-assessment.md | テストカバレッジ、コード品質指標、技術的負債 |

これらに加えて、分析のメタデータを記録する`reverse-engineering-timestamp.md`も生成されます。

第2回でTOGAFのArchitecture Visionと対比した内容が、ここで8つの具体的な成果物テンプレートとして定義されています。特にbusiness-overview.mdはBusiness Dictionary (DDDのユビキタス言語と同様に、ビジネスドメインの用語を統一定義するものです。第3回で詳述しました) を含みます。

### Step 1の二重性

実はreverse-engineering.mdには「Step 1」の見出しが2つあります。最初のStep 1は「Multi-Package Discovery」で、6つのサブステップでワークスペースをスキャンします。2番目のStep 1 (実質的にはStep 2に相当) は「Generate Business Overview Documentation」です。これはルールファイル自体の構造的な問題です。AIモデルがステップ番号の重複をどのように処理するかはモデルの実装に依存するため、影響について断定的なことは言えませんが、ソースの記述順に処理が進む場合はMulti-Package Discoveryが先に実行されることが期待されます。

---

## 3. requirements-analysis.md: 「プロダクトオーナーの役割を担え」

### ロールの指定

冒頭にある「Assume the role of a product owner (プロダクトオーナーの役割を担え) 」という指示は、AI-DLCの中でも特徴的です。AIモデルにプロダクトオーナーの視点を持たせることで、要件の体系的な分析と整合性の向上を意図しています。

### 4段階のインテント分析

Step 2でユーザーのリクエストを4つの観点から分析します:

1. **Request Clarity** (明確さ) : Clear / Vague / Incomplete
2. **Request Type** (種類) : New Feature / Bug Fix / Refactoring / Upgrade / Migration / Enhancement / New Project
3. **Initial Scope Estimate** (スコープ) : Single File → Cross-system の5段階
4. **Initial Complexity Estimate** (複雑さ) : Trivial / Simple / Moderate / Complex

この分析結果がStep 3の「Requirements Depth」の決定に用いられます。第7回で解説したAdaptive Depthの3段階 (Minimal / Standard / Comprehensive) がここで具体的に適用されます。

### 完了メッセージのパターン

requirements-analysis.mdの完了メッセージには、他のステージにはないオプションが含まれています:

```markdown
> 📝 **Add User Stories** - Choose to Include **User Stories** stage
>   (currently skipped based on project simplicity)
```

User Storiesがスキップ予定の場合に限り、「User Storiesを追加する」という選択肢が提示されます。第8回で解説した「User Control」原則の具体的な適用例です。AIがスキップと判断したステージについて、ユーザーがその判断を覆して含めることができるオプションを提示しています。

---

## 4. user-stories.md: 最多ステップの23ステップ

### 2部構成: PlanningとGeneration

user-stories.mdは328行、23ステップで構成されます。行数ではworkflow-planning.md (480行) が最大ですが、ステップ数ではuser-stories.mdがInceptionフェーズ最多です。

構造はPart 1 (Planning: Step 1〜14) とPart 2 (Generation: Step 15〜23) の2部構成になっています。この2部構成は、第9回で解説したterminology.mdの「Planning vs Generation」の区別そのものです。計画を立ててから承認を得て、その後に成果物を生成します。

### インテリジェント・アセスメント

Step 1の前に、user-stories.mdには「Intelligent Assessment Guidelines」という独自のセクションがあります。User Storiesの実行が必要かどうかを、3段階の優先度で判断するためのガイドラインです:

| 優先度 | 判断 | 例 |
|-------|------|---|
| **High Priority** | 常に実行 | 新しいユーザー機能、UX変更、マルチペルソナ |
| **Medium Priority** | 複雑さに応じて判断 | バックエンドのユーザー影響、パフォーマンス改善 |
| **Skip** | 単純なケースのみスキップ | 純粋なリファクタリング、孤立したバグ修正 |

なお、ソースにはMedium Priorityの判断に使う「Complexity Assessment Factors」(6項目) も別途定義されています。

そしてデフォルトのルールとして「When in doubt, include user stories AND ask clarifying questions (迷ったら、ユーザーストーリーを含めて明確化質問もする) 」があります。第9回で解説したoverconfidence-prevention.mdの「聞きすぎるくらい聞け」という方針と同じ考え方が見られます。

### INVEST基準の明示

Step 4では、生成するユーザーストーリーがINVEST基準に従うことが明示されています:

- **I**ndependent (独立している) 
- **N**egotiable (交渉可能) 
- **V**aluable (価値がある) 
- **E**stimable (見積もり可能) 
- **S**mall (小さい) 
- **T**estable (テスト可能) 

第3回で「アジャイルのユーザーストーリーの適用」として触れた内容が、ルールファイルで明示的に指示されています。ただし、これはプロンプト指示であり、AIモデルがINVEST基準に完全に準拠したストーリーを生成する技術的保証ではありません。

---

## 5. workflow-planning.md: 最長ファイルの全容

### ファイルの巨大さの理由

workflow-planning.mdは480行で、inceptionディレクトリ最大のファイルです。その理由は、このステージが「CONSTRUCTIONフェーズを含む後続すべてのステージの実行/スキップを決定する」要 (かなめ) だからです。

### Brownfield向けの詳細分析

workflow-planning.mdの約半分はBrownfield (既存コードベースがある) プロジェクト向けの分析に費やされています。Step 2のサブセクションとして以下の4項目が定義されています:

- **Step 2.1 Transformation Scope Detection** (Brownfield Only): 単一コンポーネントの変更か、アーキテクチャ変革か
- **Step 2.2 Change Impact Assessment**: ユーザー影響、構造変更、データモデル変更、API変更、NFR影響の5領域（※Brownfield限定の指定なし）
- **Step 2.3 Component Relationship Mapping** (Brownfield Only): 依存関係グラフの作成
- **Step 2.4 Risk Assessment**: リスクの評価

さらに独立したステップとして:

- **Step 5 Multi-Module Coordination Analysis** (Brownfield Only): 複数モジュールの更新順序、並列化可能性、テスト戦略

Greenfieldプロジェクトでは「Brownfield Only」と指定された分析がスキップされるため、同じステージでもBrownfieldとGreenfieldで実行時間が大きく異なります。

### Mermaidフローチャートの生成

Step 6では、実行計画をMermaidフローチャートとして視覚化します。スタイルルールも具体的に定義されています:

| スタイル | 色 | 用途 |
|---------|---|------|
| Material Green (#4CAF50)  | 緑 | 常に実行 / 完了済み |
| Material Orange (#FFA726)  | 橙 | CONDITIONALで実行 |
| Material Gray (#BDBDBD)  | 灰 | CONDITIONALでスキップ |
| Material Purple (#CE93D8)  | 紫 | 開始/終了 |

第9回で解説したcontent-validation.mdの「Mermaidバリデーション」が、ここで生成されるフローチャートに適用されます。

---

## 6. application-design.md: 4つの設計成果物

### 「詳細なビジネスロジックは後で」

application-design.mdの冒頭に重要な注記があります:

```markdown
**Note**: Detailed business logic design happens later
in Functional Design (per-unit, CONSTRUCTION phase)
```

Application Designは「高レベルのコンポーネント識別とサービス層の設計」に焦点を当て、詳細なビジネスロジックはCONSTRUCTIONフェーズのFunctional Designに委ねます。第5回で解説した段階的な具体化の考え方と一致する構造です。

### 4つの成果物

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | components.md | コンポーネント定義、責務、インターフェース |
| 2 | component-methods.md | メソッドシグネチャ、高レベルの目的、入出力型 |
| 3 | services.md | サービス定義、責務、オーケストレーション |
| 4 | component-dependency.md | 依存関係マトリクス、通信パターン、データフロー |

component-methods.mdには「Note: Detailed business rules will be defined in Functional Design (per-unit, CONSTRUCTION phase)」という注記が付いています。メソッドシグネチャ (メソッドの名前・引数・戻り値の型の定義) は決めるが「中身」は決めません。Inceptionフェーズの役割が「何を作るか」であり「どう作るか」ではないことが、成果物のレベルにも反映されています。

---

## 7. units-generation.md: 分割のルール

### 2部構成

units-generation.mdもuser-stories.mdと同じく、Part 1 (Planning: Step 1〜11) とPart 2 (Generation: Step 12〜19) の2部構成です。

### Unit of Workの定義

冒頭でUnit of Workが厳密に定義されています:

```markdown
**DEFINITION**: A unit of work is a logical grouping of stories
for development purposes. For microservices, each unit becomes
an independently deployable service. For monoliths, the single unit
represents the entire application with logical modules.
```

第9回で解説したterminology.mdの用語定義がここで実践されています。マイクロサービスではUnit = Service、モノリスではUnit = アプリケーション全体 (内部にModuleを持つ) 。

### 3つの成果物

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | unit-of-work.md | ユニット定義、責務 |
| 2 | unit-of-work-dependency.md | 依存関係マトリクス |
| 3 | unit-of-work-story-map.md | ストーリーとユニットの対応表 |

unit-of-work-story-map.mdは、第3回で生成されたユーザーストーリーと、ここで分割されたユニットを紐づける成果物です。この対応表により「どのストーリーがどのユニットで実装されるか」のトレーサビリティが確保されます。

---

## 7ファイルに共通するパターン

inceptionディレクトリの7ファイルを俯瞰すると、以下の共通パターンが見えます:

1. **コンテキストのロード**: 前ステージの成果物を読み込む
2. **分析**: ユーザーのリクエストや既存コードを分析する
3. **質問の生成**: 曖昧な点について質問ファイルを作成する
4. **回答の分析**: 回答の矛盾や曖昧さをチェックする
5. **成果物の生成**: テンプレートに従って成果物を生成する
6. **承認待ち**: ユーザーの明示的な承認を待つ (workspace-detection以外) 
7. **進捗更新**: aidlc-state.mdとaudit.mdを更新する

この共通パターンにより、多くのステージは一貫した構造を持っています。workspace-detectionだけがStep 6 (承認待ち) を持たない点が、その特殊な位置づけを示しています。

---

## まとめ

第10回はINCEPTIONフェーズの7つのルールファイルについて説明しました。今回学んだことは以下です。

- inceptionディレクトリの7ファイルは、94行〜480行の幅を持ち、ステージの複雑さやBrownfield分析の有無がファイルの長さに反映される傾向があります
- workspace-detection.mdは6ステップで完結する最短のステージで、承認なしの自動進行が特徴です
- reverse-engineering.mdはBrownfieldプロジェクトで「常に再実行」のポリシーを持ち、8つの成果物テンプレートで既存コードベースを体系的にドキュメント化します
- requirements-analysis.mdは「プロダクトオーナーの役割を担え」というロール指定と4段階のインテント分析が特徴です
- user-stories.mdは最多の23ステップで、INVEST基準の明示的な指示とインテリジェント・アセスメントを含みます
- workflow-planning.mdは最長の480行で、Brownfield向けの詳細分析とMermaidフローチャート生成を含みます
- application-design.mdとunits-generation.mdは「INCEPTIONでは何を決め、何をCONSTRUCTIONに残すか」の境界を明確にしています

---

## 次回予告

第11回では、constructionディレクトリの6つのルールファイルを解説します。functional-design.md (ドメインエンティティとビジネスルールの設計) 、nfr-requirements.md / nfr-design.md (非機能要件の2段階設計) 、infrastructure-design.md (論理→物理のマッピング) 、code-generation.md (Brownfieldの「コピーファイル禁止」ルール) 、build-and-test.md (6種のテスト戦略) を読み解いていきます。
