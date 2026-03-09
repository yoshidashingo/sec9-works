# AI-DLCを完全理解する 第12回: Operationsと拡張レイヤーについて

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

> **これだけは覚えて帰ってね💡**
>
> - operations.mdはわずか20行のプレースホルダー。「未完成であること」が将来への拡張余地を示す
> - AI-DLCはベースレイヤー (標準ルール) ＋拡張レイヤー (独自カスタマイズ) の二層構造で運用できる
> - ルール適用の優先度は core-workflow.md > 拡張レイヤー > ベースレイヤー
> - AI-DLCは「完成品」ではなく「拡張可能なプラットフォーム」として設計されている

---

## operations.md: 20行が語る将来ビジョン

### 全文

operationsディレクトリにはファイルが1つだけ。operations.mdの全文はこうです:

```markdown
# Operations

**Purpose**: Placeholder for future operational phases (deployment, monitoring, maintenance)

**Status**: This phase is currently a placeholder and will be expanded in future versions.

## Future Scope

The Operations phase will eventually include:
- Deployment planning and execution
- Monitoring and observability setup
- Incident response procedures
- Maintenance and support workflows
- Production readiness checklists

## Current State

All build and test activities have been moved to the CONSTRUCTION phase.
The AI-DLC workflow currently ends after the Build and Test phase in CONSTRUCTION.
```

わずか20行。INCEPTIONの7ファイル (合計1,713行) やCONSTRUCTIONの6ファイル (合計962行) と比べれば、その簡潔さは圧倒的です。

### プレースホルダーが語る5つの将来機能

operations.mdが列挙する将来機能は5つです:

| # | 機能 | 想定される内容 |
|---|------|-------------|
| 1 | Deployment planning and execution | デプロイ計画と実行手順 |
| 2 | Monitoring and observability setup | モニタリングと可観測性の構築 |
| 3 | Incident response procedures | インシデント対応手順 |
| 4 | Maintenance and support workflows | 保守・サポートのワークフロー |
| 5 | Production readiness checklists | 本番準備チェックリスト |

第1回で「DevOpsが導入した『開発から運用まで一気通貫で面倒を見る』という考え方は、AI-DLCの3フェーズ構成にも共通している」と解説しましたが、現時点でその「運用」部分は空白です。しかしこの空白は、公式にはプレースホルダーとして位置づけられています。operations.md自身が「Status: This phase is currently a placeholder」と明記している通りです。

第1回で解説した通り、AI-DLCは2025年にオープンソースとして公開されたフレームワークです。INCEPTIONとCONSTRUCTIONが先に充実し、OPERATIONSは将来の拡張に委ねられています。ソフトウェア開発における「MVP (Minimum Viable Product: 必要最低限の製品) 」に通じる考え方で、まず最も価値のある部分から実装し、段階的に拡張する戦略です。

---

## AI-DLCのカスタマイズ: 二層構造

### ベースレイヤーと拡張レイヤー

AI-DLCのルールファイル群は、そのまま使うこともできますが、組織やプロジェクトに合わせてカスタマイズすることも可能です。core-workflow.mdが規定するのはベースレイヤー (aws-aidlc-rule-details/) の読み込みのみですが、利用者側でこれに拡張レイヤーを追加する**二層構造**の運用パターンが考えられます。

```
.steering/
  aws-aidlc-rules/
    core-workflow.md           # マスターワークフロー (変更不可) 
  aws-aidlc-rule-details/      # ベースレイヤー (変更不可) 
    common/
    inception/
    construction/
    operations/
  [organization]-aidlc-rule-details/  # 拡張レイヤー (自由にカスタマイズ) 
    ...
```

- **ベースレイヤー** (aws-aidlc-rule-details/) : AI-DLC標準のルール詳細。変更不可
- **拡張レイヤー** ([organization]-aidlc-rule-details/) : 組織独自の知見・ノウハウを格納。自由にカスタマイズ可能

ベースレイヤーを変更しない理由は明確です。AI-DLCが公式にアップデートされたとき、ベースレイヤーを差し替えるだけで最新のルールを取り込めます。拡張レイヤーには手を入れていないため、アップデートの影響を受けません。ライブラリ本体に手を入れずに、拡張ポイントを通じて機能を追加する発想と同じです。

### ルール読み込みの優先順位

