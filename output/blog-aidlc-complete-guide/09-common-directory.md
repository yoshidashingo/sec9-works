# AI-DLCを完全理解する 第9回: commonディレクトリの全貌 ― 全ステージ共通のメタルール

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - commonディレクトリには11のルールファイルがあり、すべてのステージに共通する「前提条件」を定義する
> - 質問ファイル方式 (question-format-guide.md) は「チャットで質問しない」という厳格なルールを持つ
> - overconfidence-prevention.mdは「聞きすぎるくらい聞け」という設計意図を文書化したものだ（ただしプロンプト指示による制御であり、技術的な強制力はない）
> - error-handling.mdとworkflow-changes.mdが、AI-DLCの「何かあったときの対処法」を体系的に定義する

---

## commonディレクトリの位置づけ

第8回で解説したcore-workflow.mdのMANDATORY 1 (Rule Details Loading) は、ワークフロー開始時に4つの共通ファイルを読み込むよう指示していました。しかし実際のcommonディレクトリには、その4つを含む**合計11のファイル**が格納されています。

```
common/
├── process-overview.md          # ワークフロー全体図
├── welcome-message.md           # ウェルカムメッセージ
├── session-continuity.md        # セッション再開テンプレート
├── question-format-guide.md     # 質問フォーマットガイド
├── depth-levels.md              # 適応的深度の定義
├── terminology.md               # 用語集
├── overconfidence-prevention.md # 過信防止ガイド
├── content-validation.md        # コンテンツ検証ルール
├── ascii-diagram-standards.md   # ASCII図表の標準規格
├── workflow-changes.md          # ワークフロー変更管理
└── error-handling.md            # エラー処理と復旧手順
```

これらは個別のステージに属さない「横断的な関心事」を扱うファイルです。ソフトウェア設計でいうクロスカッティング・コンサーン (Cross-Cutting Concerns) に近い役割です。ソフトウェア設計における認証やログ出力がアプリケーションの特定の機能ではなく全体に関わるように、これらのファイルはAI-DLCのすべてのステージに共通する前提条件やルールを定義しています。ただし、コードレベルのクロスカッティング・コンサーンが技術的に適用されるのに対し、これらはMarkdownファイルのプロンプト指示として記述されている点が異なります。

以下、機能ごとに4つのグループに分けて解説します。

---

## グループ1: 全体図と開始・再開 ― プロセスの入口

### process-overview.md: 技術リファレンスとしての全体図

冒頭に以下の記述があります:

```markdown
**Note**: Similar content exists in core-workflow.md (user welcome message) and README.md (documentation).
This duplication is INTENTIONAL - each file serves a different purpose
```

「同じような内容がcore-workflow.mdやREADME.mdにもある。この重複は意図的なものだ。」

process-overview.mdはAIモデル向けの技術リファレンスとして設計されています。Mermaid形式のフローチャートが埋め込まれており、AIモデルがワークフロー全体の構造をコンテキストに読み込むためのファイルです。

同じワークフロー情報が3つの異なる受け手に向けて提供されている点に注目してください。ソースファイルの記述に基づく対応関係は以下の通りです:
- **process-overview.md**: 「Detailed technical reference with Mermaid diagram for AI model context loading」（AIモデル向けの技術リファレンス）
- **core-workflow.md**: 「User-facing welcome message with ASCII diagram」（ユーザー向けのASCII図付きウェルカムメッセージ）
- **README.md**: 「Human-readable documentation for repository」（リポジトリの人間向けドキュメント）

ステージの実行順序について、process-overview.mdには「No fixed sequences: Stages execute in the order that makes sense for your specific task (固定的な順序はない。タスクに合った順序で実行される) 」と記載されています。ただし、第8回で解説した通り、core-workflow.mdではINCEPTION→CONSTRUCTION→OPERATIONSというフェーズ順序は固定されており、「No fixed sequences」が指すのはフェーズ内のCONDITIONALステージの柔軟性と解釈するのが自然です。

