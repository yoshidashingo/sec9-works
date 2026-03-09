# AI-DLCを完全理解する 第8回: core-workflow.md を読み解く ― AI-DLCの最上位ルールファイル

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - core-workflow.mdはAI-DLCの最上位ルールファイルで、他のすべてのワークフローに優先するよう宣言されている
> - 冒頭の4つのMANDATORY(必須)ルールが「読み込み→検証→質問→挨拶」の基盤を形成する
> - 3フェーズの定義構造と、Key Principlesの8原則がフレームワーク全体のルールを規定する

ここからシリーズ後半に入ります。前半 (第1回〜第7回) がAI-DLCの概念と設計思想を解説したのに対し、後半 (第8回〜第12回) ではワークフロー定義ファイルそのものを読み解きます。AI-DLCの「なぜそう設計されているのか」から「実際にどう書かれているのか」へ ― 抽象から具体への転換です。

[https://extravaganzarr.s3.ap-northeast-1.amazonaws.com/aidlc-image03.png:image=https://extravaganzarr.s3.ap-northeast-1.amazonaws.com/aidlc-image03.png]

引用元：[https://aws.amazon.com/jp/blogs/news/ai-driven-development-life-cycle/:title]

---

## 後半パートの読み方

前半パート (第1回〜第7回) では、AI-DLCの概念と設計思想を既存の開発手法と比較しながら解説してきました。後半パート (第8回〜第12回) では視点を変え、**AI-DLCのワークフロー定義ファイルそのものを1行ずつ読み解いていきます**。

AI-DLCは、AIモデルに対する「指示書」としてMarkdownファイルの集合体で構成されています。この指示書がどう書かれているかを知ることで、前半で解説した概念がどう実装されているかが具体的に見えてきます。

その出発点が、今回取り上げる`core-workflow.md`です。

---

## 冒頭宣言: なぜ「すべてに優先する」のか

ファイルの先頭2行はこうです:

```markdown
# PRIORITY: This workflow OVERRIDES all other built-in workflows
# When user requests software development, ALWAYS follow this workflow FIRST
```

1行目は「このワークフローは他のすべての組み込みワークフローをオーバーライドする」。これはルールの優先順位の宣言です。2行目は「ソフトウェア開発リクエストを受けたら、常にこのワークフローを最初に実行せよ」。これは実行順序の指示です。優先順位と実行順序の2つの観点から、core-workflow.mdの最上位性を宣言しています。

なぜここまで強い宣言が必要なのでしょうか。AI-DLCはClaude Code、Amazon Q Developer CLIといったLLMを活用したAI開発ツール上で動作することを前提としています。これらのツールには、ソフトウェア開発に対するデフォルトの振る舞い (組み込みワークフロー) が存在します。たとえば「コードを書いて」と言われたらすぐにコーディングを始めるような動きです。

AI-DLCは「すぐにコードを書かない」ことが設計の根幹にあります。要件を分析し、設計を行い、承認を得てからコードを生成します。この設計意図をモデルに伝え、デフォルト動作よりもこのワークフローを優先させるために、冒頭で明示的に宣言しています。ただし、この宣言はあくまでLLMへのプロンプト指示であり、プログラミング言語のオーバーライドのように技術的に強制するメカニズムではありません。LLMが高い確率で従うことを意図した設計上の工夫です。

---

## Adaptive Workflow Principle: 4つの評価軸

冒頭宣言の直後に、AI-DLC全体を貫く原則が1つだけ置かれています:

```markdown
## Adaptive Workflow Principle
**The workflow adapts to the work, not the other way around.**
```

「ワークフローが仕事に適応する。仕事がワークフローに適応するのではない。」

第1回で「適応型ワークフロー」と紹介したものの原文が、この一文に集約されます。続けて、AIモデルが判断する際の4つの評価軸が定義されています:

1. **User's stated intent and clarity** ― ユーザーの意図がどれだけ明確か
2. **Existing codebase state (if any)** ― 既存コードベースの状態（もしあれば）
3. **Complexity and scope of change** ― 変更の複雑さとスコープ
4. **Risk and impact assessment** ― リスクとインパクトの評価

これらの評価軸は、core-workflow.md以降の各ステージの「Execute IF」「Skip IF」条件や、Adaptive Depth (第7回参照) の深度決定に反映されています。

---

## 4つのMANDATORY(必須)ルール: 基盤の基盤

Adaptive Workflow Principleの直後に、4つのMANDATORYルールが並びます。これらはすべてのステージの実行に先立って遵守すべきルールです。

### MANDATORY 1: Rule Details Loading

```markdown
**CRITICAL**: When performing any phase, you MUST read and use relevant content
from rule detail files in `.steering/aws-aidlc-rule-details/`
or `.amazonq/aws-aidlc-rule-details/` directory.
```

「フェーズを実行するときは、rule detailsディレクトリから関連ファイルを必ず読み込め」。

ソースファイルでは`.steering/aws-aidlc-rule-details/`と`.amazonq/aws-aidlc-rule-details/`の2つのパスが`or`で併記されています。前者はClaude Code環境、後者はAmazon Q Developer CLI環境に対応しており、AI-DLCが複数のAI開発ツールで動作することを想定した設計です。

AI-DLCは二層構造で設計されています。core-workflow.mdが全体の流れ (ワークフロー) を定義し、rule-detailsディレクトリ配下の個別ファイルが各ステージの詳細手順を定義します。core-workflow.mdだけを読んでも「何をするか」は分かりますが、「どうやるか」の手順は個別ファイルに書かれています。

さらに、共通ルール (commonディレクトリ) として4つのファイルを「ワークフロー開始時に常に読み込め」と指定しています:

| ファイル | 役割 |
|---------|------|
| `process-overview.md` | ワークフロー全体の技術リファレンス |
| `session-continuity.md` | セッション再開のガイダンス |
| `content-validation.md` | コンテンツの検証ルール |
| `question-format-guide.md` | 質問フォーマットのルール |

これらは次回 (第9回) で詳しく解説します。

### MANDATORY 2: Content Validation

```markdown
**CRITICAL**: Before creating ANY file, you MUST validate content
according to `common/content-validation.md` rules
```

「ファイルを作成する前に、必ずコンテンツを検証せよ」。具体的にはMermaid図のシンタックス検証、ASCII art図の標準準拠、特殊文字のエスケープ、複雑な視覚コンテンツへのテキスト代替、コンテンツパーシングの互換性テストが求められます。

AIが生成するドキュメントには、構文エラーのある図表が混入するリスクがあります。Mermaid図のシンタックスが壊れていれば描画されませんし、特殊文字がエスケープされていなければMarkdownの表示が崩れます。このルールは「生成したら必ず検証しろ」という品質チェックのルールです。

### MANDATORY 3: Question File Format

```markdown
**CRITICAL**: When asking questions at any phase, you MUST follow
question format guidelines.
```

「質問するときは、質問フォーマットガイドラインに従え」。AI-DLCには「質問ファイル方式」 (第3回で紹介した) という独自の対話方式があります。選択肢付きの質問をファイルに書き出し、ユーザーが`[Answer]:`タグで回答するフォーマットです。このフォーマットを全ステージで統一するためのルールです。

### MANDATORY 4: Custom Welcome Message

```markdown
**CRITICAL**: When starting ANY software development request,
you MUST display the welcome message.
```

「開発リクエストを開始するときは、ウェルカムメッセージを表示せよ」。ウェルカムメッセージは`.steering/aws-aidlc-rule-details/common/welcome-message.md`に定義されたテンプレートです。

注目すべきは「This should only be done ONCE at the start of a new workflow」と「Do NOT load this file in subsequent interactions to save context space」という2つの付帯条件です。ウェルカムメッセージは1回だけ表示し、2回目以降のインタラクション (セッション再開時など) ではファイルの読み込み自体をスキップしてコンテキスト領域を節約します。これはLLMが前回の表示を記憶しているわけではなく、ワークフローの状態管理ファイル (aidlc-state.md等) から既にワークフローが開始済みであると判定できるため、再表示が不要となる設計です。LLMのコンテキストウィンドウ (一度に処理できるトークンの上限) は有限のリソースであり、AI-DLCはこの制約を意識した設計をしています。

### 4つのMANDATORYの構造

この4つを俯瞰すると、「読み込み → 検証 → 質問 → 挨拶」という基盤が見えます:

```
MANDATORY 1: Rule Details Loading    → 何を参照するか (知識の基盤) 
MANDATORY 2: Content Validation      → 何を守るか (品質の基盤) 
MANDATORY 3: Question File Format    → どう対話するか (対話の基盤) 
MANDATORY 4: Custom Welcome Message  → どう始めるか (体験の基盤) 
```

個別のステージの「中身」ではなく、すべてのステージに共通する「前提条件」を定義しているのが4つのMANDATORYの役割です。

---

## 3フェーズの定義構造

4つのMANDATORYの後、core-workflow.mdの本体部分が始まります。INCEPTION → CONSTRUCTION → OPERATIONSの3フェーズが順に定義されています。

### 共通する記述パターン

各フェーズは以下の統一されたテンプレートで記述されています:

```markdown
# [Phase Name]

**Purpose**: [このフェーズの目的]
**Focus**: [焦点を示す問い]

**Stages in [Phase Name]**:
- [ステージ一覧]
```

各ステージもまた統一されたパターンに従います:

| 要素 | 内容 |
|-----|------|
| **見出し** | `## [Stage Name] ([ALWAYS/CONDITIONAL/PLACEHOLDER])` |
| **実行条件** (CONDITIONALのみ)  | `Execute IF:` / `Skip IF:` のリスト |
| **Execution** | 番号付きステップのリスト |
| **承認ゲート** | `Wait for Explicit Approval` の指示 |
| **監査ログ** | `MANDATORY: Log user's response in audit.md` |

この統一パターンが14ステージの基本構造となっています。ただし、ALWAYSステージにはExecute IF/Skip IFの実行条件がない、Workspace Detectionには承認ゲートがない、OPERATIONSはプレースホルダーのため簡略化されているなど、ステージ固有の変形があります。基本構造を統一することで、新しいステージを読むときの認知コストを低減することを意図した設計です。

### INCEPTION Phase (7ステージ) 

Inceptionフェーズには7つのステージが定義されています。第2回〜第4回で概念的に解説した内容の、ワークフロー定義上の姿です:

| # | ステージ | 分類 | 承認 |
|---|---------|------|------|
| 1 | Workspace Detection | ALWAYS | 不要 (自動進行)  |
| 2 | Reverse Engineering | CONDITIONAL | 必要 |
| 3 | Requirements Analysis | ALWAYS (深度可変)  | 必要 |
| 4 | User Stories | CONDITIONAL | 必要 |
| 5 | Workflow Planning | ALWAYS | 必要 |
| 6 | Application Design | CONDITIONAL | 必要 |
| 7 | Units Generation | CONDITIONAL | 必要 |

core-workflow.md上の特徴をいくつか拾い上げます。

**Workspace Detectionの「自動進行」**: ステップ7に「Automatically proceed to next phase」と明記されています。他のステージにはすべて「Wait for Explicit Approval」がありますが、ここだけ承認なしで次に進みます。第2回で解説した「情報収集が主目的であり、設計上の意思決定を伴わない」という設計思想が、ワークフロー定義上は「承認ステップの省略と自動進行」として実装されています。なお、aidlc-state.mdやaudit.mdの作成・更新はWorkspace Detection内で行われるため、ファイル操作が一切ないわけではありません。承認が不要なのは、ユーザーの設計判断を求める局面がないためです。

**User Storiesの「2部構成」**: User Storiesは「Planning」と「Generation」の2つのパートを持ちます。core-workflow.md上では1つのステージですが、内部で承認が2回発生します。第3回で触れた「質問→回答→分析→承認→生成」のフローが、ここで構造化されています。

**Reverse Engineeringの実行条件**: core-workflow.md上の条件は「Execute IF: Existing codebase detected AND No previous reverse engineering artifacts found」「Skip IF: Greenfield project (no existing code)」「Skip IF: Previous reverse engineering artifacts exist」です。条件文を文字通り読むと「既存コードがあり、かつ成果物がなければ実行する。成果物が既にあればスキップする」となります。第2回では「毎回再実行される」と解説しましたが、これはcore-workflow.mdの条件文だけでは説明がつきません。この条件がどのように運用されるかの詳細は、個別のreverse-engineering.mdに定義されています (第10回で解説) 。core-workflow.mdレベルでは「成果物の有無による条件分岐」として定義されている点を、ここでは正確に押さえておきます。

### CONSTRUCTION Phase (6ステージ) 

CONSTRUCTIONフェーズの定義で最も目を引くのは、**Per-Unit Loop**の構造です:

```markdown
**Stages in CONSTRUCTION PHASE**:
- Per-Unit Loop (executes for each unit):
  - Functional Design (CONDITIONAL, per-unit)
  - NFR Requirements (CONDITIONAL, per-unit)
  - NFR Design (CONDITIONAL, per-unit)
  - Infrastructure Design (CONDITIONAL, per-unit)
  - Code Generation (ALWAYS, per-unit)
- Build and Test (ALWAYS - after all units complete)
```

第5回で解説したPer-Unit Loopがここで定義されています。5つのステージが「per-unit」として囲まれ、Build and Testだけがループの外に置かれています。

もう1つの特徴は、CONSTRUCTIONフェーズのステージだけに付与されている制約です:

```markdown
**MANDATORY**: Present standardized 2-option completion message
as defined in [stage].md - DO NOT use emergent 3-option behavior
```

「標準化された2択の完了メッセージを提示せよ。3択や他の自発的なナビゲーションパターンを作るな」。これは第7回で解説した「NO EMERGENT BEHAVIOR」原則のワークフロー定義上の実装です。事実として、INCEPTIONフェーズにはこの制約がなく、各ステージ固有の承認フォーマットに委ねられています。CONSTRUCTIONフェーズでのみ明示的に制約が設けられている理由は仕様書には明記されていませんが、コード生成に近い段階ではAIの自律的な振る舞いをより厳密に制御したいという設計意図が推測されます。一方で、2択に限定することにより、想定外の状況でユーザーに適切な選択肢を提示できない可能性もあります。

### OPERATIONS Phase (1ステージ) 

```markdown
# 🟡 OPERATIONS PHASE

**Purpose**: Placeholder for future deployment and monitoring workflows
**Status**: This stage is currently a placeholder for future expansion.
```

第7回で解説した通り、OPERATIONSフェーズは将来拡張用のプレースホルダーです。core-workflow.md上では、将来含まれる予定の5項目 (デプロイ、モニタリング、インシデント対応、保守、本番準備チェックリスト) が列挙されています。また「Current State: All build and test activities are handled in the CONSTRUCTION phase.」と付記されており、OPERATIONSが実装されるまでの間、ビルドとテストの活動はCONSTRUCTIONフェーズで取り扱われることが明示されています。

---

## Key Principles: 8つの基本原則

3フェーズの定義の後に、「Key Principles」セクションが置かれています。フレームワーク全体に適用される8つの原則です:

1. **Adaptive Execution** ― 第1回の適応型ワークフロー
2. **Transparent Planning** ― 第1回で触れた実行計画の可視化
3. **User Control** ― 第7回の承認ゲート
4. **Progress Tracking** ― 第7回の進捗管理
5. **Complete Audit Trail** ― 第7回の監査証跡
6. **Quality Focus** ― 第7回のAdaptive Depth
7. **Content Validation** ― MANDATORY 2で詳述
8. **NO EMERGENT BEHAVIOR** ― 第7回のNO EMERGENT BEHAVIOR原則

前半パートで個別に解説した概念が、ここに原則として集約されています。

注目したいのは、Content ValidationとNO EMERGENT BEHAVIORです。Content Validationは4つのMANDATORYの1つとして、NO EMERGENT BEHAVIORはCONSTRUCTION各ステージの定義内で、それぞれ既に記述されています。にもかかわらず、原則としても重ねて宣言されています。重要なルールは「一度言えば十分」ではなく「繰り返し宣言する」という設計方針が窺えます。LLMに対するプロンプト指示では、重要なルールを複数箇所で繰り返すことで遵守率が高まるという経験的知見があり、この繰り返しは冗長ではなく意図的な設計と考えられます。ただし、繰り返しはコンテキストウィンドウの消費を増やすため、どこまで繰り返すかは冗長さとのトレードオフでもあります。

---

## チェックボックス追跡: 二層の進捗管理

Key Principlesの直後に、チェックボックス追跡のルールが定義されています:

```markdown
## MANDATORY: Plan-Level Checkbox Enforcement

### MANDATORY RULES FOR PLAN EXECUTION
1. NEVER complete any work without updating plan checkboxes
2. IMMEDIATELY after completing ANY step described in a plan file, mark that step [x]
3. This must happen in the SAME interaction where the work is completed
4. NO EXCEPTIONS: Every plan step completion MUST be tracked with checkbox updates
```

AI-DLCの進捗管理は二層構造になっています:

| 層 | 管理対象 | 記録先 |
|---|---------|--------|
| **Plan-Level** | 各ステージ内の詳細な実行ステップ | 各ステージの計画ファイル |
| **Stage-Level** | ワークフロー全体のステージ進捗 | aidlc-state.md |

重要なのは「SAME interaction」という制約です。「作業を完了したインタラクションと同じインタラクション内で、チェックボックスを更新せよ」。後からまとめて更新するのではなく、AIモデルが作業完了と同時に進捗を反映するよう指示しています。

なぜ即時更新が必要なのでしょうか。LLMベースのAIは、コンテキストウィンドウの上限に達するとセッションを新たに開始する必要があります。もしチェックボックスの更新を後回しにして、セッションの途中でコンテキストが切れたら、「どこまで終わったのか」が分からなくなります。作業完了と同じインタラクション内での即時更新を求めることで、セッション断絶に対するレジリエンス (回復力) を高める設計です。ただし、この即時更新もプロンプト指示であるため、LLMが更新を行う前にセッションが中断される可能性は残ります。

---

## 監査ログの書き方ルール

最後に、監査ログ (audit.md) の詳細な書き方ルールが定義されています。

### 記録のMANDATORYルール

```markdown
- MANDATORY: Log EVERY user input with timestamp in audit.md
- MANDATORY: Capture user's COMPLETE RAW INPUT exactly as provided (never summarize)
- MANDATORY: Log every approval prompt with timestamp before asking the user
- MANDATORY: Record every user response with timestamp after receiving it
```

1. すべてのユーザー入力をタイムスタンプ付きで記録する
2. ユーザーの入力は要約せず、完全な原文のまま記録する
3. 承認プロンプトは、ユーザーに提示する**前に**タイムスタンプ付きで記録する
4. ユーザーの応答は、受信した**後に**タイムスタンプ付きで記録する

3番目と4番目に注目してください。承認プロンプトは「ユーザーに聞く前」に、応答は「受け取った後」に記録します。これにより、「いつ何を聞いたか」「いつ何が答えられたか」の時系列の順序を記録する設計です。ただし、タイムスタンプの精度はAIモデルが参照できる時刻情報の仕組みに依存します。

### CRITICAL: 追記のみ、上書き禁止

```markdown
- CRITICAL: ALWAYS append changes to EDIT audit.md file,
  NEVER use tools that completely overwrite its contents
```

audit.mdへの変更は「追記 (append) 」のみ。ファイル全体を上書きする操作は禁止。

なぜ上書きが危険なのでしょうか。LLMのツール操作には「ファイルを読んで、内容を加工して、全体を書き戻す」パターンがあります。ファイルが大きくなるとコンテキストウィンドウの制約により全体を正確に保持できず、書き戻し時に内容が欠落したり意図せず変更されるリスクがあります。追記のみに限定するルールとすることで、既存の記録が消失するリスクを大幅に低減しています。ただし第7回で述べた通り、このルールはプロンプト指示として実装されているため、ファイルシステムレベルの上書き防止機構ではありません。

### 監査ログのフォーマット

```markdown
## [Stage Name or Interaction Type]
**Timestamp**: [ISO 8601 timestamp]
**User Input**: "[Complete raw user input - never summarized]"
**AI Response**: "[AI's response or action taken]"
**Context**: [Stage, action, or decision made]
```

タイムスタンプはISO 8601形式 (YYYY-MM-DDTHH:MM:SSZ) で統一されます。実際のタイムスタンプの精度は、AIモデルの時刻取得手段 (ツール呼び出し等) に依存します。User InputとAI Responseが対になる構造で、Contextがステージ名や判断内容を補足します。

---

## ディレクトリ構造の定義

core-workflow.mdの末尾には、成果物の配置先となるディレクトリ構造が定義されています:

```
<WORKSPACE-ROOT>/
├── [project-specific structure]     # アプリケーションコード
│
├── aidlc-docs/                      # AI-DLCのドキュメント
│   ├── inception/                   # Inceptionフェーズの成果物
│   │   ├── plans/
│   │   ├── reverse-engineering/
│   │   ├── requirements/
│   │   ├── user-stories/
│   │   └── application-design/
│   ├── construction/                # CONSTRUCTIONフェーズの成果物
│   │   ├── plans/
│   │   ├── {unit-name}/
│   │   └── build-and-test/
│   ├── operations/                  # OPERATIONSフェーズ (プレースホルダー) 
│   ├── aidlc-state.md
│   └── audit.md
```

重要なルールは「アプリケーションコードはワークスペースルートに、ドキュメントはaidlc-docs/に」という分離原則です。core-workflow.mdには「Application code: Workspace root (NEVER in aidlc-docs/)」と明記されています。

この分離により、設計文書とアプリケーションコードの混在を防ぎます。一方で、コードとドキュメントが物理的に離れるため、両者の対応関係の把握にはaidlc-state.mdなどによる管理が必要になります。

---

## まとめ

第8回はAI-DLC全体の振る舞いを規定するcore-workflow.mdの構造について説明しました。今回学んだことは以下です。

- 冒頭宣言「OVERRIDES all other built-in workflows」は、LLMのデフォルト動作よりもこのワークフローを優先するよう指示するプロンプト上の宣言です
- 4つのMANDATORYルール (読み込み・検証・質問形式・ウェルカムメッセージ) がすべてのステージの前提条件として規定されています
- 3フェーズ14ステージは統一テンプレート (Execute IF / Skip IF / Execution / 承認ゲート / 監査ログ) を基本構造とし、ステージの性質に応じた変形があります
- Key Principlesの8原則は前半パートの概念を集約し、重要なルールを繰り返し宣言する構造をとっています (コンテキスト消費とのトレードオフを伴います)
- チェックボックス追跡の二層構造 (Plan-Level / Stage-Level) と即時更新のルールが、セッション断絶への耐性を高める設計になっています
- 監査ログは追記のみ・上書き禁止のルールにより既存記録の消失リスクを低減し、承認前/応答後のタイムスタンプにより時系列の順序を記録します

---

## 次回予告

第9回では、core-workflow.mdが「常に読み込め」と指定するcommonディレクトリの全貌を解読します。process-overview.md、session-continuity.md、question-format-guide.md、depth-levels.mdなど、AI-DLCの基盤となる共通ルールファイル群を1つずつ読み解いていきます。