二層構造を運用する際のルール読み込み手順は以下の通りです:

1. **aws-aidlc-rule-details** から該当ステージのルールファイルを読み込む
2. **拡張レイヤー** に同名または関連するファイルが存在する場合、追加で読み込む
3. 両方のルールを統合して適用する

競合がある場合の優先順位:

| 優先度 | ソース | 役割 |
|-------|--------|------|
| 最優先 | core-workflow.md | プロセスフロー (変更不可)  |
| 高 | 拡張レイヤー | 業界・業務固有のルール |
| ベース | aws-aidlc-rule-details | 標準ルール |

拡張レイヤーはベースレイヤーを「上書き」するのではなく「補完・拡張」します。たとえば、ベースレイヤーのrequirements-analysis.mdが複数の質問カテゴリを定義している場合、拡張レイヤーで「金融業界固有の質問カテゴリ」を追加できます。元のカテゴリは残したまま、業界固有の観点を加える形です。

### 拡張レイヤーで何をカスタマイズするか

拡張レイヤーに格納する典型的な内容は以下の通りです:

- **業界コンテキスト**: 顧客業界に固有の規制、基準、考慮事項
- **品質基準**: 組織独自のレビュー観点、品質チェックリスト
- **成果物テンプレート**: 組織流のドキュメントフォーマット
- **サービスマッピング**: 自社のサービスメニューとAI-DLCのステージの対応付け
- **用語定義**: 業界用語や組織固有の用語の統一

AI-DLCは特定の業界や組織に最適化されていない汎用フレームワークですが、拡張レイヤーの仕組みにより、さまざまな業界・組織の要件に合わせたカスタマイズが可能です。

---

## ワークフロー定義ファイル群の全体像

第8回〜第11回で解説してきたすべてのファイルを、1つの表にまとめましょう。

### core-workflow.md (1ファイル) 

AI-DLC全体の「憲法」。4つのMANDATORYルール、3フェーズ定義、8つのKey Principles、チェックボックス追跡、監査ログルールを含みます。

### common/ (11ファイル) 

| ファイル | 一言で言うと |
|---------|-----------|
| process-overview.md | AIモデル向け全体図 (Mermaid)  |
| welcome-message.md | ユーザー向けウェルカムメッセージ |
| session-continuity.md | セッション再開テンプレート |
| question-format-guide.md | 質問ファイル方式のルール |
| depth-levels.md | 適応的深度の定義 |
| terminology.md | 用語集 |
| overconfidence-prevention.md | 過信防止ガイド |
| content-validation.md | コンテンツ検証ルール |
| ascii-diagram-standards.md | ASCII図表の標準規格 |
| workflow-changes.md | ワークフロー変更管理 |
| error-handling.md | エラー処理と復旧手順 |

### inception/ (7ファイル) 

| ファイル | ステップ数 | 成果物数 | 分類 |
|---------|----------|---------|------|
| workspace-detection.md | 6 | 1 | ALWAYS |
| reverse-engineering.md | 12 | 8+1 | CONDITIONAL |
| requirements-analysis.md | 9 | 1-2 | ALWAYS |
| user-stories.md | 23 | 2 | CONDITIONAL |
| workflow-planning.md | 11 | 1 | ALWAYS |
| application-design.md | 15 | 4 | CONDITIONAL |
| units-generation.md | 19 | 3 | CONDITIONAL |

### construction/ (6ファイル) 

| ファイル | ステップ数 | 成果物数 | 分類 |
|---------|----------|---------|------|
| functional-design.md | 9 | 3 | CONDITIONAL |
| nfr-requirements.md | 9 | 2 | CONDITIONAL |
| nfr-design.md | 9 | 2 | CONDITIONAL |
| infrastructure-design.md | 9 | 2-3 | CONDITIONAL |
| code-generation.md | 16 | 多数 | ALWAYS |
| build-and-test.md | 10 | 5+ | ALWAYS |

### operations/ (1ファイル) 

| ファイル | 状態 |
|---------|------|
| operations.md | プレースホルダー |

**合計: 1 + 11 + 7 + 6 + 1 = 26ファイル**。これがAI-DLCのワークフロー定義の全体です。

---

## シリーズ総括: AI-DLCが変える開発の風景

### 12回で見えてきたもの