### welcome-message.md: ユーザーの第一印象を設計する

第8回のMANDATORY 4で触れたウェルカムメッセージの本体がこのファイルです。110行にわたるテンプレートで、挨拶と概要、3フェーズのASCII図、各フェーズの説明、Key Principles、次のステップの予告で構成されます。

AI-DLCにおけるユーザーの役割は「作る人」ではなく「判断する人」として位置づけられています。process-overview.mdでは「Your Team's Role」として以下が挙げられています:
- **Answer questions**: 専用の質問ファイルに回答する
- **Review and approve each phase**: 各フェーズをレビューし承認する
- **Collectively decide on architectural approach**: アーキテクチャ方針をチームで決定する

なお、これらはprocess-overview.mdの記述であり、welcome-message.mdでは表現が若干異なる場合があります。

### session-continuity.md: セッション断絶への対処

第7回で触れた`aidlc-state.md`によるセッション再開の仕組みが、具体的なテンプレートとして定義されているのがこのファイルです。

```markdown
**Welcome back! I can see you have an existing AI-DLC project in progress.**

Based on your aidlc-state.md, here's your current status:
- **Project**: [project-name]
- **Current Phase**: [INCEPTION/CONSTRUCTION/OPERATIONS]
- **Current Stage**: [Stage Name]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]
```

「MANDATORY: Load Previous Stage Artifacts」の指示により、セッション再開時には前回までに生成された成果物 (AI-DLCの各ステージが出力するMarkdownドキュメントやコードなどのファイル群) を段階的に読み込むルールが定められています:

- **初期ステージ** (Workspace Detection等) : ワークスペース分析のみ
- **要件・ストーリー**: リバースエンジニアリング＋要件の成果物
- **設計ステージ**: 要件＋ストーリー＋アーキテクチャ＋設計の成果物
- **コードステージ**: 上記すべて＋既存のコードファイル

ステージが進むほど読み込む成果物が増えます。session-continuity.mdが定義するこの「段階的コンテキストローディング」は、LLM (Large Language Model: 大規模言語モデル) のコンテキストウィンドウを効率的に使うための設計です。初期ステージの再開で設計文書まで読み込む必要はありませんし、コードステージの再開で要件文書を読み飛ばすわけにもいきません。

---

## グループ2: 対話と質問 ― AIとユーザーの接点

### question-format-guide.md: 「チャットで質問するな」

第3回で「質問ファイル方式」として紹介した仕組みの全ルールがこのファイルに定義されています。冒頭には以下の指示があります:

```markdown
**CRITICAL**: You must NEVER ask questions directly in the chat.
ALL questions must be placed in dedicated question files.
```

「チャットで質問するな。すべての質問は専用のファイルに置け。」

なぜチャットではなくファイルなのか。第3回で解説した通り、理由は永続性・構造化・監査可能性の3つです。質問と回答がファイルとして残ることで、セッション再開や後からの追跡が可能になります。なお、「NEVER」はプロンプト指示としての強い要求であり、AIモデルがこのルールを100%遵守する技術的保証があるわけではありません。

質問フォーマットの構造は以下の通りです:

```markdown
## Question [Number]
[質問文]

A) [選択肢1]
B) [選択肢2]
X) Other (please describe after [Answer]: tag below)

[Answer]:
```

重要なルールが2つあります。**「Other」選択肢の必須化**と**選択肢の数の制約 (ガイドライン) **です。

1つ目の「Other」 (その他) は、**すべての質問の最後の選択肢として必須**とされています。用意された選択肢にぴったり合わない場合のエスケープハッチです。

2つ目の選択肢の数は「Minimum: 2 meaningful options + "Other"」「Maximum: 5 meaningful options + "Other"」とガイドラインが示されています。さらに「Don't make up options just to fill slots (枠を埋めるために選択肢を作り上げるな) 」という指示があります。選択肢は「あるべき数」だけ用意します。

