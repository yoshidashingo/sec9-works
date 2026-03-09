# AI-DLCを完全理解する 第4回: 設計図を描く ― 計画と分割の技術

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - AI-DLC (AI-Driven Development Life Cycle) のWorkflow Planningで「どのステージを実行し、どれをスキップするか」を明示的に計画する
> - Application Designは4つの設計成果物で、コンポーネントの責務とインターフェースを定義する
> - Units Generationでシステムを開発可能な作業単位 (Unit of Work) に分割する
> - SAFeのPI Planning、C4 Model、マイクロサービスの分割戦略と比較して、AI-DLCの位置づけを明らかにする

[https://extravaganzarr.s3.ap-northeast-1.amazonaws.com/aidlc-image03.png:image=https://extravaganzarr.s3.ap-northeast-1.amazonaws.com/aidlc-image03.png]

引用元：[https://aws.amazon.com/jp/blogs/news/ai-driven-development-life-cycle/:title]

---

## 要件が決まったら、次は「どう作るか」

第3回では、Requirements AnalysisとUser Storiesで「何を作るか」を決めるプロセスを解説しました。要件が固まったら、次は設計と計画です。

AI-DLCのInceptionフェーズ後半には、3つのステージが控えています:

1. **Workflow Planning**: どのステージを実行し、どれをスキップするかを決める
2. **Application Design**: コンポーネントとサービスの設計
3. **Units Generation**: システムを作業単位に分割する

Workflow PlanningはALWAYS (常時実行) ステージです。プロジェクトの全体計画は省略できません。一方、Application DesignとUnits GenerationはCONDITIONAL (条件付き実行) で、シンプルな変更では不要と判断されてスキップされます。

---

## Workflow Planning: 「何をやるか／やらないか」を決める

### なぜ「やらないこと」を決めるのか

Workflow Planningの本質は、**実行するステージだけでなく、スキップするステージも明示的に決める**ことにあります。

AI-DLCの14ステージのうち、ALWAYSステージ (Workspace Detection、Requirements Analysis、Workflow Planning、Code Generation、Build and Test) は必ず実行されます。判断が必要なのは残りのCONDITIONALステージです。Application Designを実行するのか？ NFR Requirementsは必要か？ Infrastructure Designはスキップできるか？

各CONDITIONALステージの実行/スキップ判断を、AIが自動で行い、理由 (Rationale) とともに記録します。「なぜこのステージを実行するのか」「なぜスキップするのか」が、すべて`execution-plan.md`に残ります。

### 11ステップの流れ

Workflow Planningは11ステップで構成されます:

1. **先行コンテキストの読み込み**: Reverse Engineering、Requirements Analysis、User Storiesの成果物をすべて読み込みます
2. **詳細なスコープと影響分析**: 変更がユーザー体験・アーキテクチャ・データモデル・API・非機能要件のどこに影響するかを評価します
3. **ステージの実行/スキップ判定**: 各CONDITIONALステージについて、実行条件とスキップ条件を照合して判定します
4. **適応型深度の適用**: 実行するステージごとに、成果物の詳細度を決定します
5. **マルチモジュール連携分析** (Brownfieldのみ) : モジュール間の依存関係と更新戦略を決定します
6. **ワークフローの可視化**: Mermaidフローチャートで全ステージの実行/スキップ状態を図示します
7. **実行計画ドキュメントの作成**: `execution-plan.md`を生成します
8. **状態追跡の初期化**: `aidlc-state.md`を更新します
9. **ユーザーへの提示**: 実行計画を提示し、承認を求めます
10. **ユーザー応答の処理**: 承認、変更要求、ステージ追加/削除の要望に対応します
11. **ログ記録**: 承認結果を`audit.md`に記録します

ステップ9〜10でユーザーの承認を挟むのは、AIのステージ判定が必ずしも正確とは限らないためです。特にスキップと判定されたステージについて、本当に不要かをユーザー自身が批判的に検証することが重要です。

### リスク評価の4段階

ステップ2の影響分析では、リスクを4段階で評価します:

| リスクレベル | 条件 | ロールバックの難易度 |
|-------------|------|-------------------|
| **Low** | 影響が局所的で、変更箇所が明確 | 容易 |
| **Medium** | 複数コンポーネントに影響、未知の要素がある | 中程度 |
| **High** | システム全体に影響、未知の要素が多い | 困難 |
| **Critical** | 本番環境に直結、不確実性が高い | 非常に困難 |

このリスク評価が、後続のステージ判定に直接影響します。リスクがHighやCriticalなら、NFR RequirementsやInfrastructure Designがスキップされることは少ないでしょう。

### Mermaidフローチャートによる可視化

Workflow Planningの特徴的な成果物が、**Mermaidフローチャート**です。全ステージの実行/スキップ状態を、色分けされたフローチャートとして可視化します:

- 緑: 実行済み／常時実行
- オレンジ: 条件付きで実行
- グレー (破線) : スキップ
- 紫: 開始／終了

この図があることで、「全体のうち自分が今どこにいるのか」が一目で分かります。長い開発プロセスの中で現在地を見失わない ― 地図としてのフローチャートです。

---

## Application Design: コンポーネントの責務を定義する

Workflow Planningで「Application Designを実行する」と判定されたら、このステージに進みます。新しいコンポーネントやサービスが必要な場合に実行されます。

### 4つの設計成果物

Application Designは15ステップで構成され、4つの設計成果物を生成します:

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | **components.md** | コンポーネントの名前、目的、責務、インターフェース |
| 2 | **component-methods.md** | 各コンポーネントのメソッドシグネチャ、入出力の型 |
| 3 | **services.md** | サービスの定義、責務、他サービスとの連携パターン |
| 4 | **component-dependency.md** | 依存関係マトリクス、通信パターン、データフロー図 |

重要な設計上の判断がここにあります。Application Designが定義するのは**コンポーネントの「何」と「何のために」**であり、**「どう実装するか」ではありません**。詳細なビジネスロジックの設計は、後続のCONSTRUCTIONフェーズ「Functional Design」で行います。

この分離は意図的です。設計を1つのステージに詰め込むと、巨大で見通しの悪い設計書ができてしまいます。AI-DLCは「構造の設計」と「ロジックの設計」を明確に分離し、それぞれを独立したステージとして扱います。一方で、構造設計の時点ではビジネスロジックの詳細が未確定であるため、後のFunctional Designで構造の見直しが必要になる可能性もあり、その場合は手戻りのコストが発生します。

---

## Units Generation: 作業単位への分割

Application Designでコンポーネントの全体像が決まったら、次はそれを**開発可能な作業単位**に分割します。Units Generationステージです。

### Unit of Workとは何か

Unit of Work (UOW) は、**関連するユーザーストーリーを論理的にまとめた、アーキテクチャスタイルに依存しない開発単位**です。AI-DLCの仕様書では次のように説明されています:

> マイクロサービスの場合は独立してデプロイ可能なサービスとなり、モノリスの場合は単一ユニットがアプリケーション全体を表し、論理モジュールで整理される。

マイクロサービスならサービス境界に、モノリスならモジュール境界に対応します。いずれの場合も、UOWは「ストーリーの集合を開発可能な単位にまとめたもの」という一貫した定義を持ちます。

### Planning→Generationの2部構成

Units Generationは19ステップで、Planning (11ステップ) とGeneration (8ステップ) の2部構成です。第3回で解説したUser Storiesと同じパターンです。

**Planning (ステップ1〜11) ** では

- 分割計画を作成し、質問ファイルで不明点を解消します
- 3つの必須成果物を定義します:
  - `unit-of-work.md`: ユニットの定義と責務
  - `unit-of-work-dependency.md`: ユニット間の依存関係マトリクス
  - `unit-of-work-story-map.md`: ストーリーからユニットへのマッピング
- ユーザーの承認を得てからGenerationに進みます

**Generation (ステップ12〜19) ** では

- 承認された計画に基づいてユニット成果物を生成します
- 各ステップの完了をチェックボックスで追跡します
- 完了後にユーザーの最終承認を得ます

### ストーリーマップの必須化

Units Generationの特徴的な成果物が`unit-of-work-story-map.md`です。第3回で生成されたUser Storiesの各ストーリーが、どのユニットに割り当てられるかを明示します。

これは「すべてのストーリーがどこかのユニットに必ず属する」ことを保証する仕組みです。後述するWBSの「100%ルール」と同じ発想で、割り当て漏れを構造的に防ぎます。

---

## 既存手法との比較: 計画と分割の系譜

### SAFeのPI Planning

SAFe (Scaled Agile Framework) は、Dean Leffingwellが2011年に発表した大規模アジャイルのフレームワークです。その中核イベントが「PI Planning (Program Increment Planning) 」― 通常2日間をかけて行われる対面イベントで、ART (Agile Release Train) の「心臓の鼓動」と呼ばれます。

PI Planningでは以下が決まります:

- **PI目標**: 今回のPI (通常8〜12週間) で達成すべきこと
- **チーム間依存関係**: プログラムボード上で可視化される
- **リスク**: ROAMボード (Resolved / Owned / Accepted / Mitigated) で4分類管理

AI-DLCのWorkflow Planningと並べてみましょう:

| 観点 | SAFe PI Planning | AI-DLC Workflow Planning |
|------|-----------------|------------------------|
| **決定対象** | どのフィーチャーを実行するか | どのステージを実行/スキップするか |
| **判断基準** | ビジネスバリュー、チームキャパシティ | 変更の影響範囲、リスクレベル |
| **リスク管理** | ROAM (4分類)  | Low/Medium/High/Critical (4段階)  |
| **可視化** | プログラムボード | Mermaidフローチャート |
| **実行者** | チーム全員 (対面)  | AI (ユーザー承認あり)  |
| **所要時間** | 2日間 (対面イベント)  | AIが短時間で実行 (ユーザー承認を含む)  |

判断の対象は異なります。SAFeのPI Planningはチーム横断の合意形成を目的とし、AI-DLCのWorkflow Planningはステージの実行判定を目的とします。しかし、**「何をやり何をやらないかを、理由とともに明示的に計画する」**という構造的原則は共通しています。解決する問題のスケールは異なりますが、計画の透明性と説明責任を重視する姿勢は同じです。

### C4 Model: 抽象度の段階的管理

Simon Brownが2006年〜2011年にかけて開発したC4 Modelは、ソフトウェアアーキテクチャを4つのレベルで可視化する手法です。

| レベル | 名称 | 何を見せるか |
|--------|------|-------------|
| **Level 1** | Context | システム全体と外部との関係。全ステークホルダー向け |
| **Level 2** | Container | Webアプリ、API、DB等の技術的構成要素 |
| **Level 3** | Component | 各コンテナ内部のモジュールやクラス群 |
| **Level 4** | Code | クラス、メソッド、インターフェースの詳細 |

C4 Modelの主要な設計方針は「**1枚の図に詰め込みすぎない**」ことです。地図のように段階的にズームインし、聴衆に応じた適切な粒度で情報を提供します。

AI-DLCのApplication Designは、C4 ModelのLevel 2〜3に相当する設計を行います。4つの成果物 (components.md → component-methods.md → services.md → component-dependency.md) で設計の異なる側面を順に定義します。C4のように同一対象を段階的にズームインするのとはメカニズムが異なりますが、「一度にすべてを定義しない」という原則は共通しています。

ただし、C4が「可視化とコミュニケーション」に重点を置くのに対し、AI-DLCは「設計意思決定の記録と承認」に重点を置きます。各段階でユーザーへの質問と承認を挟む対話型プロセスが、AI-DLCの特徴です。

### マイクロサービスの分割戦略

2014年、Martin FowlerとJames Lewisが「Microservices」の定義を整理した記事を公開しました。独立してデプロイ可能な小さなサービスの集合としてシステムを構築するアーキテクチャスタイルです。

マイクロサービスの分割基準として広く知られるのが2つあります:

1. **ビジネスケイパビリティ**: 組織のビジネス機能に沿って分割します (受注管理、在庫管理、顧客管理など) 
2. **境界づけられたコンテキスト (Bounded Context) **: Eric EvansのDDDで定義された概念で、ドメインモデルが一貫して有効な範囲で分割します

Sam Newmanの『Building Microservices』 (初版2015年、第2版2021年) は、マイクロサービスへの段階的な移行アプローチを解説した代表的な書籍です。Martin Fowlerは2015年の「MonolithFirst」で「成功したマイクロサービスの事例は、ほぼすべてがモノリスから始まり、大きくなりすぎて分割された」と書き、「モノリスファースト」アプローチを提唱しました。

AI-DLCのUnits Generationは、この「分割の基準を明確にしてから実装に進む」という考え方を取り入れています。さらに、AI-DLCの定義では「マイクロサービスの場合は独立デプロイ可能なサービス、モノリスの場合は論理モジュール」と明示されており、特定のアーキテクチャスタイルに偏らない設計になっています。

### WBSの100%ルール

1950年代後半に米国国防総省のPolaris計画で生まれ、1962年に体系化されたWBS (Work Breakdown Structure) は、プロジェクトの作業を階層的に分解する手法です。その最も重要な原則が「100%ルール」― **分解の結果が元のスコープの100%をカバーすること**です。

AI-DLCのUnits Generationにおける`unit-of-work-story-map.md`は、この100%ルールと同様の「漏れ防止」の発想に基づいています。「すべてのストーリーがいずれかのユニットに割り当てられている」ことを確認することで、作業の抜け漏れを構造的に防止します。

---

## 3ステージが示す設計原則

Workflow Planning、Application Design、Units Generationの3ステージから、AI-DLCの設計に対するアプローチが見えてきます。

**3ステージに共通する設計原則は「段階的具体化」です。** 計画 → 構造 → 分割の順に、抽象度を段階的に下げていきます。まず全体の実行計画を決め (Workflow Planning) 、次にコンポーネントの構造を設計し (Application Design) 、最後に開発可能な単位に分割します (Units Generation) 。各段階でユーザーの承認を得ることで、方向性のズレを早期に検出します。

段階的具体化と承認ゲートの組み合わせは、C4 Modelのズームイン、WBSの階層的分解、SAFeのPI→スプリントの多段階計画など、ソフトウェア開発方法論において広く採用されている基本原則です。AI-DLCもこの原則に従い、各段階の成果物をAIが生成し、人間が承認するという形で運用します。

---

## まとめ

第4回は設計と分割を担うWorkflow Planning・Application Design・Units Generationについて説明しました。今回学んだことは以下です。

- Workflow Planning (11ステップ) は、全ステージの実行/スキップをリスク評価に基づいて判定し、Mermaidフローチャートで可視化します
- Application Design (15ステップ) は4つの設計成果物 (components / methods / services / dependency) で構造を定義します。ビジネスロジックの詳細はFunctional Designに委ねます
- Units Generation (19ステップ) はUnit of Workという抽象的な分割単位で、アーキテクチャスタイルに依存しない分割を行います
- なお、3ステージすべてが実行される場合は計45ステップの対話と承認が必要になります。小規模な変更に対しては過重になりうるため、CONDITIONALステージのスキップ機能を活用し、プロジェクト規模に応じた適用が重要です
- SAFeのPI Planning、C4 Modelの段階的ズーム、マイクロサービスの分割戦略、WBSの100%ルール ― いずれも「計画と分割」の知恵であり、AI-DLCのプロセスにはこれらと共通する要素が見られます

---

## 次回予告

第5回では、INCEPTIONフェーズからCONSTRUCTIONフェーズへ移り、「ビジネスロジックと品質の設計」を取り上げます。Per-Unit Loop (ユニット単位で回す設計サイクル) 、Functional Design (技術に依存しないビジネスロジック設計) 、NFR Requirements / NFR Design (非機能要件の扱い方) を、DDDの戦術的設計、AWS Well-Architected Framework、ISO 25010と比較しながら解説します。