第1回から第12回まで、AI-DLCの全体像を見てきました。ここで、シリーズ全体を通じて見えてきたAI-DLCの本質をまとめます。

**AI-DLCは「AIにどうコーディングさせるか」のフレームワークではありません。「AIにどう開発プロセスを回させるか」のフレームワークです。**

従来の開発手法では、プロセスの設計と運用は人間の仕事でした。ウォーターフォールのプロジェクトマネージャーも、アジャイルのスクラムマスターも、DevOpsのプラットフォームチームも、「次に何をすべきか」を決めるのは人間でした。AI-DLCはこの前提を変え、ルールファイル群の指示に基づいてAIがプロセスを進行します。

ただし「AIに丸投げ」ではありません。12回を通じて繰り返し見てきた通り、AI-DLCには以下の仕組みが組み込まれています:

- **承認ゲート**: ほぼすべてのステージで人間の承認が必要
- **質問ファイル方式**: AIが「分かったつもり」で進まないための構造化された対話
- **過信防止**: 「聞きすぎるくらい聞け」という設計思想
- **監査証跡**: すべてのやり取りがタイムスタンプ付きで記録される
- **NO EMERGENT BEHAVIOR**: AIが独自の判断で新しいパターンを生み出すことは認められていない
- **適応型ワークフロー**: タスクの複雑さに応じてプロセスが自動で伸び縮みする

これらは、AIの出力を適切に検証しながら活用するための設計です。

### 26ファイルが形成する構造

26のファイルは、以下の階層構造を形成しています:

```
core-workflow.md          ← 全体を規定する「憲法」
  ├── common/             ← すべてのステージに適用されるメタルール
  ├── inception/          ← Inceptionの各ステージのルール
  ├── construction/       ← CONSTRUCTIONの各ステージのルール
  └── operations/         ← 将来拡張用のプレースホルダー
```

この構造には、ソフトウェアアーキテクチャの基本原則が見て取れます:

- **関心の分離**: フェーズ別、ステージ別にファイルを分離
- **DRY原則**: commonディレクトリで共通ルールを一元管理
- **開放閉鎖原則**: ベースレイヤーを変更せずに拡張レイヤーで拡張
- **段階的具体化**: core-workflow.md (抽象) → 個別ファイル (具体) 

AI-DLCのワークフロー定義ファイル群は、それ自体がこれらのソフトウェア設計原則を反映した構造になっています。

### AI-DLCの未来

OPERATIONSフェーズの空白は、AI-DLCの現在地を正直に示しています。コードの生成とテストまではAIが主導できますが、AI-DLCの現バージョンでは、デプロイ・モニタリング・インシデント対応はまだ対象範囲外です。

しかし、INCEPTIONとCONSTRUCTIONの仕組みを見れば、OPERATIONSが充実したときの姿は想像できます。デプロイ計画の策定、モニタリングの設定、インシデント対応手順の生成 ― これらもALWAYS/CONDITIONALの適応型ワークフローで実行され、承認ゲートと監査証跡により品質を高める設計が適用されると推測されます。

AI-DLCは「完成品」ではありません。拡張レイヤーによるカスタマイズとOPERATIONSフェーズの将来実装を前提とした「拡張可能なプラットフォーム」です。

---

## まとめ

第12回はOPERATIONSフェーズの現状と、AI-DLCのカスタマイズの仕組みについて説明しました。今回学んだことは以下です。

- operations.mdは20行のプレースホルダーで、5つの将来機能 (デプロイ、モニタリング、インシデント対応、保守、本番準備) を予告します
- AI-DLCはベースレイヤー＋拡張レイヤーの二層構造でカスタマイズ可能です。ベースレイヤーは変更不可、拡張レイヤーで組織固有のルールを追加します
- ワークフロー定義の全体は26ファイルで構成されます (core-workflow 1 + common 11 + inception 7 + construction 6 + operations 1) 
- 本シリーズで述べた通り、AI-DLCの本質は「ルールファイル群に基づくAI主導の開発プロセス」にあります
- 26ファイルの構造自体が、関心の分離、DRY原則、開放閉鎖原則、段階的具体化というソフトウェア設計の原則を反映しています
- AI-DLCは「完成品」ではなく「拡張可能なプラットフォーム」として設計され、拡張レイヤーとOPERATIONSフェーズの将来実装を前提としています