もう1つの重要な仕組みが**矛盾検出**です。question-format-guide.mdの「Contradiction and Ambiguity Detection」セクションでは、矛盾の例として以下が挙げられています:

- **Scope mismatch**: 「Bug fix」なのに「Entire codebase affected」
- **Risk mismatch**: 「Low risk」なのに「Breaking changes」
- **Timeline mismatch**: 「Quick fix」なのに「Multiple subsystems」
- **Impact mismatch**: 「Single component」なのに「Significant architecture changes」

これらは網羅的な分類ではなく、「logically inconsistent answers（論理的に矛盾した回答）」の代表例として示されたものです。矛盾が検出された場合は`{phase-name}-clarification-questions.md`で追加質問を行い、解消を目指します。ただし、矛盾検出自体がAIモデルの判断に依存するため、すべての矛盾を確実に検出できる保証はありません。question-format-guide.mdは、この矛盾検出のルールと具体例の「原典」として機能しています。

### overconfidence-prevention.md: 運用フィードバックから生まれたガイド

このファイルは他のファイルとは毛色が違います。冒頭にこう書かれています:

```markdown
## Problem Statement
AI-DLC was exhibiting overconfidence by not asking enough clarifying questions,
even for complex project intent statements.
```

「AI-DLCが過信を示していた。複雑なプロジェクトの意図表明に対しても、十分な明確化質問を行わなかった。」

これは**問題が発生した後に追加されたガイド**であることが読み取れます。overconfidence-prevention.mdの「Root Cause Analysis」セクションによれば、根本原因は4つのステージのルールファイルにある指示 (directives) にありました:

- Functional Design: 「Skip entire categories if not applicable（該当しないカテゴリはスキップせよ）」
- User Stories: 「Use categories as inspiration, NOT as mandatory checklist（カテゴリはインスピレーションとして使え。必須チェックリストではない）」
- Requirements Analysis: 「Similar patterns encouraging minimal questioning（質問を最小限に抑える方向の類似パターン）」
- NFR Requirements: 「"Only if" conditions that discouraged thorough analysis（『〜の場合のみ』という条件が徹底的な分析を抑制）」

これらはすべて「質問を減らす方向」に誘導する指示でした。結果として、AIが質問を十分に行わずに先に進んでしまう問題が起きたとされています。

修正の方向はソースファイルに明記されています:

**旧 (OLD APPROACH) **: 「Only ask questions if absolutely necessary」
**新 (NEW APPROACH) **: 「When in doubt, ask the question - overconfidence leads to poor outcomes」

5つの新原則 (New Guiding Principles) が定められました:

1. **Default to Asking**: 曖昧さがあれば質問する
2. **Comprehensive Coverage**: すべての関連カテゴリを評価し、スキップしない
3. **Thorough Analysis**: すべてのユーザー回答から曖昧さを探す
4. **Mandatory Follow-up**: 不明確な回答には追加質問する
5. **No Proceeding with Ambiguity**: すべての曖昧さが解消されるまで先に進まない

このガイドの存在は、AI-DLCが実運用で発生した問題に対して修正を加えた痕跡と読み取れます。同時に、このガイド自体もプロンプト指示である以上、過信防止が技術的に強制されるわけではなく、AIモデルの振る舞いが改善される「意図」を表明したものである点は留意が必要です。

---

## グループ3: 言葉と深さの統一 ― 共通言語の確立

### terminology.md: 用語の厳密な使い分け

第3回でDDDの「ユビキタス言語」に触れましたが、AI-DLCもフレームワーク内の用語を定義しています。最も基本的な区別は**Phase**と**Stage**です:

- **Phase**: 3つの上位フェーズ (INCEPTION / CONSTRUCTION / OPERATIONS) 
- **Stage**: フェーズ内の個別の活動

正しい例: 「The CONSTRUCTION phase contains 7 stages」
間違い: 「The Requirements Assessment phase」 (phaseではなくstageが正しい) 

