# AI-DLCを完全理解する 第5回: ビジネスロジックと品質を設計する ― Construction前半戦

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - AI-DLC (AI-Driven Development Life Cycle) のCONSTRUCTIONフェーズはPer-Unit Loop (ユニット単位の設計サイクル) で回る
> - Functional Designは「何をするか」を技術非依存で設計する (3つの成果物) 
> - NFR Requirements / NFR Designは非機能要件を「要件→パターン→実装」の3段階で段階的に具体化する
> - DDDの戦術的設計、AWS Well-Architected Framework、ISO 25010と比較し、AI-DLCの位置づけを明らかにする

[https://extravaganzarr.s3.ap-northeast-1.amazonaws.com/aidlc-image03.png:image=https://extravaganzarr.s3.ap-northeast-1.amazonaws.com/aidlc-image03.png]

引用元：[https://aws.amazon.com/jp/blogs/news/ai-driven-development-life-cycle/:title]

---

## INCEPTIONからCONSTRUCTIONへ

第4回までで、Inceptionフェーズの主要ステージを解説しました。Workspace Detectionで現場を把握し、Requirements Analysisで要件を定義し、User Storiesでユーザーストーリーを作成し、Workflow Planningで実行計画を立て、Application Designでコンポーネント構造を設計し、Units Generationで作業単位に分割しました。

ここからCONSTRUCTIONフェーズに入ります。INCEPTIONが「何を、なぜ作るか」を決めるフェーズだったのに対し、CONSTRUCTIONは「どう作るか」を決めて実際にコードを生み出すフェーズです。

---

## Per-Unit Loop: ユニット単位で回す設計サイクル

CONSTRUCTIONフェーズには、INCEPTIONにはなかった重要な構造があります。**Per-Unit Loop**です。

### ユニットごとに1周する

INCEPTIONフェーズのUnits Generationで、システムは複数のUnit of Work (UOW) に分割されています。CONSTRUCTIONでは、このユニットごとに設計サイクルを1周回します:

```
ユニットA: Functional Design → NFR Requirements → NFR Design → Infrastructure Design → Code Generation
ユニットB: Functional Design → NFR Requirements → NFR Design → Infrastructure Design → Code Generation
ユニットC: ...
 (全ユニット完了後) 
Build and Test
```

**1つのユニットの設計と実装が完全に終わってから、次のユニットに移る**。これがPer-Unit Loopの基本ルールです。

### スプリントとの違い

一見するとアジャイルのスプリントに似ていますが、根本的な違いがあります。

| 観点 | アジャイル・スプリント | Per-Unit Loop |
|------|---------------------|---------------|
| **反復の単位** | 時間 (1〜4週間の固定期間)  | 機能 (ユニット単位)  |
| **スコープ決定** | スプリントプランニングで選択 | Inceptionで確定済み |
| **内部構造** | チームが自律的に決定 | FD→NFR Req→NFR Design→Infra→Code Genの定義されたシーケンス (各ステージはCONDITIONAL)  |
| **完了の定義** | Sprint Review + Definition of Done | 各ステージのExplicit Approval |
| **駆動力** | 時間駆動 (タイムボックス)  | 成果物駆動 (完了が次への条件)  |

スプリントは「2週間でできることをやる」という時間駆動です。Per-Unit Loopは「このユニットが完成するまで進む」という成果物駆動です。Per-Unit Loopはユニット単位の完成度を高められる反面、途中でのスコープ変更や優先順位の組み替えにはスプリントほど柔軟に対応しにくいという側面があります。また、ユニット間に依存関係がある場合、先に完了したユニットの設計が後続ユニットの要件によって見直しが必要になり、手戻りが発生する可能性もあります。逐次処理を前提としているため、複数ユニットの並行開発には向きません。どちらが優れているかではなく、人間チームの協働リズムとAI駆動の設計プロセスという、異なる文脈に最適化された設計です。

---

## Functional Design: ビジネスロジックを技術から切り離す

Per-Unit Loopの最初のステージがFunctional Designです。各ユニットのビジネスロジックを、技術的な実装から切り離して設計します。

### 「技術非依存」の意味

Functional Designの仕様書には「technology-agnostic design」と明記されています。技術非依存 (technology-agnostic) とは、「Javaで実装する」「DynamoDBに保存する」「REST APIで公開する」といった技術的な判断を一切持ち込まないということです。純粋に「このユニットが何をするか」「どんなビジネスルールがあるか」だけを定義します。

なぜ技術を持ち込まないのか？ 技術的な判断がビジネスロジックの設計に影響を与え、本来のドメインの構造から乖離するリスクがあるからです。「DynamoDBだからこのデータ構造にしよう」ではなく、「このビジネスでは顧客と注文が1対多の関係にある」というドメインの構造から出発します。技術的な実装判断は、後続のInfrastructure DesignやCode Generationに委ねます。この考え方はDDDにおける「ドメインモデルをインフラストラクチャの関心事から保護する」という思想と共通しています。

一方で、技術非依存の設計には、後続のインフラ設計やコード生成の段階で技術的制約との矛盾が発覚し手戻りが生じるリスクがあります。設計の実現可能性を早期に検証できない点は、このアプローチの制約です。

### 9ステップと3つの成果物

Functional Designは9ステップで構成され、AIが3つの成果物を生成します:

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | **business-logic-model.md** | ビジネスロジックの全体モデル。ワークフロー、データ変換、ビジネスプロセス |
| 2 | **business-rules.md** | ビジネスルール、バリデーションロジック、制約条件 |
| 3 | **domain-entities.md** | ドメインエンティティの定義、エンティティ間の関係 |

質問ファイル方式による対話プロセスは、Requirements AnalysisやUser Storiesと同じパターンです (第3回参照) 。ビジネスロジック、ドメインモデル、ビジネスルール、データフロー、統合ポイント、エラー処理、ビジネスシナリオの7カテゴリについて質問を生成し、曖昧さが残らなくなるまで対話を続けます。

---

## NFR Requirements: 「品質」を質問で洗い出す

Functional Designでビジネスロジックが固まったら、次は非機能要件 (NFR: Non-Functional Requirements) です。NFR Requirementsステージでは、品質に関する要件を洗い出します。

### 8つの質問カテゴリ

NFR Requirementsは9ステップで構成され、以下の8カテゴリで質問を生成します:

| # | カテゴリ | 質問の例 |
|---|---------|---------|
| 1 | **スケーラビリティ** | 想定負荷、成長パターン、スケーリングトリガー |
| 2 | **パフォーマンス** | 応答時間、スループット、レイテンシ |
| 3 | **可用性** | 稼働率、災害復旧、フェイルオーバー |
| 4 | **セキュリティ** | データ保護、コンプライアンス、認証・認可 |
| 5 | **技術スタック選定** | 技術的な好み、制約、既存システムとの統合 |
| 6 | **信頼性** | エラー処理、フォールトトレランス、監視 |
| 7 | **保守性** | コード品質、ドキュメント、テスト |
| 8 | **ユーザビリティ** | ユーザー体験、アクセシビリティ |

このステージの成果物は2つ:
- **nfr-requirements.md**: 非機能要件の定義
- **tech-stack-decisions.md**: 技術スタックの選定と理由

### なぜ技術スタック選定がNFRと同居するのか

技術の選択は非機能要件と密接に関わるため、技術スタックの選定はNFR Requirementsに含まれています。「レスポンスタイム数ミリ秒以内」という要件があればインメモリDBが候補になりますし、「年間稼働率99.99%」ならマネージドサービスの活用が有力になります。NFRが決まるタイミングで技術を選ぶことで、要件と技術の整合性を取りやすくなります。なお、ここでの技術スタック選定は言語・フレームワーク・データベースエンジンといった技術プラットフォームの選定であり、具体的なクラウドサービス (AWS/Azure/GCP等) へのマッピングは後続のInfrastructure Designで行います。

---

## NFR Design: パターンで品質を組み込む

NFR Requirementsで「何が必要か」が定まったら、NFR Designで「どう実現するか」をパターンとして設計します。

### 2つの成果物

NFR Designも9ステップで構成され、AIが2つの成果物を生成します:

| # | 成果物 | 内容 |
|---|--------|------|
| 1 | **nfr-design-patterns.md** | レジリエンス、スケーラビリティ、パフォーマンス、セキュリティのパターン |
| 2 | **logical-components.md** | キュー、キャッシュ、ロードバランサーなどの論理的なインフラコンポーネント |

ここで重要なのは「論理コンポーネント」という概念です。NFR Designで定義するのは「キャッシュが必要」「メッセージキューが必要」という論理的な要件であり、「Redis」「SQS」という具体的な製品の選択ではありません。具体的な製品へのマッピングは、後続のInfrastructure Designで行います。

### 「要件→パターン→実装」の3段階

NFR Requirements (要件)  → NFR Design (パターン)  → Infrastructure Design (実装) という3段階は、第4回で解説したInceptionフェーズの「計画→構造→分割」と同じ発想を、ConstructionフェーズのNFR設計にも適用した一例です。抽象度を段階的に下げていきます。ただし、3段階のプロセスは各段階で対話と承認のコストを伴います。小規模なプロジェクトや単純な非機能要件の場合、このオーバーヘッドが設計の迅速さを損なう可能性があります。

```
NFR Requirements:  「レスポンスタイム100ms以内、可用性99.99%」
       ↓
NFR Design:        「キャッシュパターン、サーキットブレーカーパターン」
       ↓
Infrastructure Design: 「ElastiCache (Redis)、ALBヘルスチェック」
```

---

## 既存手法との比較: 品質設計の系譜

### DDDの戦術的設計

Eric Evansが2003年に提唱したDDDには、「戦略的設計」と「戦術的設計」の2つの側面があります。戦略的設計はBounded ContextやContext Mapでドメインの大きな構造を整理するもので、第3回のユビキタス言語で触れました。戦術的設計は、その構造の内部でドメインモデルを実装するための具体的なパターン群です。

Evansの原著で定義された戦術的設計の主要なパターン (Building Blocks) は以下の7つです:

| パターン | 役割 |
|---------|------|
| **Entity** | 一意のアイデンティティを持つオブジェクト。属性が変わっても同一性が保たれる |
| **Value Object** | 不変のオブジェクト。値だけで定義され、アイデンティティを持たない |
| **Aggregate** | Aggregate Rootを起点とするEntityとValue Objectの集合体。トランザクション整合性の境界を形成する |
| **Repository** | Aggregateの永続化を抽象化するインターフェース |
| **Service** | 特定のEntityに属さないドメインロジックを保持する |
| **Factory** | 複雑なドメインオブジェクトの生成を担当する |
| **Module** | 関連するドメインオブジェクトをまとめ、凝集度を高める |

※ 上記に加え、DDDコミュニティでは**Domain Event** (ドメイン内で起きた意味のある出来事を表現する) も重要なパターンとして広く認知されています。Evansの原著には含まれていませんが、後にVaughn Vernonの『Implementing Domain-Driven Design』(2013) で体系化されました。

AI-DLCのFunctional Designが生成する`domain-entities.md`は、DDDのEntity、Value Object、Aggregateと共通する要素が見られます。`business-rules.md`はServiceやAggregate内のビジネスルールと重なる領域を扱っています。

ただし、AI-DLCはDDDの「ドメインモデリング」に近い部分を扱いつつも、Repository、Factoryなどの実装パターンには踏み込みません。実装パターンはCode Generationステージの領域です。AI-DLCは、DDDの戦術的設計が一体として扱う領域を、「ビジネスロジック設計 (Functional Design) 」と「実装 (Code Generation) 」の2つのステージに分離しています。DDDが一体として扱うのは、ドメインモデルと実装コードの一致を重視する設計思想に基づいており、この分離が常に望ましいとは限りません。

### AWS Well-Architected Framework

AWS Well-Architected Frameworkは、クラウドアーキテクチャの品質を評価するフレームワークです。2015年にホワイトペーパーが公開された当初は5つの柱で構成されていましたが、2021年にSustainability柱が追加され、現在は6つの柱となっています。

| 柱 | 焦点 | AI-DLC NFRカテゴリとの対応 |
|----|------|--------------------------|
| **Operational Excellence** | 運用・監視・改善 | 保守性 (部分的)  |
| **Security** | 情報とシステムの保護 | セキュリティ |
| **Reliability** | 障害復旧、可用性 | 可用性、信頼性 |
| **Performance Efficiency** | リソースの効率的使用 | パフォーマンス、スケーラビリティ |
| **Cost Optimization** | コスト管理 |  (AI-DLCでは明示なし)  |
| **Sustainability** | 環境負荷の最小化 |  (AI-DLCでは明示なし)  |

AI-DLCのNFR Requirementsの8カテゴリは、Well-Architectedの6つの柱の多くをカバーしています。ただし、Cost OptimizationとSustainabilityはAI-DLCのNFRカテゴリに明示的には含まれていません。AI-DLCがソフトウェアの設計品質にスコープを絞っているためと考えられます。運用コストや環境負荷は、AI-DLCの枠組みでは別の観点として扱われます。

一方、AI-DLCには「技術スタック選定」という独自カテゴリがあります。Well-Architectedは特定の技術選択を推奨しませんが、AI-DLCは設計プロセスの中で技術選択を明示的に行い、その理由を記録します。

### ISO 25010: ソフトウェア品質の国際標準

ISO 25010は、ソフトウェア品質を体系的に分類する国際標準です。2011年版では8つの品質特性、2023年の改訂版では9つの品質特性を定義しています。

| ISO 25010 品質特性 | 対応するAI-DLC NFRカテゴリ | 重複する領域 |
|-------------------|--------------------------|-------------|
| 機能適合性 | Functional Design (別ステージ)  | 間接 |
| 性能効率性 | パフォーマンス | 多い |
| 互換性 |  (Tech Stack Selectionで部分的に考慮)  | 一部 |
| 使用性 | ユーザビリティ | 多い |
| 信頼性 | 可用性、信頼性 | 多い |
| セキュリティ | セキュリティ | 多い |
| 保守性 | 保守性 | 多い |
| 移植性 |  (Tech Stack Selectionで間接的に考慮)  | 少ない |
| 安全性 ※2023年追加 |  (AI-DLCでは明示なし)  | 少ない |

ISO 25010は品質の**分類体系 (タクソノミー) **であり、「何を測るか」を定義します。AI-DLCのNFR Requirements/NFR Designは品質の**設計プロセス**であり、「どう実現するか」を扱います。ただし、ISO 25010にもISO 25040 (評価プロセス) が対として存在し、Well-Architected FrameworkにもWell-Architected Reviewという設計レビュープロセスがあります。AI-DLCはこれらと異なるアプローチで品質の設計プロセスを定義しており、両者は補完的な関係にあります。

---

## まとめ

第5回はCONSTRUCTIONフェーズ前半のPer-Unit Loop・Functional Design・非機能要件の扱いについて説明しました。今回学んだことは以下です。

- CONSTRUCTIONフェーズはPer-Unit Loopで回ります。時間ではなくユニット (機能単位) を反復の軸とする、成果物駆動の設計サイクルです。ただし逐次処理のため並行開発には向かず、ユニット間の依存関係による手戻りリスクがあります
- Functional Design (9ステップ) は技術非依存でビジネスロジックを設計します。DDDの戦術的設計のうち「ドメインモデリング」に近い発想に基づいていますが、後工程での技術制約との矛盾による手戻りリスクを伴います
- NFR Requirements (9ステップ) は8カテゴリの質問で品質要件を洗い出し、NFR Design (9ステップ) はパターンで設計に落とし込みます
- 「要件→パターン→実装」の3段階で抽象度を段階的に下げていきますが、小規模プロジェクトではオーバーヘッドとなりえます
- AWS Well-Architected Frameworkの6つの柱、ISO 25010の品質特性体系と、AI-DLCのNFRカテゴリは多くの領域で重なります。AI-DLCは品質の設計プロセスを明示的に定義している点に特徴がありますが、Well-ArchitectedやISO 25040にもそれぞれ独自の評価・レビュープロセスが存在します

---

## 次回予告

第6回では、CONSTRUCTIONフェーズの後半戦を取り上げます。Infrastructure Design (論理設計を物理インフラに落とす) 、Code Generation (計画→承認→生成のプロセス) 、Build and Test (6種類のテスト戦略) を、Infrastructure as Code、TDD/BDD、CI/CDパイプラインと比較しながら解説します。