もう1つの重要な区別が、アーキテクチャに関する4つの用語です:

| 用語 | 定義 | 使う場面 |
|-----|------|---------|
| **Unit of Work** | 開発目的でまとめたユーザーストーリーの論理グループ | 計画・分割の議論 |
| **Service** | マイクロサービスアーキテクチャにおける独立デプロイ可能なコンポーネント | デプロイ・インフラの議論 |
| **Module** | サービスやモノリス内の論理的な機能グループ | 内部構造の議論 |
| **Component** | 特定の機能を提供するクラス、関数、パッケージ | 設計・実装の議論 |

これらの用語は日常会話では混同されがちですが、terminology.mdでは明確な区別が定義されています。Unit of WorkはINCEPTIONフェーズの計画段階で使う用語であり、ServiceはCONSTRUCTIONフェーズの実装段階で使う用語です。ただし、これもプロンプト指示による定義であり、AIモデルが常にこの使い分けを正確に守れるかどうかは別の問題です。

さらに**Planning vs Generation**の区別も定義されています。AI-DLCの多くのステージは「計画 (Planning) 」と「生成 (Generation) 」の2段階で構成されます。Story Planning → Story Generation、Code Planning → Code Generationのように、常にこのペアで動きます。

### depth-levels.md: 「深さ」のルール

第7回で解説したAdaptive Depthの詳細定義がこのファイルです。core-workflow.mdのWorkflow Planningでも「Each stage independently evaluated for inclusion and depth (各ステージは実行するかどうかと深度を個別に評価する) 」と記述されており、ステージ選択と深度という2つの次元の概念はcore-workflow.mdにも存在します。depth-levels.mdはこの深度の次元を詳細に定義するファイルです:

```markdown
**When a stage executes, ALL its defined artifacts are created.
The "depth" refers to the level of detail and rigor within those artifacts,
which adapts to the problem's complexity.**
```

「ステージが実行されたら、定義されたすべての成果物が作成される。『深さ』とは、その成果物内の詳細さと厳密さのレベルを指し、問題の複雑さに応じて適応される。」

※原文の「which adapts to the problem's complexity」は重要な修飾句です。深さが固定値ではなく問題の複雑さに応じて変動することを明示しています。

つまり、AI-DLCの適応には2つの次元があります:

1. **ステージ選択 (バイナリ) **: 実行するか、しないか
2. **詳細レベル (アダプティブ) **: 実行する場合、どれだけ詳しくやるか

詳細レベルを決定する要因は、depth-levels.mdの「Factors Influencing Detail Level」セクションに列挙された6つ (Request Clarity, Problem Complexity, Scope, Risk Level, Available Context, User Preferences) です。ただしdepth-levels.mdでは「Model decides: Based on problem characteristics, not prescriptive rules (モデルが判断する。規範的なルールではなく、問題の特性に基づいて) 」と記載されており、深度の決定は最終的にAIモデルの判断に委ねられています。

depth-levels.mdにはRequirements Analysisの具体例が示されています。Simple Scenario (Bug Fix) では`requirements.md`は「Concise functional requirement, minimal sections」、Complex Scenario (System Migration) では「Comprehensive functional + non-functional requirements, traceability, acceptance criteria」と記載されています。**同じ成果物名でも、中身の密度がまったく違います**。

---

## グループ4: 品質管理と変更・エラー対処

### content-validation.md と ascii-diagram-standards.md: 図表の品質管理

第8回のMANDATORY 2 (Content Validation) の詳細ルールがcontent-validation.mdに定義されています。主に以下の3種類のコンテンツの検証ルールが記述されています:

1. **Mermaid図**: シンタックスチェック、特殊文字のエスケープ、バリデーション失敗時のテキスト代替
2. **ASCII図**: ascii-diagram-standards.mdの規格に準拠しているか
3. **一般的なMarkdown**: コードブロック、特殊文字、構文の正確性

ascii-diagram-standards.mdは、ASCII図の描画ルールを細かく定義しています:

```markdown
### ✅ ALLOWED: `+` `-` `|` `^` `v` `<` `>` and alphanumeric text
### ❌ FORBIDDEN: Unicode box-drawing characters
```

使える文字は`+` `-` `|` `^` `v` `<` `>`とアルファベット・数字のみ。`┌` `─` `│` `└`などのUnicodeのBox Drawing文字は禁止。理由は「フォントやプラットフォームによって表示が不安定になるから」です。

さらに厳格なのが**文字幅の統一ルール**です。「Every line in a box MUST have EXACTLY the same character count (ボックス内のすべての行は、スペースを含めてまったく同じ文字数でなければならない) 」。これは等幅フォントでの表示崩れを防ぐためのルールです。

content-validation.mdで特徴的なのは「フォールバック」の考え方です。Mermaidのバリデーションに失敗したら、Mermaid図を諦めてテキストベースの表現に切り替えます。「完璧な図を無理に作る」のではなく「確実に表示できる形に落とす」。この発想は第7回で解説した「Quality Focus」原則と方向性が一致しています。

### workflow-changes.md: 途中変更のシナリオ集

AI-DLCは適応型ワークフローですが、ワークフロー自体の途中変更も想定しています。workflow-changes.mdは**8つの変更シナリオ**とその対処手順を定義しています:

| # | シナリオ | 例 |
|---|---------|---|
| 1 | スキップしたステージの追加 | 「やはりユーザーストーリーも作りたい」 |
| 2 | 計画済みステージのスキップ | 「NFR Designは飛ばそう」 |
| 3 | 現在のステージの再実行 | 「このユーザーストーリーが気に入らない。やり直したい」 |
| 4 | 以前のステージの再実行 | 「アーキテクチャの決定を変えたい」 |
| 5 | ステージ深度の変更 | 「要件分析をComprehensiveに切り替えて」 |
| 6 | ワークフローの一時停止 | 「今日はここまで。明日続ける」 |
| 7 | アーキテクチャ決定の変更 | 「モノリスからマイクロサービスに変えたい」 |
| 8 | ユニットの追加・削除 | 「Paymentユニットを分割してBillingも作りたい」 |

各シナリオには「Handling (対処手順) 」と「Considerations (考慮事項) 」が定義されています。共通するパターンは以下の通りです:

1. **リクエストの確認**: ユーザーが何を変えたいか明確にする
2. **影響評価**: 変更が他のステージにどう波及するか分析する
3. **明示的な確認**: ユーザーが影響を理解した上で承認する
4. **すべてのトラッキング更新**: aidlc-state.md、計画ファイル、audit.mdを同期する

特に興味深いのはシナリオ4 (以前のステージの再実行) です。ソースファイルにはApplication Designを変更する場合の例が具体的に記載されています: 「Restarting Application Design will require redoing: Units Planning, Units Generation, per-unit design (all units), Code Planning, Code Generation」。つまり、**5つのステージ**のやり直しが必要になります。ワークフロー変更の「コスト」がステージの進行度に応じて増大する設計です。この「後工程ほど手戻りコストが大きい」という特性はウォーターフォールの課題と共通する側面がありますが、AI-DLCでは影響範囲の明示と対処手順のルール化により、手戻りの影響を管理しやすくする意図が見られます。

### error-handling.md: 何かあったときの対処法

最後のファイルは最も長いものです (374行) 。AIが遭遇しうるエラーを、**重要度4段階 × ステージ別**で体系的に定義しています。

重要度の4段階:

| レベル | 定義 | 例 |
|-------|------|---|
| **Critical** | ワークフロー続行不可 (Workflow cannot continue)  | 必須ファイルの欠損、入力の処理不能 |
| **High** | フェーズが計画通り完了不可 (Phase cannot complete as planned)  | 必須質問への回答不足、矛盾する回答 |
| **Medium** | ワークアラウンドで続行可 (Phase can continue with workarounds)  | オプション成果物の欠損、非クリティカルなバリデーション失敗 |
| **Low** | 進行に影響なし (Minor issues that don't block progress)  | フォーマット不整合、オプション情報の不足 |

ステージ別では、Context Assessment (Workspace Detection) からOperationsまで各ステージ固有のエラーパターンと対処法が列挙されています。なお、ソースファイルではステージ名が一部terminology.mdの定義と異なる表記 (例: 「Requirements Assessment」) で記載されている箇所があります。

さらにこのファイルの後半は**セッション再開時のエラー**に特化しています。session-continuity.mdが「正常な再開」を扱うのに対し、error-handling.mdは「異常な再開」を扱います:

- 成果物ファイルが存在するがaidlc-state.mdでは未完了とされている
- aidlc-state.mdでは完了だが成果物ファイルが存在しない
- 複数のステージが同時に「現在実行中」とマークされている

これらはすべて「状態の不整合」です。データベースのACIDトランザクションであれば、操作の原子性によってこうした不整合は原理的に発生しません。しかし、AI-DLCではaidlc-state.mdと成果物ファイルの更新がアトミックではないため、不整合が起こり得ます。error-handling.mdは、この不整合を検出し、ユーザーに確認した上で修復するための手順を定義しています。

---

## 11ファイルの全体像

commonディレクトリの11ファイルを俯瞰すると、4つの役割が見えます:

| 役割 | ファイル | 一言で言うと |
|-----|---------|-----------|
| **入口** | process-overview.md, welcome-message.md, session-continuity.md | 始め方・戻り方 |
| **対話** | question-format-guide.md, overconfidence-prevention.md | 聞き方・聞く姿勢 |
| **統一** | terminology.md, depth-levels.md | 言葉・深さの共通基準 |
| **品質・対処** | content-validation.md, ascii-diagram-standards.md, workflow-changes.md, error-handling.md | 品質管理・変更・エラー |

これらは個別のステージのルールファイルとは異なり、「AI-DLCというフレームワーク自体がどう振る舞うべきか」を定義するメタルールです。個別ステージのルールが「何を設計するか」を指示するのに対し、commonディレクトリは「どう設計するか」「どう対話するか」「何かあったらどうするか」というフレームワークの基盤を提供しています。ただし、これらすべてがMarkdownファイルのプロンプト指示であるため、技術的な強制力はAIモデルのプロンプト遵守能力に依存します。

---

## まとめ

第9回はすべてのステージに共通するメタルールを定義するcommonディレクトリについて説明しました。今回学んだことは以下です。

- commonディレクトリの11ファイルは、AI-DLCのすべてのステージに共通するメタルール（プロンプト指示）を定義します
- process-overview.md / welcome-message.md / session-continuity.mdは「入口と再開」を担当し、同じワークフロー情報をAIモデル・ユーザー・再開セッションの3つの受け手に向けて提供します
- question-format-guide.mdは「チャットで質問するな、ファイルに書け」というルールと矛盾検出の仕組みを定義しています（ただし遵守はAIモデルの判断に依存します）
- overconfidence-prevention.mdは実運用で発生した「過信」問題への対処として追加されたガイドです。プロンプト指示によるAIモデルの行動制御にはこうした試行錯誤が伴うことを示す事例でもあります
- depth-levels.mdはステージ選択 (実行 or スキップ) とは別に、成果物の詳細レベルを問題の複雑さに応じて適応させる仕組みを定義します
- workflow-changes.mdの8つの変更シナリオとerror-handling.mdのエラー対処は、「順風満帆でないケース」にも対処手順を用意する設計を示します

---

## 次回予告

第10回では、inceptionディレクトリの7つのルールファイルを解説します。workspace-detection.md (唯一「承認不要」のステージの全容) 、reverse-engineering.md (8種の成果物テンプレート) 、requirements-analysis.md (プロダクトオーナーの役割) 、user-stories.md (最大ボリュームのステージ) などを1つずつ読み解いていきます。
