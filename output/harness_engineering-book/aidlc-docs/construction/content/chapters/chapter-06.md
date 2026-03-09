# 第6章: 長期実行エージェントの実装パターン

> **読者レベル**: ★★★（上級 — エージェント開発経験のある読者向け）
> **想定ページ数**: 約40ページ

> **本章の位置づけ**: 第3章で概観した各コンポーネントの**具体的な実装パターン（HOW）**を、長期実行エージェントという最も挑戦的なユースケースを通じて解説する。

AIエージェントが単発の質問応答や短いコード生成を超えて、数時間から数日にわたるソフトウェア開発タスクを自律的に遂行する——これが「長期実行エージェント」（Long-Running Agent）の世界である。第3章ではエージェントハーネスの6つのコンポーネントを「何があるか（WHAT）」の観点から整理した。本章では、それらのコンポーネントを「どう実装するか（HOW）」の観点から、長期実行という最も挑戦的なユースケースを通じて具体的に解説する。

長期実行エージェントは、ハーネスエンジニアリングのすべての課題が集約される場所である。コンテキストウィンドウの制約、セッション間の状態消失、品質の劣化、方向性の逸脱——これらの問題は、実行時間が長くなるほど顕在化する。逆に言えば、長期実行エージェントのハーネスを適切に設計できれば、短期実行のエージェントは自然に信頼性の高いものとなる。

本章では、Anthropicの2エージェントアーキテクチャ（ANT-01）、LangChainの推論サンドイッチパターン（LC-08）、Open SWEの3段階構造（LC-17）など、業界の最先端で実証された実装パターンを体系的に解説する。各パターンには具体的なコード例を添え、読者が自身のプロジェクトに適用できる実践的な知見を提供する。

---

## 6.1 なぜ長期実行が難しいのか

長期実行エージェントの設計に入る前に、なぜ長期実行がこれほど困難なのかを3つの根本的な制約から理解する必要がある。

### コンテキストウィンドウの物理的制約とコンテキストロット

LLMのコンテキストウィンドウは、第2章で導入したOSメタファーにおける「RAM」に相当する（LC-11）。2026年現在、主要モデルのコンテキストウィンドウは100Kから200Kトークン程度であり、一見すると十分に大きく見える。しかし、長期実行エージェントにとって、この容量は決して潤沢ではない。

典型的なコーディングエージェントのセッションを考えてみよう。システムプロンプトに2,000トークン、ツール定義に5,000トークン、プロジェクトのコンテキスト（ディレクトリ構造、設定ファイル、関連コード）に10,000トークン——これだけで全体の約10%が消費される。さらに、ツールの実行結果は1回あたり数千トークンに達することも珍しくない。100回のツールコールを行えば、それだけで数十万トークンに到達し、コンテキストウィンドウを圧迫する。

問題は容量の枯渇だけではない。Anthropicのエンジニアリングチームは、コンテキストが増大するにつれてモデルの性能が劣化する現象を「コンテキストロット」（Context Rot）と名づけた（ANT-03）。コンテキストウィンドウに情報が蓄積されるほど、モデルは重要な情報と不要な情報の区別が困難になり、指示への追従性が低下する。これは「コンテキストウィンドウが大きければ大きいほど良い」という素朴な期待に反する、実践上きわめて重要な知見である。

コンテキストロットの影響は定量的にも確認されている。LangChainチームのTerminal Bench 2.0実験では、コンテキスト管理を適切に行わないエージェントは、長時間のタスクにおいて明確なスコア低下を示した（LC-08）。コンテキストが肥大化すると、モデルは直近のツール出力に過度に注目し、セッション冒頭で与えられたタスク目標やコーディング規約を「忘れる」傾向が顕著になるのである。

```
┌─────────────────────────────────────────────────────┐
│              コンテキストウィンドウ (200K tokens)        │
│                                                       │
│  ┌──────────┐  開始時: クリーンな状態                   │
│  │System    │  - 指示が明確                            │
│  │Prompt    │  - ツール定義が適切に配置                  │
│  │(2K)      │  - 十分な空き容量                         │
│  ├──────────┤                                         │
│  │Tools     │                                         │
│  │(5K)      │                                         │
│  ├──────────┤                                         │
│  │Context   │                                         │
│  │(10K)     │                                         │
│  ├──────────┤                                         │
│  │          │                                         │
│  │  空き    │  ← 183K tokens 利用可能                  │
│  │          │                                         │
│  └──────────┘                                         │
│                                                       │
│  ┌──────────┐  100回のツールコール後: コンテキストロット   │
│  │System    │  - 初期指示が「埋もれる」                  │
│  │(2K)      │  - 不要な中間結果が蓄積                    │
│  │Tools(5K) │  - モデルの注意が分散                      │
│  │Context   │  - 品質が劇的に低下                       │
│  │(10K)     │                                         │
│  │──────────│                                         │
│  │ Tool結果 │                                         │
│  │ (50K)    │                                         │
│  │──────────│                                         │
│  │ 会話履歴 │                                         │
│  │ (80K)    │                                         │
│  │──────────│                                         │
│  │ 最新結果 │                                         │
│  │ (40K)    │                                         │
│  └──────────┘  ← 空き 13K tokens                      │
└─────────────────────────────────────────────────────┘
```

[図6.1: コンテキストウィンドウの消費とコンテキストロットの進行]

### セッション間の状態消失問題

LLMは本質的にステートレスである。1つの推論呼び出しが完了すれば、そのセッションで蓄積されたすべての文脈——実装の方針決定、試行錯誤の経緯、中間成果物の所在——は失われる。これは、人間のエンジニアが退勤時に翌日の自分へメモを残さずに帰るようなものである。

短期実行のエージェントでは、この特性は大きな問題にならない。単一のセッション内でタスクを完結できるからである。しかし、長期実行エージェントでは事情が異なる。大規模なリファクタリング、機能追加、複数日にわたるプロジェクト——これらのタスクは、必然的に複数のセッションをまたいで遂行される。

Anthropicのエンジニアリングチームは、この問題を「状態消失」（State Loss）と呼び、長期実行エージェントにおける最も根本的な課題の1つとして位置づけた（ANT-01）。新しいセッションが開始されるたびに、エージェントは「まっさらな状態」から始まる。前のセッションで何を実装したのか、どのファイルを変更したのか、どのテストが通っていてどのテストが失敗しているのか——これらの情報を何らかの方法で新しいセッションに引き継がなければ、エージェントは同じ作業を繰り返したり、矛盾した変更を加えたりするリスクがある。

### Time Blindness（時間盲目性）

長期実行エージェントが直面する第3の制約は、モデルが「時間」の感覚を持たないことである。人間のエンジニアは、タスクに着手して30分が経過すれば「そろそろ方向性を確認しよう」と感じる。1時間経過すれば「このアプローチは正しいのか」と自問する。しかし、LLMにはこの「時間感覚」が存在しない。

LangChainチームは、この特性を「Time Blindness（時間盲目性）」と表現した。エージェントは、タスク開始から何分経過したか、残り時間がどれくらいあるか、現在のペースで期限に間に合うかといった判断ができない。この時間盲目性は、2つの深刻な問題を引き起こす。

第一に、**リソースの浪費**である。エージェントは、些末な問題に過度の時間を費やし、本質的に重要なタスクに取り組む時間が不足するという事態に陥りやすい。Terminal Bench 2.0のような時間制限のあるベンチマークでは、この問題がタイムアウト失敗として直接的にスコアに反映される（LC-08）。

第二に、**停止判断の欠如**である。人間であれば「このアプローチは行き詰まっている。別の方法を試そう」と判断できる局面で、エージェントは同じアプローチを際限なく繰り返す可能性がある。これが後述する「破滅ループ」（Doom Loop）の一因でもある。

### 3つの制約の相互作用

これら3つの制約——コンテキストロット、状態消失、時間盲目性——は独立した問題ではなく、相互に増幅し合う。コンテキストロットが進行すると、エージェントは自身の進捗状況を正確に把握できなくなり、状態消失と類似の症状を引き起こす。時間盲目性により、エージェントはコンテキストが枯渇しつつあることに気づかず、重要度の低い情報でコンテキストウィンドウを埋め尽くす。

```
     コンテキストロット
        ↗         ↘
    増幅            増幅
    ↑                  ↓
時間盲目性  ←  増幅  →  状態消失
```

[図6.2: 3つの制約の相互増幅関係]

長期実行エージェントのハーネス設計とは、この3つの制約に対するシステマティックな対策を構築することに他ならない。以降のセクションでは、それぞれの制約に対する具体的な実装パターンを順に解説していく。

---

## 6.2 Initializer Agent + Coding Agent パターン

### Anthropicの2エージェントアーキテクチャ

長期実行エージェントの実装パターンとして、Anthropicが提案した「Initializer Agent + Coding Agent」の2エージェントアーキテクチャは、そのシンプルさと実効性において最も優れた出発点である（ANT-01）。

このパターンの核心的な洞察は、長期実行タスクを「1つの万能エージェント」に任せるのではなく、**2つの特化型エージェント**に分離するという設計判断にある。

```
┌────────────────────────────────────────────────────┐
│              長期実行タスク全体                        │
│                                                      │
│  ┌──────────────────┐    ┌──────────────────┐       │
│  │ Initializer Agent │───→│  Coding Agent    │       │
│  │ （初期化エージェント）│    │（実装エージェント）│       │
│  │                  │    │                  │       │
│  │ ・環境セットアップ  │    │ ・増分的実装       │       │
│  │ ・git初期化        │    │ ・テスト実行       │       │
│  │ ・機能リスト作成    │    │ ・コミット         │       │
│  │ ・進捗ファイル初期化 │    │ ・進捗ファイル更新  │       │
│  │                  │    │                  │       │
│  │  1回のみ実行       │    │  繰り返し実行      │       │
│  └──────────────────┘    └──────────────────┘       │
│         ↓                        ↑                   │
│         └──── claude-progress.txt ────┘               │
│              （状態ブリッジ）                            │
└────────────────────────────────────────────────────┘
```

[図6.3: Initializer Agent + Coding Agent の2エージェントアーキテクチャ]

### Initializerの役割

Initializer Agent（初期化エージェント）は、プロジェクトの「足場」を組むことに特化したエージェントである。その責務は明確に限定されている。

**1. 環境セットアップ**

Initializerは、プロジェクトのディレクトリ構造を解析し、必要な開発環境を整備する。既存のプロジェクトであれば、コードベースの構造を把握し、ビルドシステム、テストフレームワーク、依存関係を理解する。新規プロジェクトであれば、適切なディレクトリ構造とビルド設定を生成する。

**2. git初期化**

Initializerは、gitリポジトリの初期状態を確立する。これは単に`git init`を実行するだけではない。適切な`.gitignore`の設定、初期コミットの作成、そしてCoding Agentが増分的にコミットできるブランチ戦略の確立を含む。gitの状態はCoding Agentにとって「復帰ポイント」として機能するため、その初期設定は極めて重要である。

**3. 機能リスト作成**

Initializerの最も重要な責務は、タスクを構造化された機能リストに分解することである。この機能リストは、Coding Agentが「次に何をすべきか」を判断するための羅針盤となる。

```markdown
# 機能リスト: Webアプリケーションのユーザー認証機能

## 完了済み
- なし

## 進行中
- なし

## 未着手
1. [ ] ユーザーモデルの定義（User model with email, password_hash, created_at）
2. [ ] パスワードハッシュ化ユーティリティ（bcrypt使用）
3. [ ] 登録エンドポイント（POST /api/auth/register）
4. [ ] ログインエンドポイント（POST /api/auth/login）
5. [ ] JWTトークン生成・検証ミドルウェア
6. [ ] 認証保護付きエンドポイントのサンプル
7. [ ] ユニットテスト（モデル、ユーティリティ）
8. [ ] 統合テスト（API エンドポイント）
9. [ ] エラーハンドリングとバリデーション
10. [ ] ログアウトとトークン無効化
```

**4. 進捗ファイルの初期化**

Initializerは、`claude-progress.txt`（または同等の進捗ファイル）を作成し、Coding Agentとの間の「状態ブリッジ」を初期化する。この進捗ファイルについては次節（6.3）で詳述する。

以下は、Initializerの実装例である。

```python
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

INITIALIZER_SYSTEM_PROMPT = """あなたはプロジェクト初期化の専門家です。
以下の手順を厳密に実行してください:

1. プロジェクトのディレクトリ構造を解析する
2. 必要な開発環境をセットアップする
3. gitリポジトリを初期化する（未初期化の場合）
4. タスクを構造化された機能リストに分解する
5. claude-progress.txt を以下のフォーマットで作成する:

## プロジェクト概要
[タスクの概要を1-2文で記載]

## 完了済み機能
- なし

## 進行中の機能
- なし

## 未着手の機能
[番号付きリストで全機能を列挙]

## 技術的な決定事項
[アーキテクチャ上の決定を記録]

## 既知の問題
- なし

重要: 実装コードは一切書かないでください。
あなたの役割は「足場を組む」ことであり、「建物を建てる」ことではありません。
"""

def create_initializer_agent(tools, model="claude-sonnet-4-20250514"):
    """初期化エージェントを生成する"""
    return create_react_agent(
        model=model,
        tools=tools,
        prompt=INITIALIZER_SYSTEM_PROMPT,
    )
```

### Coding Agentの役割

Coding Agent（実装エージェント）は、Initializerが整えた足場の上で、実際のコード実装を増分的に進めるエージェントである。Coding Agentの設計における最も重要な原則は「増分性」（Incrementality）である。

**1. 増分的進捗**

Coding Agentは、機能リストの項目を1つずつ実装する。1つの機能が完了したら、次の機能に進む前に必ず以下のステップを実行する。

**2. テスト実行**

実装した機能に対するテストを作成し、実行する。テストが通過しない場合は、テストが通過するまで修正を繰り返す。

**3. コミット**

テストが通過したら、変更をgitにコミットする。コミットメッセージには、実装した機能の概要を明記する。

**4. 進捗ファイル更新**

最も重要なステップとして、`claude-progress.txt`を更新し、完了した機能を「完了済み」に移動する。これにより、仮にCoding Agentのセッションが途中で終了しても、次のセッションは進捗ファイルを読むことで中断箇所から再開できる。

```python
CODING_AGENT_SYSTEM_PROMPT = """あなたは実装エージェントです。
セッション開始時に必ず以下を実行してください:

1. claude-progress.txt を読み込む
2. git log --oneline -20 で最近のコミット履歴を確認する
3. 未着手の機能リストから次のタスクを選択する

実装サイクル（各機能ごとに繰り返し）:
1. 機能を実装する
2. テストを作成する
3. テストを実行する（失敗時は修正）
4. git add && git commit する
5. claude-progress.txt を更新する
   - 完了した機能を「完了済み」に移動
   - 技術的な決定事項があれば記録
   - 既知の問題があれば記録

重要な制約:
- 1回のセッションで全機能を完了する必要はない
- 各機能は独立してコミット可能な単位であること
- 進捗ファイルの更新を絶対に忘れないこと
- 進捗ファイルは「次のセッションの自分」への引き継ぎ書である
"""

def create_coding_agent(tools, model="claude-sonnet-4-20250514"):
    """実装エージェントを生成する"""
    return create_react_agent(
        model=model,
        tools=tools,
        prompt=CODING_AGENT_SYSTEM_PROMPT,
    )
```

### 2エージェント分離の設計上の利点

InitializerとCoding Agentを分離する設計には、3つの明確な利点がある。

**第一に、コンテキストの最適化**である。Initializerは「全体像の把握と計画」に特化し、Coding Agentは「個別機能の実装」に特化する。それぞれのエージェントが必要とする情報は異なるため、コンテキストウィンドウの無駄遣いを避けることができる。

**第二に、障害の局所化**である。Coding Agentが実装中にエラーや方向性の逸脱を起こしても、Initializerが作成した機能リストと進捗ファイルが「錨」（アンカー）として機能する。新しいCoding Agentセッションを起動すれば、正しい方向からやり直すことができる。

**第三に、専門化によるプロンプト効率**である。1つの巨大なシステムプロンプトで「計画も実装もテストもすべてやれ」と指示するよりも、それぞれの役割に特化したプロンプトの方が、モデルの追従性が高い。これは、第2章で議論したコンテキストエンジニアリングの「Isolate（分離）」戦略（LC-11）の直接的な応用である。

---

## 6.3 進捗ブリッジングの実装

### claude-progress.txt パターンの具体的な実装

進捗ブリッジング（Progress Bridging）とは、セッション間の状態消失問題を解決するために、エージェントの進捗状況をファイルシステム上に永続化し、新しいセッションがそのファイルを読み込むことで文脈を復元する手法である（ANT-01, BLG-07）。

`claude-progress.txt`はAnthropicが提案したパターン名であるが、その本質は特定のファイル名やフォーマットにあるのではない。重要なのは、「エージェントが自身の状態を構造化された形で外部に書き出し、次のセッションがそれを読み込む」というアーキテクチャパターンである。これは、第2章で解説したコンテキストエンジニアリングの4戦略のうち「Write（外部永続化）」と「Select（必要時取得）」の組み合わせに相当する（LC-11）。

以下は、進捗ブリッジングの実装において必要な要素を網羅した、より詳細なフォーマット例である。

```markdown
# プロジェクト進捗: ECサイトの注文管理API

## 最終更新
- セッションID: session-2026-02-15-003
- 更新日時: 2026-02-15T14:32:00Z
- 完了機能数: 5/12

## プロジェクト概要
ECサイトのバックエンドAPIのうち、注文管理に関する機能群を実装する。
フレームワーク: FastAPI、DB: PostgreSQL、ORM: SQLAlchemy

## 完了済み機能
1. [x] 注文モデルの定義（Order, OrderItem, OrderStatus）
   - コミット: a1b2c3d "feat: define order models with SQLAlchemy"
2. [x] 注文作成エンドポイント（POST /api/orders）
   - コミット: e4f5g6h "feat: implement order creation endpoint"
3. [x] 注文一覧取得エンドポイント（GET /api/orders）
   - コミット: i7j8k9l "feat: implement order listing with pagination"
4. [x] 注文詳細取得エンドポイント（GET /api/orders/{id}）
   - コミット: m0n1o2p "feat: implement order detail endpoint"
5. [x] 在庫チェックミドルウェア
   - コミット: q3r4s5t "feat: add inventory check middleware"

## 進行中の機能
6. [ ] 注文ステータス更新エンドポイント（PATCH /api/orders/{id}/status）
   - 状態: ステータス遷移のバリデーションロジックまで完了
   - 残り: エンドポイントのテスト作成、エラーハンドリング
   - 変更中ファイル: src/api/orders.py, src/models/order.py

## 未着手の機能
7. [ ] 注文キャンセルエンドポイント
8. [ ] 注文履歴の検索・フィルタリング
9. [ ] 注文の合計金額計算ロジック（税込・割引適用）
10. [ ] 配送先住所のバリデーション
11. [ ] 注文確認メール送信（非同期タスク）
12. [ ] 管理者向け注文管理エンドポイント

## 技術的な決定事項
- ステータス遷移は State Machine パターンで実装する
  （pending → confirmed → shipped → delivered / cancelled）
- ページネーションはカーソルベースを採用（オフセットベースは大量データで性能劣化）
- 在庫チェックは楽観的ロックで実装（悲観的ロックは同時接続時のデッドリスク）

## 既知の問題
- PostgreSQLのコネクションプーリング設定が未最適化（現在デフォルト値）
- テストのフィクスチャが冗長（共通化の余地あり）

## 次のセッションへの引き継ぎ
- 機能6のステータス更新エンドポイントのテストから再開すること
- src/api/orders.py の L.145-180 に未完のバリデーションロジックあり
- テスト実行コマンド: pytest tests/api/test_orders.py -v
```

### 構造化機能リストの設計と運用

進捗ファイルの中核をなすのが「構造化機能リスト」（Structured Feature List）である。この機能リストは、Initializerが作成し、Coding Agentが更新するという分業体制で運用される（BLG-07）。

機能リストの設計において守るべき原則は3つある。

**原則1: 各項目は独立してコミット可能であること**

機能リストの各項目は、それ単体でgitにコミットでき、テストが通る状態であるべきである。これは、セッションが途中で中断されても、中途半端な変更がリポジトリに残らないことを保証する。

**原則2: 各項目の粒度は1セッション内で完了可能であること**

1つの機能が複数セッションにまたがると、セッション間の状態管理がさらに複雑になる。理想的には、各機能は30分から2時間程度で完了できる粒度に分解すべきである。

**原則3: 依存関係を明示すること**

機能間に依存関係がある場合は、その順序を機能リストに明記する。これにより、Coding Agentが誤った順序で実装を進めることを防げる。

```python
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from datetime import datetime


class FeatureStatus(Enum):
    """機能の状態を表す列挙型"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


@dataclass
class Feature:
    """構造化機能リストの1項目"""
    id: int
    title: str
    description: str
    status: FeatureStatus = FeatureStatus.TODO
    commit_hash: Optional[str] = None
    dependencies: list[int] = field(default_factory=list)
    notes: str = ""
    updated_at: Optional[str] = None

    def mark_done(self, commit_hash: str) -> None:
        """機能を完了済みにする"""
        self.status = FeatureStatus.DONE
        self.commit_hash = commit_hash
        self.updated_at = datetime.now().isoformat()

    def mark_in_progress(self, notes: str = "") -> None:
        """機能を進行中にする"""
        self.status = FeatureStatus.IN_PROGRESS
        self.notes = notes
        self.updated_at = datetime.now().isoformat()


@dataclass
class ProgressBridge:
    """進捗ブリッジの全体構造"""
    project_name: str
    features: list[Feature]
    technical_decisions: list[str] = field(default_factory=list)
    known_issues: list[str] = field(default_factory=list)
    session_id: str = ""

    def next_feature(self) -> Optional[Feature]:
        """次に着手すべき機能を返す"""
        # 進行中の機能があればそれを優先
        for f in self.features:
            if f.status == FeatureStatus.IN_PROGRESS:
                return f
        # なければ依存関係が満たされた未着手の機能を返す
        done_ids = {f.id for f in self.features
                    if f.status == FeatureStatus.DONE}
        for f in self.features:
            if f.status == FeatureStatus.TODO:
                if all(dep in done_ids for dep in f.dependencies):
                    return f
        return None

    def completion_ratio(self) -> str:
        """完了率を返す"""
        done = sum(1 for f in self.features
                   if f.status == FeatureStatus.DONE)
        total = len(self.features)
        return f"{done}/{total}"

    def save(self, filepath: str = "claude-progress.json") -> None:
        """進捗をJSONファイルに保存する"""
        data = asdict(self)
        # Enumをシリアライズ可能な形に変換
        for feature in data["features"]:
            feature["status"] = feature["status"].value
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: str = "claude-progress.json") -> "ProgressBridge":
        """JSONファイルから進捗を読み込む"""
        with open(filepath) as f:
            data = json.load(f)
        features = []
        for fd in data["features"]:
            fd["status"] = FeatureStatus(fd["status"])
            features.append(Feature(**fd))
        return cls(
            project_name=data["project_name"],
            features=features,
            technical_decisions=data.get("technical_decisions", []),
            known_issues=data.get("known_issues", []),
            session_id=data.get("session_id", ""),
        )
```

### git履歴によるコンテキスト復元の実装手順

進捗ファイルはセッション間のブリッジとして機能するが、それだけでは不十分なケースがある。たとえば、進捗ファイルの更新を忘れた場合、あるいは進捗ファイルには記録されていない技術的な詳細を復元する必要がある場合である。

このような状況に対するバックアップ手段として、git履歴を活用したコンテキスト復元がある。Coding Agentが各機能の完了時にコミットを行っていれば、git履歴はそれ自体が進捗の記録となる。

```python
import subprocess
from dataclasses import dataclass


@dataclass
class GitContextRestorer:
    """git履歴からコンテキストを復元するユーティリティ"""

    repo_path: str = "."

    def get_recent_commits(self, count: int = 20) -> str:
        """直近のコミット履歴を取得する"""
        result = subprocess.run(
            ["git", "log", f"--oneline", f"-{count}"],
            capture_output=True, text=True,
            cwd=self.repo_path,
        )
        return result.stdout

    def get_changed_files(self, since_commit: str = "HEAD~10") -> str:
        """指定コミット以降に変更されたファイル一覧を取得する"""
        result = subprocess.run(
            ["git", "diff", "--name-status", since_commit, "HEAD"],
            capture_output=True, text=True,
            cwd=self.repo_path,
        )
        return result.stdout

    def get_diff_summary(self, since_commit: str = "HEAD~5") -> str:
        """指定コミット以降の変更の統計情報を取得する"""
        result = subprocess.run(
            ["git", "diff", "--stat", since_commit, "HEAD"],
            capture_output=True, text=True,
            cwd=self.repo_path,
        )
        return result.stdout

    def restore_context(self) -> str:
        """コンテキスト復元用の要約を生成する"""
        commits = self.get_recent_commits()
        changed_files = self.get_changed_files()
        diff_stat = self.get_diff_summary()

        context = f"""## git履歴から復元されたコンテキスト

### 直近のコミット履歴
{commits}

### 変更されたファイル一覧
{changed_files}

### 変更の統計
{diff_stat}
"""
        return context
```

Coding Agentのセッション起動プロトコルは、以下の順序で情報を収集するように設計する。

```python
SESSION_STARTUP_PROTOCOL = """
セッション起動プロトコル（必ずこの順序で実行すること）:

Step 1: 進捗ファイルの読み込み
  → claude-progress.txt（またはclaude-progress.json）を読む
  → 完了済み機能、進行中の機能、未着手の機能を把握する

Step 2: git履歴の確認
  → git log --oneline -20 を実行する
  → 進捗ファイルの内容とgit履歴に矛盾がないか確認する
  → 矛盾がある場合はgit履歴を優先する

Step 3: 現在のコード状態の確認
  → git status を実行する
  → コミットされていない変更がある場合は、その内容を確認する
  → 必要に応じてコミットまたはリバートする

Step 4: テストの実行
  → 既存のテストスイートを実行する
  → 失敗するテストがある場合は、それを最優先で修正する

Step 5: 次のタスクの決定
  → 進行中の機能があればそれを継続する
  → なければ、依存関係が満たされた次の未着手機能に着手する
"""
```

### チェックポインティングとロールバックの実装

進捗ブリッジングの最後の要素は、チェックポインティングとロールバックの仕組みである。これは、Coding Agentが誤った方向に実装を進めてしまった場合の「巻き戻し」を可能にする安全弁である。

gitコミットは自然なチェックポイントとして機能する。各機能の完了時にコミットを行うことで、問題が発生した場合に最後の安全なコミットまでロールバックできる。

```python
from dataclasses import dataclass
import subprocess


@dataclass
class CheckpointManager:
    """チェックポインティングとロールバックを管理する"""

    repo_path: str = "."

    def create_checkpoint(self, feature_id: int, message: str) -> str:
        """機能完了時のチェックポイントを作成する"""
        # ステージングと通常コミット
        subprocess.run(
            ["git", "add", "-A"],
            cwd=self.repo_path,
        )
        result = subprocess.run(
            ["git", "commit", "-m", f"checkpoint(feature-{feature_id}): {message}"],
            capture_output=True, text=True,
            cwd=self.repo_path,
        )
        # コミットハッシュを取得
        hash_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True,
            cwd=self.repo_path,
        )
        return hash_result.stdout.strip()

    def create_tagged_checkpoint(self, tag_name: str) -> None:
        """タグ付きのチェックポイントを作成する（重要な節目用）"""
        subprocess.run(
            ["git", "tag", tag_name],
            cwd=self.repo_path,
        )

    def rollback_to_checkpoint(self, commit_hash: str) -> None:
        """指定チェックポイントまでロールバックする"""
        subprocess.run(
            ["git", "reset", "--hard", commit_hash],
            cwd=self.repo_path,
        )

    def list_checkpoints(self) -> str:
        """チェックポイント（checkpoint プレフィクス付きコミット）一覧を返す"""
        result = subprocess.run(
            ["git", "log", "--oneline", "--grep=checkpoint"],
            capture_output=True, text=True,
            cwd=self.repo_path,
        )
        return result.stdout
```

チェックポインティングの運用における重要な判断は、「いつロールバックすべきか」である。以下の基準が実務的に有用である。

1. **テストの退行**: 以前通過していたテストが失敗するようになった場合
2. **ビルドの失敗**: プロジェクト全体のビルドが通らなくなった場合
3. **方向性の逸脱**: 実装が機能リストの記述から大きく外れている場合
4. **3回以上の同一エラー**: 同じエラーに対して3回以上修正を試みても解決しない場合

これらの基準を自動化することで、Coding Agentは人間の介入なしにロールバック判断を行えるようになる。これは6.7節で解説する自己検証ループと密接に関連するパターンである。

---

## 6.4 コンパクションと推論計算配分の実装

6.1節で述べたコンテキストロットに対する最も直接的な対策が「コンパクション」（Compaction）である。コンパクションとは、長いコンテキストを要約・圧縮し、重要な情報を保持しながらトークン消費量を削減する技術の総称である（ANT-03）。本節では、コンパクションの具体的な実装パターンと、それと密接に関連する推論計算配分の戦略を解説する。

### コンパクションの実装パターン

コンパクションの実装には、大きく分けて3つのアプローチがある。それぞれが異なるトレードオフを持ち、実用的にはこれらを組み合わせて使用する。

**アプローチ1: ツール結果のエビクション（Eviction）**

最も直接的なコンパクション手法は、古いツール実行結果をコンテキストから除去する「エビクション」である。LangChainのDeepAgents v0.2では、大規模なツール結果を自動的にエビクトする仕組みが実装されている（LC-03）。

ツール結果のエビクションの考え方は単純である。ファイル読み込み、ディレクトリリスティング、検索結果など、ツールの出力は往々にして大量のトークンを消費する。しかし、これらの出力は「一時的な参照情報」であり、エージェントが次の行動を決定した後は、その大部分が不要になる。

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ToolResultEvictor:
    """大規模ツール結果のエビクション（除去）を管理する"""

    max_result_tokens: int = 2000
    max_total_tool_tokens: int = 50000
    preserved_count: int = 3  # 直近N回分は保持

    def evict(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """古いツール結果を要約または除去する"""
        tool_results = [
            (i, msg) for i, msg in enumerate(messages)
            if msg.get("role") == "tool"
        ]

        if not tool_results:
            return messages

        # 直近N回分は保持
        evictable = tool_results[:-self.preserved_count]
        result = list(messages)

        for idx, msg in reversed(evictable):
            content = msg.get("content", "")
            token_estimate = len(content) // 4  # 簡易トークン推定

            if token_estimate > self.max_result_tokens:
                # 大規模結果を要約に置換
                result[idx] = {
                    "role": "tool",
                    "tool_call_id": msg.get("tool_call_id"),
                    "content": self._summarize_result(content),
                }

        return result

    def _summarize_result(self, content: str) -> str:
        """ツール結果の要約を生成する（簡易版）"""
        lines = content.strip().split("\n")
        if len(lines) <= 5:
            return content

        # 先頭3行と末尾2行を保持し、中間を省略
        summary_lines = lines[:3] + [
            f"\n... ({len(lines) - 5} lines omitted) ...\n"
        ] + lines[-2:]
        return "\n".join(summary_lines)
```

**アプローチ2: 会話履歴の圧縮**

ツール結果のエビクションが「個別の出力」を対象にするのに対し、会話履歴の圧縮は「会話全体」を対象とする。長期実行エージェントでは、ユーザーとエージェントの間の会話ターンが数十回に達することがある。これらのやり取りの大部分は、最新の作業に直接関連しない過去の文脈である。

会話履歴の圧縮では、LLMを使って過去の会話を要約し、圧縮された形でコンテキストに保持する。

```python
from langchain_core.messages import (
    SystemMessage, HumanMessage, AIMessage
)
from langchain_anthropic import ChatAnthropic


class ConversationCompressor:
    """会話履歴を要約・圧縮する"""

    def __init__(self, model_name: str = "claude-haiku-4-20250514"):
        # 圧縮には軽量・高速なモデルを使用する
        self.summarizer = ChatAnthropic(model=model_name)

    def compress(
        self,
        messages: list,
        keep_recent: int = 6,
    ) -> list:
        """会話履歴を圧縮する

        Args:
            messages: 全メッセージリスト
            keep_recent: 直近で保持するメッセージ数
        """
        if len(messages) <= keep_recent + 2:
            # 圧縮不要（システムプロンプト + 直近メッセージのみ）
            return messages

        system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
        non_system = [m for m in messages if not isinstance(m, SystemMessage)]

        old_messages = non_system[:-keep_recent]
        recent_messages = non_system[-keep_recent:]

        # 古いメッセージを要約
        summary = self._create_summary(old_messages)

        # 要約 + 直近メッセージで再構成
        compressed = system_msgs + [
            HumanMessage(content=f"[以下は過去の会話の要約です]\n{summary}"),
        ] + recent_messages

        return compressed

    def _create_summary(self, messages: list) -> str:
        """メッセージ群を要約する"""
        conversation_text = "\n".join(
            f"{type(m).__name__}: {m.content[:500]}"
            for m in messages
            if hasattr(m, "content") and isinstance(m.content, str)
        )

        summary_prompt = f"""以下の会話履歴を、重要な情報を保持しつつ
簡潔に要約してください。特に以下を必ず含めること:
- 実行したタスクとその結果
- 下された技術的な判断
- 発生したエラーとその対処
- 現在の状態に影響する未解決の問題

会話履歴:
{conversation_text}

要約:"""

        response = self.summarizer.invoke([HumanMessage(content=summary_prompt)])
        return response.content
```

**アプローチ3: 閾値ベースの自動発動**

上記2つのアプローチを「いつ発動するか」という問題を解決するのが、閾値ベースの自動発動メカニズムである。LangChainのDeepAgentsでは、`max_input_tokens`パラメータの85%に達した時点で自動的にコンパクションが発動する仕組みが実装されている（LC-04）。

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class AutoCompactionManager:
    """閾値ベースの自動コンパクション管理"""

    max_input_tokens: int = 200000
    compaction_threshold: float = 0.85  # 85%で発動
    emergency_threshold: float = 0.95  # 95%で緊急圧縮

    def __post_init__(self):
        self.tool_evictor = ToolResultEvictor()
        self.conversation_compressor = ConversationCompressor()

    def check_and_compact(
        self, messages: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """コンテキスト使用率を確認し、必要に応じて圧縮する"""
        current_tokens = self._estimate_tokens(messages)
        usage_ratio = current_tokens / self.max_input_tokens

        if usage_ratio >= self.emergency_threshold:
            # 緊急圧縮: ツールエビクション + 会話圧縮の両方を実行
            messages = self.tool_evictor.evict(messages)
            messages = self.conversation_compressor.compress(
                messages, keep_recent=4
            )
            return messages

        if usage_ratio >= self.compaction_threshold:
            # 通常圧縮: ツールエビクションのみ
            messages = self.tool_evictor.evict(messages)
            return messages

        return messages

    def _estimate_tokens(self, messages: list[dict[str, Any]]) -> int:
        """メッセージリストの総トークン数を推定する"""
        total_chars = sum(
            len(str(msg.get("content", "")))
            for msg in messages
        )
        return total_chars // 4  # 簡易推定: 4文字 ≒ 1トークン
```

この85%ルールの背景には、コンパクション自体にもトークンを消費するという実務上の知見がある。要約生成のためにLLMを呼び出す処理自体がコンテキストウィンドウを圧迫するため、ぎりぎりまで待つのではなく、余裕を持った段階で発動する必要がある（LC-04）。

### Claude Codeのauto-compactパターン

Claude Codeは、コンテキストウィンドウの使用率が95%に達した時点で自動的に要約（auto-compact）を発動する（LC-11）。このパターンは、上述の閾値ベースアプローチの実プロダクト実装例として参考になる。

Claude Codeのauto-compactの特徴は、要約対象を慎重に選別する点にある。システムプロンプト、現在実行中のタスクに直接関連する最新のやり取り、そしてCLAUDE.mdに記載されたプロジェクト固有のルールは圧縮対象から除外される。圧縮されるのは、中間的なツール出力、探索的な会話、すでに反映済みのコード変更履歴など、「意思決定に必要な情報は含むが、詳細は不要」な部分である。

### SQLite+MCPによる常時圧縮パターン

より積極的なアプローチとして、SQLiteとMCPサーバーを組み合わせた常時圧縮パターンがある（TLDV-03）。このパターンでは、コンテキストウィンドウの使用率を常に50%以下に維持することを目標とする。

```
┌──────────────────────────────────────────────────┐
│              エージェント実行環境                      │
│                                                    │
│  ┌─────────────────────────────────────────┐      │
│  │        コンテキストウィンドウ（50%以下維持）  │      │
│  │                                         │      │
│  │  System Prompt + 最新のやり取り            │      │
│  │  + SQLiteからの選択的コンテキスト           │      │
│  │                                         │      │
│  │  ──────── 50%ライン ────────             │      │
│  │                                         │      │
│  │           空き領域                        │      │
│  │                                         │      │
│  └─────────────────────────────────────────┘      │
│            ↕ MCP                                   │
│  ┌─────────────────────────────────────────┐      │
│  │         SQLite データベース                │      │
│  │                                         │      │
│  │  ・全会話履歴（圧縮なし）                   │      │
│  │  ・全ツール実行結果                        │      │
│  │  ・技術的な決定の記録                      │      │
│  │  ・エラーと対処の履歴                      │      │
│  │                                         │      │
│  │  → 必要なときにクエリで取得               │      │
│  └─────────────────────────────────────────┘      │
└──────────────────────────────────────────────────┘
```

[図6.4: SQLite+MCPによる常時圧縮アーキテクチャ]

この手法の核心は、「すべての情報をコンテキストウィンドウに載せる」という従来のアプローチを放棄し、「必要な情報を必要なときにだけ取得する」というオンデマンド方式に切り替えることにある。AIコーディング道場での実践報告によれば、通常は50回のツールコールでコンテキスト上限に達するところを、この手法により500トークン程度に圧縮して劇的にセッション寿命を延長できたという（TLDV-03）。

これは、第2章で解説したコンテキストエンジニアリングの4戦略のうち「Write（外部永続化）」と「Select（必要時取得）」を最も徹底した形で実装したパターンと位置づけられる（LC-11）。IBMの研究チームが提案した「外部実行時メモリ+ポインタ方式」——ツール出力をコンテキスト外に保存し、LLMにはポインタだけを渡す仕組み——とも設計思想を共有する（TLDV-06）。

```python
import sqlite3
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ContextStore:
    """SQLiteベースのコンテキスト永続化ストア"""

    db_path: str = "agent_context.db"

    def __post_init__(self):
        self.conn = sqlite3.connect(self.db_path)
        self._init_tables()

    def _init_tables(self) -> None:
        """テーブルを初期化する"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS tool_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                input_summary TEXT,
                result TEXT NOT NULL,
                token_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                reasoning TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error_type TEXT NOT NULL,
                description TEXT NOT NULL,
                resolution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_tool_results_created
            ON tool_results(created_at DESC);

            CREATE INDEX IF NOT EXISTS idx_tool_results_name
            ON tool_results(tool_name);
        """)
        self.conn.commit()

    def store_tool_result(
        self,
        tool_name: str,
        result: str,
        input_summary: str = "",
        session_id: str = "",
    ) -> int:
        """ツール実行結果を保存し、IDを返す"""
        token_count = len(result) // 4
        cursor = self.conn.execute(
            """INSERT INTO tool_results
               (tool_name, input_summary, result, token_count, session_id)
               VALUES (?, ?, ?, ?, ?)""",
            (tool_name, input_summary, result, token_count, session_id),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_result_pointer(self, result_id: int) -> str:
        """ツール結果のポインタ（要約+ID）を返す"""
        row = self.conn.execute(
            """SELECT tool_name, input_summary, token_count, created_at
               FROM tool_results WHERE id = ?""",
            (result_id,),
        ).fetchone()
        if not row:
            return f"[Result #{result_id}: not found]"
        return (
            f"[Result #{result_id}: {row[0]}({row[1]}) "
            f"- {row[2]} tokens @ {row[3]}]"
        )

    def retrieve_result(self, result_id: int) -> Optional[str]:
        """IDを指定してツール結果の全文を取得する"""
        row = self.conn.execute(
            "SELECT result FROM tool_results WHERE id = ?",
            (result_id,),
        ).fetchone()
        return row[0] if row else None

    def store_decision(
        self,
        category: str,
        description: str,
        reasoning: str = "",
    ) -> None:
        """技術的な決定を記録する"""
        self.conn.execute(
            """INSERT INTO decisions (category, description, reasoning)
               VALUES (?, ?, ?)""",
            (category, description, reasoning),
        )
        self.conn.commit()

    def get_recent_decisions(self, limit: int = 10) -> list[dict]:
        """直近の技術的決定を取得する"""
        rows = self.conn.execute(
            """SELECT category, description, reasoning, created_at
               FROM decisions ORDER BY created_at DESC LIMIT ?""",
            (limit,),
        ).fetchall()
        return [
            {
                "category": r[0],
                "description": r[1],
                "reasoning": r[2],
                "created_at": r[3],
            }
            for r in rows
        ]
```

### 「推論サンドイッチ」パターン

コンパクションとは異なる角度から長期実行エージェントの効率を最適化するのが、「推論サンドイッチ」（Reasoning Sandwich）パターンである（LC-08）。これは、タスクのフェーズごとにLLMの推論コスト（reasoning effort）の配分を変えるアプローチである。

LangChainチームは、Terminal Bench 2.0の実験を通じて、推論コストの配分がエージェントのパフォーマンスに大きな影響を与えることを発見した。直感的には「すべてのフェーズで最大限の推論コストをかければ最良の結果が得られる」と考えがちであるが、データはこの直感が誤りであることを示している。

```
推論サンドイッチパターン:

  ┌────────────────────────────────┐
  │  計画フェーズ                     │  推論レベル: extra-high
  │  ・タスク分析                     │  （高コスト・高精度）
  │  ・アーキテクチャ決定              │
  │  ・実装計画の策定                  │
  ├────────────────────────────────┤
  │  実装フェーズ                     │  推論レベル: high
  │  ・コード生成                     │  （中コスト・効率重視）
  │  ・ファイル編集                   │
  │  ・テスト作成                     │
  ├────────────────────────────────┤
  │  検証フェーズ                     │  推論レベル: extra-high
  │  ・テスト結果の分析               │  （高コスト・高精度）
  │  ・品質チェック                   │
  │  ・完了判定                      │
  └────────────────────────────────┘
```

[図6.5: 推論サンドイッチパターンの構造]

この実験結果は印象的である。すべてのフェーズで最大推論（extra-high）を使用したアプローチは**53.9%**のスコアにとどまったのに対し、フェーズごとにバランスを取った推論サンドイッチでは**63.6%**を達成した（LC-08）。約10ポイントの差は、推論コストの「かけ方」がパフォーマンスに決定的な影響を持つことを意味する。

なぜ最大推論が常に最善ではないのか。その主な理由はタイムアウトである。Terminal Bench 2.0のような時間制限のあるベンチマークでは、すべてのステップで最大推論を使用すると、各ステップの応答時間が長くなり、制限時間内に完了できるツールコールの回数が減少する。結果として、実装やテストに費やせる時間が不足し、タスクの完了率が低下するのである。

推論サンドイッチパターンの実装は、LangGraphのMiddleware機構を活用することで実現できる。

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any


class TaskPhase(Enum):
    """タスクのフェーズ"""
    PLANNING = "planning"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"


# 推論レベルの定義（APIプロバイダのパラメータ名に合わせて調整）
REASONING_LEVELS = {
    TaskPhase.PLANNING: "extra-high",       # 計画は深く考える
    TaskPhase.IMPLEMENTATION: "high",        # 実装は効率重視
    TaskPhase.VERIFICATION: "extra-high",    # 検証は深く考える
}


@dataclass
class ReasoningSandwichMiddleware:
    """推論サンドイッチパターンを実装するMiddleware"""

    current_phase: TaskPhase = TaskPhase.PLANNING

    def detect_phase(self, messages: list[dict[str, Any]]) -> TaskPhase:
        """直近のメッセージからタスクフェーズを推定する"""
        if not messages:
            return TaskPhase.PLANNING

        last_content = str(messages[-1].get("content", "")).lower()

        # 検証フェーズの検出
        verification_signals = [
            "test", "verify", "check", "validate",
            "assert", "review", "confirm",
        ]
        if any(signal in last_content for signal in verification_signals):
            return TaskPhase.VERIFICATION

        # 計画フェーズの検出
        planning_signals = [
            "plan", "design", "architect", "strategy",
            "approach", "consider", "analyze",
        ]
        if any(signal in last_content for signal in planning_signals):
            return TaskPhase.PLANNING

        # デフォルトは実装フェーズ
        return TaskPhase.IMPLEMENTATION

    def modify_request(
        self, messages: list[dict[str, Any]], config: dict[str, Any]
    ) -> dict[str, Any]:
        """リクエストのreasoning effortを調整する"""
        phase = self.detect_phase(messages)
        self.current_phase = phase
        reasoning_level = REASONING_LEVELS[phase]

        config["reasoning_effort"] = reasoning_level
        return config
```

推論サンドイッチの適用にあたっては、フェーズの検出精度が重要となる。上のコード例は簡易的なキーワードベースの検出であるが、実運用ではより精緻な判定ロジックが必要になる場合がある。たとえば、テスト結果の分析中に新たな計画が必要になるケースなど、フェーズが動的に遷移する状況への対応が求められる。

---

## 6.5 マルチエージェント並列実行の実装

### 16並列エージェントによるCコンパイラ構築事例

長期実行エージェントの効率を根本的に向上させるアプローチとして、マルチエージェント並列実行がある。その最も印象的な事例が、AnthropicのNicholas Carlini氏による16並列Claudeインスタンスを使ったCコンパイラの構築である（ANT-12）。

この事例では、16のClaude Opus 4.6インスタンスが並列に動作し、約10万行のRustベースのCコンパイラを構築した。約2,000のエージェントセッションが実行され、APIコストは約20,000ドルであった（ANT-12）。

この事例が示す重要な洞察は、**並列性がエージェント開発の本質的な特性である**ということである。人間のエンジニアが16人で1つのコンパイラを開発する場合、コミュニケーションコスト、コードスタイルの不統一、マージコンフリクトなど、協調のオーバーヘッドが甚大になる。しかし、エージェントの場合は、適切なハーネスを設計すれば、これらのオーバーヘッドを大幅に抑制できる。

### オーケストレーター・ワーカーパターンの実装手順

マルチエージェント並列実行の標準的なアーキテクチャは、「オーケストレーター・ワーカー」（Orchestrator-Worker）パターンである。Anthropicはこのパターンを、エージェント設計の基本デザインパターンの1つとして位置づけている（ANT-02, ANT-06）。

```
┌─────────────────────────────────────────────────┐
│                 Orchestrator                      │
│            （オーケストレーター）                     │
│                                                   │
│  ・タスクの分解と割り当て                             │
│  ・ワーカーの生成と管理                               │
│  ・結果の収集と統合                                   │
│  ・品質チェックと再割り当て                            │
│                                                   │
│       ┌─────┬─────┬─────┬─────┐               │
│       ↓     ↓     ↓     ↓     ↓               │
│    ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐        │
│    │ W-1 ││ W-2 ││ W-3 ││ W-4 ││ W-N │        │
│    │     ││     ││     ││     ││     │        │
│    │Auth ││Cart ││Pay  ││Ship ││...  │        │
│    │機能  ││機能  ││機能  ││機能  ││     │        │
│    └─────┘└─────┘└─────┘└─────┘└─────┘        │
│       ↓     ↓     ↓     ↓     ↓               │
│       └─────┴─────┴─────┴─────┘               │
│                    ↓                              │
│              結果の統合                             │
└─────────────────────────────────────────────────┘
```

[図6.6: オーケストレーター・ワーカーパターンの構造]

以下に、LangGraphを使ったオーケストレーター・ワーカーパターンの実装例を示す。

```python
import asyncio
from dataclasses import dataclass, field
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic


ORCHESTRATOR_PROMPT = """あなたはプロジェクトのオーケストレーターです。
与えられたタスクを独立して並列実行可能なサブタスクに分解してください。

各サブタスクは以下の要件を満たす必要があります:
1. 他のサブタスクと独立して実装可能であること
2. 明確な入力と出力の定義があること
3. 完了条件が客観的に判定可能であること

出力フォーマット:
各サブタスクをJSON配列で出力してください。
[
  {
    "id": "task-1",
    "title": "サブタスクのタイトル",
    "description": "詳細な実装指示",
    "dependencies": [],
    "estimated_complexity": "low|medium|high"
  }
]
"""

WORKER_PROMPT = """あなたは実装ワーカーです。
与えられたサブタスクを正確に実装してください。

制約:
- 指定されたサブタスクのみを実装すること
- 他のサブタスクの領域には手を出さないこと
- 必ずテストを作成すること
- 作業完了後に結果を構造化された形で報告すること
"""


@dataclass
class WorkerResult:
    """ワーカーの実行結果"""
    task_id: str
    success: bool
    files_changed: list[str] = field(default_factory=list)
    tests_passed: int = 0
    tests_failed: int = 0
    error_message: str = ""
    summary: str = ""


@dataclass
class OrchestratorWorkerHarness:
    """オーケストレーター・ワーカーパターンの実装"""

    max_parallel_workers: int = 8
    orchestrator_model: str = "claude-sonnet-4-20250514"
    worker_model: str = "claude-sonnet-4-20250514"

    async def execute(self, task_description: str) -> list[WorkerResult]:
        """タスクを分解し、並列実行する"""

        # Step 1: オーケストレーターがタスクを分解
        subtasks = await self._decompose_task(task_description)

        # Step 2: 依存関係のないタスクを並列実行
        results = []
        pending = list(subtasks)
        completed_ids: set[str] = set()

        while pending:
            # 実行可能なタスクを抽出
            runnable = [
                t for t in pending
                if all(
                    dep in completed_ids
                    for dep in t.get("dependencies", [])
                )
            ]

            if not runnable:
                break  # デッドロック防止

            # 並列数を制限して実行
            batch = runnable[:self.max_parallel_workers]
            batch_results = await asyncio.gather(
                *[self._run_worker(t) for t in batch]
            )

            for result in batch_results:
                results.append(result)
                if result.success:
                    completed_ids.add(result.task_id)

            # 完了したタスクをpendingから除去
            completed_task_ids = {r.task_id for r in batch_results}
            pending = [
                t for t in pending
                if t["id"] not in completed_task_ids
            ]

        # Step 3: 結果の統合と検証
        await self._integrate_results(results)

        return results

    async def _decompose_task(
        self, task_description: str
    ) -> list[dict[str, Any]]:
        """オーケストレーターがタスクをサブタスクに分解する"""
        model = ChatAnthropic(model=self.orchestrator_model)
        response = await model.ainvoke([
            SystemMessage(content=ORCHESTRATOR_PROMPT),
            HumanMessage(content=task_description),
        ])
        # 応答からJSON部分を抽出・パース
        import json
        content = response.content
        start = content.find("[")
        end = content.rfind("]") + 1
        return json.loads(content[start:end])

    async def _run_worker(
        self, subtask: dict[str, Any]
    ) -> WorkerResult:
        """ワーカーエージェントを実行する"""
        model = ChatAnthropic(model=self.worker_model)
        try:
            response = await model.ainvoke([
                SystemMessage(content=WORKER_PROMPT),
                HumanMessage(
                    content=f"サブタスク: {subtask['title']}\n"
                    f"詳細: {subtask['description']}"
                ),
            ])
            return WorkerResult(
                task_id=subtask["id"],
                success=True,
                summary=response.content[:500],
            )
        except Exception as e:
            return WorkerResult(
                task_id=subtask["id"],
                success=False,
                error_message=str(e),
            )

    async def _integrate_results(
        self, results: list[WorkerResult]
    ) -> None:
        """ワーカーの結果を統合する"""
        successful = [r for r in results if r.success]
        failed = [r for r in results if not r.success]

        if failed:
            # 失敗したタスクのリトライまたはエスカレーション
            for result in failed:
                print(
                    f"FAILED: {result.task_id} - "
                    f"{result.error_message}"
                )
```

### サブエージェントのコンテキスト分離戦略

マルチエージェント並列実行において最も重要な設計判断は、各ワーカー（サブエージェント）のコンテキストをどう分離するかである。これは、第2章で解説したコンテキストエンジニアリングの「Isolate（分離）」戦略の核心的な応用である（LC-11）。

LangChainのDeep Agentsフレームワークでは、サブエージェントを「コンテキスト肥大化対策としての作業委譲」の手段と位置づけている（LC-09）。各サブエージェントは、独自のコンテキストウィンドウを持ち、親エージェント（オーケストレーター）のコンテキストを汚染しない。サブエージェントの実行結果は、要約された形で親エージェントに返される。

```python
from dataclasses import dataclass
from typing import Any


@dataclass
class ContextIsolationStrategy:
    """サブエージェントのコンテキスト分離戦略"""

    max_result_tokens: int = 1000  # 親に返す結果の最大トークン数

    def create_isolated_context(
        self,
        subtask: dict[str, Any],
        shared_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """サブエージェント用の分離されたコンテキストを構築する

        サブエージェントには以下のみを渡す:
        1. サブタスク固有のシステムプロンプト
        2. サブタスクの詳細な指示
        3. 共有コンテキスト（プロジェクト規約、API仕様など）の関連部分のみ
        """
        messages = [
            {
                "role": "system",
                "content": self._build_worker_prompt(
                    subtask, shared_context
                ),
            },
            {
                "role": "user",
                "content": subtask["description"],
            },
        ]
        return messages

    def summarize_result(self, worker_output: str) -> str:
        """ワーカーの出力を要約して親エージェントに返す

        完全な出力ではなく、構造化された要約のみを返すことで、
        親エージェントのコンテキスト肥大化を防ぐ。
        """
        if len(worker_output) // 4 <= self.max_result_tokens:
            return worker_output

        # 長い出力は構造化された要約に変換
        lines = worker_output.split("\n")
        summary_parts = []
        summary_parts.append("## ワーカー実行結果（要約）")

        # 重要な行（コミット、テスト結果、エラー）を抽出
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in [
                "commit", "test", "error", "success",
                "fail", "created", "modified",
            ]):
                summary_parts.append(f"- {line.strip()}")

        return "\n".join(summary_parts[:20])  # 最大20行

    def _build_worker_prompt(
        self,
        subtask: dict[str, Any],
        shared_context: dict[str, Any],
    ) -> str:
        """ワーカー用のシステムプロンプトを構築する"""
        return f"""あなたは以下のサブタスクを担当するワーカーです。

## サブタスク
タイトル: {subtask['title']}
ID: {subtask['id']}

## プロジェクト規約
{shared_context.get('coding_standards', 'N/A')}

## 使用技術
{shared_context.get('tech_stack', 'N/A')}

## 制約
- このサブタスクの範囲のみを実装すること
- 他のサブタスクの領域に影響する変更を行わないこと
- 作業完了後、変更したファイルの一覧とテスト結果を報告すること
"""
```

コンテキスト分離の効果は、単にコンテキストウィンドウの容量問題を解決するだけに留まらない。各ワーカーが独立したコンテキストで動作することで、1つのワーカーの失敗が他のワーカーに伝播しない。これは、6.1節で議論したコンテキストロットの問題に対する構造的な解決策でもある。あるワーカーのコンテキストが劣化しても、他のワーカーのコンテキストは影響を受けない。

---

## 6.6 3段階エージェント構造パターン

### Open SWE: Manager→Planner→Programmer & Reviewer

6.2節で解説した2エージェントアーキテクチャ、6.5節で解説したオーケストレーター・ワーカーパターンを統合・発展させた形として、LangChainのOpen SWEが採用する3段階エージェント構造がある（LC-17）。

Open SWEは、クラウド上で非同期に動作するオープンソースのコーディングエージェントであり、長時間実行される自律的なソフトウェア開発タスクを想定して設計されている。そのアーキテクチャは、3つの明確に分離された段階で構成される。

```
┌────────────────────────────────────────────────────┐
│               3段階エージェント構造                     │
│                                                      │
│  ┌──────────────────────────────────────────┐       │
│  │  Stage 1: Manager（マネージャー）            │       │
│  │                                          │       │
│  │  ・ユーザーインタラクションの処理              │       │
│  │  ・タスクの受付と要件の確認                   │       │
│  │  ・GitHubイシューからの作業委譲               │       │
│  │  ・Plannerへの作業指示                      │       │
│  └──────────────┬───────────────────────────┘       │
│                 ↓                                    │
│  ┌──────────────────────────────────────────┐       │
│  │  Stage 2: Planner（プランナー）              │       │
│  │                                          │       │
│  │  ・コードベースの分析                       │       │
│  │  ・詳細な実装計画の作成                      │       │
│  │  ・Human-in-the-Loop: 承認/編集/変更依頼     │       │
│  │  ・計画確定後、Programmerへの指示             │       │
│  └──────────────┬───────────────────────────┘       │
│                 ↓                                    │
│  ┌──────────────────────────────────────────┐       │
│  │  Stage 3: Programmer & Reviewer            │       │
│  │           （プログラマー＆レビュアー）          │       │
│  │                                          │       │
│  │  ・サンドボックスでのコード実装               │       │
│  │  ・テストの作成と実行                       │       │
│  │  ・自己レビューとQA検証                     │       │
│  │  ・PRの作成                               │       │
│  └──────────────────────────────────────────┘       │
└────────────────────────────────────────────────────┘
```

[図6.7: Open SWEの3段階エージェント構造]

### 各段階の責務分離と長期実行への適用

3段階構造の各段階は、明確に異なる責務を担い、それぞれが長期実行の課題に対する特定の解決策を提供する。

**Stage 1: Manager（マネージャー）**

Managerは、ユーザーとの界面を担当するエージェントである。GitHubイシューやカスタムUIを通じてタスクを受け付け、要件を確認し、Plannerに作業を委譲する。Managerの特徴は、タスクの「全体像」を把握していることである。長期実行プロジェクトにおいて、ManagerはPlannerやProgrammerが作業に没頭して全体方向を見失うことを防ぐ「錨」の役割を果たす。

```python
MANAGER_PROMPT = """あなたはプロジェクトマネージャーです。
ユーザーからのリクエストを受け付け、以下を行います:

1. リクエストの要件を明確化する
   - 曖昧な点があればユーザーに質問する
   - スコープを明確に定義する
   - 受入条件を確認する

2. Plannerに作業を委譲する
   - 要件の要約
   - 技術的な制約
   - 優先順位

3. Plannerの計画をレビューする
   - 計画が要件を満たしているか確認
   - 不足がある場合はフィードバック

あなたはコードを書きません。
あなたの価値は「正しい方向を指し示す」ことにあります。
"""
```

**Stage 2: Planner（プランナー）**

Plannerは、Managerから受け取った要件を詳細な実装計画に変換するエージェントである。コードベースを分析し、変更が必要なファイル、実装の順序、テスト戦略を策定する。

Plannerの設計における重要な特徴は、**Human-in-the-Loop（人間の介入）が計画段階で統合されている**点である（LC-17）。Plannerが作成した計画は、自動的に実行に移されるのではなく、人間のレビューを経て承認される。人間は計画を承認するか、編集するか、変更を要求することができる。

```python
PLANNER_PROMPT = """あなたは実装プランナーです。
与えられた要件に対し、詳細な実装計画を作成してください。

計画には以下を含めること:
1. 変更対象ファイルの一覧と変更内容の概要
2. 実装の順序（依存関係を考慮）
3. 各ステップの推定所要時間
4. テスト戦略（ユニットテスト、統合テスト）
5. リスクと軽減策

出力フォーマット:
## 実装計画

### 概要
[計画の概要を1-2文で]

### ステップ
1. [ステップ1の説明]
   - 対象ファイル: xxx
   - 変更内容: xxx
   - テスト: xxx

2. [ステップ2の説明]
   ...

### リスク
- [リスク1]: [軽減策]
- [リスク2]: [軽減策]

重要: あなたはコードを書きません。計画のみを作成します。
計画は人間のレビューを経て承認された後、Programmerに渡されます。
"""
```

**Stage 3: Programmer & Reviewer（プログラマー＆レビュアー）**

Programmerは、承認された計画に基づいてコードを実装するエージェントである。Daytona等のサンドボックス環境内で動作し、コード変更、テスト実行、自己レビューを行い、最終的にPull Requestを作成する。

Programmerには「Reviewer」の役割も統合されている点が特徴的である。実装が完了した後、Programmerは自身の変更をレビューし、品質基準を満たしているかを確認する。これは、6.7節で詳述する自己検証ループの一形態である。

### Human-in-the-Loopの計画段階での統合

3段階エージェント構造における最も重要な設計判断は、Human-in-the-Loopを**計画段階（Stage 2）**に配置していることである。この判断には、以下の3つの根拠がある。

**根拠1: コスト効率**

計画段階で方向性の誤りを検出・修正することは、実装後に修正するよりも遥かに低コストである。Programmerが数時間かけて実装した後に「方針が違った」と判明すれば、その時間とトークンは無駄になる。計画段階でのレビューは、この種の浪費を未然に防ぐ。

**根拠2: コンテキストの最適化**

Programmerに渡されるコンテキストは、承認済みの計画という「洗練された情報」である。ユーザーとの間で交わされた要件確認のやり取り、複数の代替案の検討過程など、実装に不要な情報はPlannerの段階でフィルタリングされる。これは、コンテキストロット対策としても有効である。

**根拠3: 責任範囲の明確化**

Human-in-the-Loopが計画段階に限定されることで、人間の責任範囲が明確になる。人間は「何を作るか」の最終判断を行い、「どう作るか」はProgrammerに委ねる。この分業は、第8章で議論する「Humans Steer, Agents Execute」の原則（OAI-01）の具体的な実装でもある。

```python
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class PlanReviewResult(Enum):
    """計画レビューの結果"""
    APPROVED = "approved"
    EDITED = "edited"
    REJECTED = "rejected"


@dataclass
class HumanInTheLoopGate:
    """計画段階でのHuman-in-the-Loop制御"""

    auto_approve_threshold: Optional[float] = None

    async def review_plan(
        self,
        plan: str,
        confidence_score: float = 0.0,
    ) -> tuple[PlanReviewResult, str]:
        """計画を人間にレビューさせる

        auto_approve_thresholdが設定されている場合、
        信頼度スコアがそれを超えていれば自動承認する。
        """
        if (
            self.auto_approve_threshold is not None
            and confidence_score >= self.auto_approve_threshold
        ):
            return PlanReviewResult.APPROVED, plan

        # 人間にレビューを要求
        print("=" * 60)
        print("実装計画のレビューが必要です")
        print("=" * 60)
        print(plan)
        print("=" * 60)

        response = input(
            "\n[A]承認 / [E]編集 / [R]却下: "
        ).strip().upper()

        if response == "A":
            return PlanReviewResult.APPROVED, plan
        elif response == "E":
            edited_plan = input("修正した計画を入力してください:\n")
            return PlanReviewResult.EDITED, edited_plan
        else:
            reason = input("却下理由: ")
            return PlanReviewResult.REJECTED, reason
```

3段階エージェント構造は、長期実行エージェントにおいて特に強力な効果を発揮する。タスクが大規模になるほど、計画の品質がプロジェクト全体の成否を左右する。人間が計画段階で介入することで、長期実行中のエージェントが方向性を見失うリスクを構造的に排除できるのである。

---

## 6.7 自己検証ループの実装

長期実行エージェントの信頼性を確保するうえで、自己検証ループ（Self-Verification Loop）は不可欠な仕組みである。自己検証ループとは、エージェントがタスクの「完了」を宣言する前に、自身の成果物を検証するプロセスを強制的に挟む設計パターンである。

### PreCompletionChecklistMiddleware

LangChainチームがTerminal Bench 2.0で実証した最も効果的な改善の1つが、`PreCompletionChecklistMiddleware`である（LC-08）。このMiddlewareは、エージェントがタスクの完了を報告しようとする際に、事前に定義された検証チェックリストの実行を強制する。

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PreCompletionChecklistMiddleware:
    """タスク完了前に検証パスを強制するMiddleware

    エージェントが「完了」を宣言する前に、以下の検証を強制する:
    1. すべてのテストが通過しているか
    2. ハッピーパスとエッジケースの両方がテストされているか
    3. コードがビルド可能か
    4. 変更がgitにコミットされているか
    """

    checklist_items: list[str] = field(default_factory=lambda: [
        "すべての既存テストが通過する",
        "新規機能に対するテストが作成されている",
        "エッジケース（空入力、境界値、エラーケース）がテストされている",
        "コードがビルドエラーなくコンパイルされる",
        "変更がgitにコミットされている",
        "進捗ファイルが最新に更新されている",
    ])

    def modify_request(
        self,
        messages: list[dict[str, Any]],
        config: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """完了報告の前にチェックリストの実行を注入する"""
        if not messages:
            return messages, config

        last_msg = messages[-1]
        content = str(last_msg.get("content", "")).lower()

        # 完了を示すシグナルを検出
        completion_signals = [
            "完了", "done", "finished", "complete",
            "implemented", "実装しました", "終わりました",
        ]

        if any(signal in content for signal in completion_signals):
            checklist_prompt = self._build_checklist_prompt()
            messages = messages + [{
                "role": "user",
                "content": checklist_prompt,
            }]

        return messages, config

    def _build_checklist_prompt(self) -> str:
        """検証チェックリストのプロンプトを構築する"""
        items = "\n".join(
            f"  {i+1}. [ ] {item}"
            for i, item in enumerate(self.checklist_items)
        )
        return f"""タスクの完了を報告する前に、以下のチェックリストを
すべて確認してください。各項目を実際に検証し、
結果を報告してください。

## 完了前チェックリスト
{items}

すべての項目が確認できるまで、タスクは完了とみなしません。
未確認の項目がある場合は、その項目の検証を実行してください。
"""
```

### ハッピーパスとエッジケースの両方をテストで確認

自己検証ループの要は、テストの網羅性にある。LangChainチームの実験では、エージェントにハッピーパス（正常系）のテストだけでなく、エッジケース（異常系・境界値）のテストも明示的に要求することで、タスクの成功率が有意に向上した（LC-08）。

```python
TEST_VERIFICATION_PROMPT = """実装した機能に対して、
以下の3カテゴリのテストを作成・実行してください。

## 1. ハッピーパス（正常系）テスト
- 典型的な入力に対して期待通りの出力が得られることを確認
- 主要なユースケースをカバー

## 2. エッジケーステスト
- 空の入力、None、空文字列
- 境界値（最大値、最小値、ゼロ）
- 非常に大きな入力データ
- 特殊文字を含む入力

## 3. エラーハンドリングテスト
- 不正な入力に対して適切なエラーが返されることを確認
- 外部依存（DB、API）の障害時の振る舞い

テスト実行後、結果を以下のフォーマットで報告してください:

### テスト結果
- ハッピーパス: X/Y 通過
- エッジケース: X/Y 通過
- エラーハンドリング: X/Y 通過
- 全体: X/Y 通過
"""
```

以下は、エージェントがテスト検証を自動的に実行するためのユーティリティ実装である。

```python
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class TestVerifier:
    """テスト実行と結果検証のユーティリティ"""

    project_path: str = "."
    test_command: str = "pytest"

    def run_tests(
        self, test_path: Optional[str] = None
    ) -> dict[str, Any]:
        """テストを実行し、結果を構造化して返す"""
        cmd = [self.test_command, "-v", "--tb=short"]
        if test_path:
            cmd.append(test_path)

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.project_path,
            timeout=120,  # 2分のタイムアウト
        )

        return {
            "exit_code": result.returncode,
            "passed": result.returncode == 0,
            "stdout": result.stdout[-2000:],  # 末尾2000文字
            "stderr": result.stderr[-1000:],  # 末尾1000文字
            "summary": self._extract_summary(result.stdout),
        }

    def verify_no_regression(
        self, baseline_test_path: Optional[str] = None
    ) -> dict[str, Any]:
        """既存テストの退行がないことを確認する"""
        result = self.run_tests(baseline_test_path)
        if not result["passed"]:
            result["regression_detected"] = True
            result["action_required"] = (
                "既存テストの退行が検出されました。"
                "新規変更をロールバックするか、"
                "退行の原因を修正してください。"
            )
        else:
            result["regression_detected"] = False
        return result

    def _extract_summary(self, stdout: str) -> str:
        """テスト出力からサマリー行を抽出する"""
        lines = stdout.strip().split("\n")
        # pytestのサマリー行を探す
        for line in reversed(lines):
            if "passed" in line or "failed" in line or "error" in line:
                return line.strip()
        return "サマリーを抽出できませんでした"
```

### トレーシングベースのフィードバックループ

自己検証ループの第3の柱が、トレーシングベースのフィードバックである（LC-08）。これは、エージェントの実行トレース（各ステップの入力、出力、所要時間、トークン消費量）を記録・分析し、その結果をハーネスの改善にフィードバックするプロセスである。

LangChainチームは、Terminal Bench 2.0の実験において、エージェントの実行トレースを分析することで、繰り返し発生する失敗パターンを特定した。たとえば、「エージェントがディレクトリ構造の把握に過度の時間を費やしている」というパターンが発見された場合、`LocalContextMiddleware`を追加してディレクトリ構造を事前にマッピングするという改善を行った。

```python
import time
import json
from dataclasses import dataclass, field
from typing import Any, Optional
from datetime import datetime


@dataclass
class TraceEntry:
    """トレースの1エントリ"""
    step_id: int
    timestamp: str
    action_type: str  # "tool_call", "llm_call", "checkpoint"
    tool_name: Optional[str] = None
    input_tokens: int = 0
    output_tokens: int = 0
    duration_ms: int = 0
    success: bool = True
    error: Optional[str] = None


@dataclass
class ExecutionTracer:
    """エージェント実行のトレーシング"""

    session_id: str = ""
    traces: list[TraceEntry] = field(default_factory=list)
    _step_counter: int = 0

    def trace_step(
        self,
        action_type: str,
        tool_name: Optional[str] = None,
    ):
        """ステップのトレースを開始するコンテキストマネージャー"""
        return _TraceContext(self, action_type, tool_name)

    def add_entry(self, entry: TraceEntry) -> None:
        """トレースエントリを追加する"""
        self.traces.append(entry)

    def analyze_patterns(self) -> dict[str, Any]:
        """実行パターンを分析する"""
        total_tokens = sum(
            t.input_tokens + t.output_tokens for t in self.traces
        )
        total_duration = sum(t.duration_ms for t in self.traces)
        failures = [t for t in self.traces if not t.success]

        # ツール使用頻度の分析
        tool_usage: dict[str, int] = {}
        for t in self.traces:
            if t.tool_name:
                tool_usage[t.tool_name] = (
                    tool_usage.get(t.tool_name, 0) + 1
                )

        # 繰り返しパターンの検出
        repeated_failures = self._detect_repeated_failures()

        return {
            "total_steps": len(self.traces),
            "total_tokens": total_tokens,
            "total_duration_ms": total_duration,
            "failure_count": len(failures),
            "failure_rate": (
                len(failures) / len(self.traces)
                if self.traces else 0
            ),
            "tool_usage": tool_usage,
            "repeated_failures": repeated_failures,
        }

    def _detect_repeated_failures(self) -> list[dict[str, Any]]:
        """繰り返しの失敗パターンを検出する"""
        failure_patterns: dict[str, int] = {}
        for t in self.traces:
            if not t.success and t.error:
                key = f"{t.tool_name}:{t.error[:100]}"
                failure_patterns[key] = (
                    failure_patterns.get(key, 0) + 1
                )

        return [
            {"pattern": k, "count": v}
            for k, v in failure_patterns.items()
            if v >= 2  # 2回以上の繰り返しを報告
        ]

    def export(self, filepath: str) -> None:
        """トレースをJSONファイルにエクスポートする"""
        data = {
            "session_id": self.session_id,
            "traces": [
                {
                    "step_id": t.step_id,
                    "timestamp": t.timestamp,
                    "action_type": t.action_type,
                    "tool_name": t.tool_name,
                    "input_tokens": t.input_tokens,
                    "output_tokens": t.output_tokens,
                    "duration_ms": t.duration_ms,
                    "success": t.success,
                    "error": t.error,
                }
                for t in self.traces
            ],
            "analysis": self.analyze_patterns(),
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


class _TraceContext:
    """トレーシング用のコンテキストマネージャー"""

    def __init__(
        self,
        tracer: ExecutionTracer,
        action_type: str,
        tool_name: Optional[str],
    ):
        self.tracer = tracer
        self.action_type = action_type
        self.tool_name = tool_name
        self.start_time: float = 0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration_ms = int((time.time() - self.start_time) * 1000)
        self.tracer._step_counter += 1
        entry = TraceEntry(
            step_id=self.tracer._step_counter,
            timestamp=datetime.now().isoformat(),
            action_type=self.action_type,
            tool_name=self.tool_name,
            duration_ms=duration_ms,
            success=exc_type is None,
            error=str(exc_val) if exc_val else None,
        )
        self.tracer.add_entry(entry)
        return False  # 例外を再送出
```

トレーシングベースのフィードバックの本質は、「1回の実行結果を改善するのではなく、ハーネス自体を反復的に改善する」という点にある。個別のタスクの成否ではなく、タスク群にわたって共通する失敗パターンを特定し、ハーネスのMiddlewareやプロンプトを改善する。これは、第1章で紹介した「build → test → ship → observe → refine」サイクル（LC-13）の具体的な実装である。

---

## 6.8 5つの失敗パターンと対策

長期実行エージェントが直面する失敗パターンは、実務においておおむね5つに分類される。これらのパターンを事前に理解し、それぞれに対する対策をハーネスに組み込むことで、長期実行の信頼性を大幅に向上させることができる。

### パターン1: コンテキスト消失

**症状**: エージェントが過去のセッションで実装した内容を「忘れ」、同じ作業を繰り返す。あるいは、前のセッションで下した技術的な決定と矛盾する実装を行う。

**原因**: 6.1節で述べたセッション間の状態消失。新しいセッションが開始されるたびに、コンテキストがリセットされる。

**対策: 進捗ブリッジング（6.3節）**

```
┌─────────────┐    claude-progress.txt    ┌─────────────┐
│ Session N   │ ─────────────────────────→│ Session N+1 │
│             │    + git history          │             │
│ 機能A完了    │    + チェックポイント        │ 機能Bから再開 │
└─────────────┘                           └─────────────┘
```

進捗ファイルとgit履歴の二重の保証により、コンテキストの消失を防ぐ。さらに、セッション起動プロトコル（6.3節）を定義し、新しいセッションが必ず進捗ファイルの読み込みから開始するようにする。

### パターン2: 方向性の逸脱

**症状**: エージェントがタスクの本来の目的から逸脱し、関連性の低い作業に没頭する。たとえば、簡単なバグ修正を依頼されたのに、大規模なリファクタリングを始めてしまう。

**原因**: コンテキストロットの進行により、セッション冒頭で与えられたタスク目標の影響力が低下する。また、エージェントが「より良い」解決策を見つけたと判断し、元のスコープを超えた作業に着手する傾向。

**対策: ポリシーファイルとガードレール**

ポリシーファイル（`AGENTS.md`、`CLAUDE.md`）にタスクのスコープ制約を明記し、エージェントの行動範囲を限定する。第4章で解説したガードレール設計の手法がここで直接適用される。

```markdown
# CLAUDE.md の方向性ガードレール例

## スコープ制約
- 依頼されたタスクのスコープ外の変更を行わないこと
- リファクタリングが必要と判断した場合は、実行せずに報告すること
- 新しい依存関係の追加は事前に承認を得ること

## 判断の記録義務
- 技術的な判断を行った場合は、その理由を進捗ファイルに記録すること
- スコープの解釈に迷った場合は、保守的に（狭く）解釈すること
```

### パターン3: 無限ループ

**症状**: エージェントが同じエラーに対して同じアプローチを繰り返し試行し、進捗しない。API呼び出しとトークンの消費だけが増大する。

**原因**: 時間盲目性（6.1節）により、エージェントは「すでにN回同じことを試した」という認識を持てない。また、コンテキストロットにより、過去の試行の記録がコンテキストから「見えなく」なっている場合もある。

**対策: 停止条件とコスト予算**

```python
from dataclasses import dataclass


@dataclass
class ExecutionBudget:
    """実行予算の管理"""

    max_iterations: int = 100
    max_tokens: int = 1_000_000
    max_duration_seconds: int = 3600  # 1時間
    max_cost_dollars: float = 10.0

    # 現在の消費量
    current_iterations: int = 0
    current_tokens: int = 0
    current_duration: float = 0
    current_cost: float = 0

    def check_budget(self) -> tuple[bool, str]:
        """予算内かどうかを確認する

        Returns:
            (予算内かどうか, 超過した場合の理由)
        """
        if self.current_iterations >= self.max_iterations:
            return False, (
                f"最大反復回数 ({self.max_iterations}) に到達しました"
            )
        if self.current_tokens >= self.max_tokens:
            return False, (
                f"最大トークン数 ({self.max_tokens:,}) に到達しました"
            )
        if self.current_duration >= self.max_duration_seconds:
            return False, (
                f"最大実行時間 ({self.max_duration_seconds}秒) "
                f"に到達しました"
            )
        if self.current_cost >= self.max_cost_dollars:
            return False, (
                f"最大コスト (${self.max_cost_dollars:.2f}) "
                f"に到達しました"
            )
        return True, ""

    def remaining_summary(self) -> str:
        """残予算のサマリーを返す"""
        return (
            f"残予算: "
            f"反復 {self.max_iterations - self.current_iterations}回, "
            f"トークン {self.max_tokens - self.current_tokens:,}, "
            f"時間 {self.max_duration_seconds - self.current_duration:.0f}秒, "
            f"コスト ${self.max_cost_dollars - self.current_cost:.2f}"
        )
```

### パターン4: 品質劣化

**症状**: 長時間の実行が進むにつれて、生成されるコードの品質が徐々に低下する。変数名が雑になる、テストが省略される、エラーハンドリングが不十分になるなどの兆候が現れる。

**原因**: コンテキストロットの進行と、コンテキストウィンドウの圧迫によるモデルの注意力低下。セッション冒頭で指示されたコーディング規約やスタイルガイドが、大量の中間結果に埋もれてしまう。

**対策: 継続的評価と自動リファクタリング**

品質劣化への対策は、2つの方向から行う。第一に、コンパクション（6.4節）によりコンテキストロットの進行を抑制する。第二に、定期的な品質チェックポイントを設けて劣化を早期に検出する。

```python
from dataclasses import dataclass


@dataclass
class QualityGateMiddleware:
    """定期的な品質チェックを強制するMiddleware"""

    check_interval: int = 5  # N機能ごとにチェック
    features_since_last_check: int = 0

    def should_check(self) -> bool:
        """品質チェックが必要かどうか"""
        self.features_since_last_check += 1
        if self.features_since_last_check >= self.check_interval:
            self.features_since_last_check = 0
            return True
        return False

    def quality_check_prompt(self) -> str:
        """品質チェックのプロンプトを返す"""
        return """## 定期品質チェック

以下の観点で、直近の実装を確認してください:

1. **コーディング規約の準拠**
   - 命名規則は一貫しているか
   - コメントは適切に記述されているか
   - インデントとフォーマットは統一されているか

2. **テストの品質**
   - テストカバレッジは十分か
   - テスト名は意図を表現しているか
   - アサーションは具体的か

3. **エラーハンドリング**
   - 想定されるエラーケースに対処しているか
   - エラーメッセージは有用か
   - リソースの後始末は適切か

4. **アーキテクチャの一貫性**
   - 新しいコードが既存のアーキテクチャパターンに従っているか
   - 不必要な複雑性が導入されていないか

問題がある場合は、この場で修正してください。
"""
```

### パターン5: 破滅ループ（Doom Loop）

**症状**: エージェントが同一ファイルに対して何度も編集を繰り返し、変更と巻き戻しのサイクルに陥る。1つのバグを修正すると別のバグが発生し、それを修正するとまた元のバグが再発する——という悪循環。

**原因**: 根本的なアーキテクチャ上の問題に対して、表面的なパッチを繰り返し適用しようとする。エージェントが「アプローチ自体を変更する」という判断に至れない。

**対策: LoopDetectionMiddleware**

LangChainチームが実装した`LoopDetectionMiddleware`は、同一ファイルに対するN回以上の編集を検出し、エージェントにアプローチの再考を促すコンテキストを注入する（LC-08）。

```python
from dataclasses import dataclass, field
from typing import Any
from collections import Counter


@dataclass
class LoopDetectionMiddleware:
    """破滅ループを検出し、アプローチ変更を促すMiddleware

    同一ファイルへの繰り返し編集を追跡し、
    閾値を超えた場合にアプローチの再考を促す。
    """

    max_edits_per_file: int = 3
    file_edit_counts: Counter = field(
        default_factory=Counter
    )
    warning_injected: bool = False

    def track_edit(self, filepath: str) -> None:
        """ファイル編集を記録する"""
        self.file_edit_counts[filepath] += 1

    def check_for_loops(self) -> list[str]:
        """ループの兆候があるファイルを返す"""
        return [
            filepath
            for filepath, count in self.file_edit_counts.items()
            if count >= self.max_edits_per_file
        ]

    def modify_request(
        self,
        messages: list[dict[str, Any]],
        config: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """ループ検出時にコンテキストを注入する"""
        # 直近のメッセージからファイル編集を検出
        last_content = str(
            messages[-1].get("content", "")
        ) if messages else ""

        # ファイルパスのパターンを検出（簡易実装）
        import re
        file_patterns = re.findall(
            r'(?:editing|modifying|changing|wrote)\s+(\S+\.\w+)',
            last_content, re.IGNORECASE
        )
        for fp in file_patterns:
            self.track_edit(fp)

        # ループ検出
        looping_files = self.check_for_loops()
        if looping_files and not self.warning_injected:
            self.warning_injected = True
            warning = self._build_warning(looping_files)
            messages = messages + [{
                "role": "user",
                "content": warning,
            }]

        return messages, config

    def _build_warning(self, files: list[str]) -> str:
        """ループ検出の警告メッセージを構築する"""
        file_list = "\n".join(
            f"  - {f}: {self.file_edit_counts[f]}回編集"
            for f in files
        )
        return f"""⚠ ループ検出の警告

以下のファイルに対して繰り返しの編集が検出されました:
{file_list}

同じファイルを繰り返し編集していることは、
現在のアプローチに根本的な問題がある可能性を示唆しています。

以下の対応を検討してください:
1. 現在のアプローチの前提を見直す
2. 問題をより小さな部分に分解する
3. 異なるアルゴリズムや設計パターンを検討する
4. 直近のチェックポイントまでロールバックし、
   別のアプローチで再実装する

...consider reconsidering your approach...
"""
```

### 5つの失敗パターンの相互関係

これら5つの失敗パターンは独立した問題ではなく、しばしば連鎖する。コンテキスト消失（パターン1）が方向性の逸脱（パターン2）を引き起こし、逸脱した方向での実装が品質劣化（パターン4）につながり、低品質なコードの修正が破滅ループ（パターン5）を誘発する——という連鎖が典型的である。

```
パターン1            パターン2           パターン4          パターン5
コンテキスト消失 ──→ 方向性の逸脱 ──→ 品質劣化 ──→ 破滅ループ
                                                    ↑
                    パターン3 ─────────────────────┘
                    無限ループ

対策の対応関係:
  進捗ブリッジング ──→ ポリシー/ガードレール ──→ 品質ゲート ──→ LoopDetection
   (6.3節)              (第4章)              (6.7節)        (本節)
             停止条件/コスト予算 ────────────────────────────┘
                  (本節)
```

[図6.8: 5つの失敗パターンの連鎖と対策の対応関係]

効果的なハーネス設計とは、これらの対策を個別に実装するのではなく、Middlewareパイプラインとして統合的に組み上げることである。各Middlewareが特定の失敗パターンを担当し、エージェントの実行フローの中で自動的に発動する。

```python
from dataclasses import dataclass


@dataclass
class LongRunningAgentHarness:
    """長期実行エージェント用の統合ハーネス

    5つの失敗パターンに対する対策を
    Middlewareパイプラインとして統合する。
    """

    def __post_init__(self):
        # 各失敗パターンに対応するMiddleware
        self.loop_detector = LoopDetectionMiddleware(
            max_edits_per_file=3
        )
        self.pre_completion = PreCompletionChecklistMiddleware()
        self.quality_gate = QualityGateMiddleware(
            check_interval=5
        )
        self.auto_compaction = AutoCompactionManager(
            max_input_tokens=200000,
            compaction_threshold=0.85,
        )
        self.execution_budget = ExecutionBudget(
            max_iterations=100,
            max_cost_dollars=10.0,
        )
        self.reasoning_sandwich = ReasoningSandwichMiddleware()

    def process(self, messages, config):
        """Middlewareパイプラインを実行する"""
        # 1. 予算チェック
        within_budget, reason = self.execution_budget.check_budget()
        if not within_budget:
            return self._graceful_shutdown(reason)

        # 2. コンパクション
        messages = self.auto_compaction.check_and_compact(messages)

        # 3. ループ検出
        messages, config = self.loop_detector.modify_request(
            messages, config
        )

        # 4. 推論レベル調整
        config = self.reasoning_sandwich.modify_request(
            messages, config
        )

        # 5. 完了前チェックリスト
        messages, config = self.pre_completion.modify_request(
            messages, config
        )

        return messages, config

    def _graceful_shutdown(self, reason: str):
        """予算超過時のグレースフルシャットダウン"""
        return [{
            "role": "system",
            "content": (
                f"実行予算の上限に到達しました: {reason}\n"
                "現在の進捗をclaude-progress.txtに保存し、"
                "変更をgitにコミットしてからセッションを終了してください。"
            ),
        }], {}
```

---

## 6.9 [Hands-on] 長期実行エージェントの状態管理実装

本節では、本章で解説した実装パターンを統合し、実際に動作する長期実行エージェントの状態管理を構築するハンズオンを行う。3つの演習を通じて、進捗ブリッジング、コンパクション戦略、失敗パターンの検出と対策を体験する。

### 演習1: 進捗ブリッジングの実装

**目的**: セッション間で状態を引き継ぐ進捗ブリッジングを実装し、セッションの中断と再開が正しく動作することを確認する。

**手順**:

1. 以下のプロジェクトディレクトリ構造を作成する。

```
hands-on-ch06/
├── progress_bridge.py      # 進捗ブリッジの実装
├── session_protocol.py     # セッション起動プロトコル
├── claude-progress.json    # 進捗ファイル（自動生成）
└── tests/
    └── test_progress.py    # テスト
```

2. 6.3節の`ProgressBridge`クラスを実装する。

3. 以下のテストケースを実装し、すべて通過することを確認する。

```python
"""tests/test_progress.py: 進捗ブリッジのテスト"""
import os
import json
import tempfile
from progress_bridge import ProgressBridge, Feature, FeatureStatus


def test_create_and_save():
    """進捗ブリッジの作成と保存"""
    bridge = ProgressBridge(
        project_name="テストプロジェクト",
        features=[
            Feature(id=1, title="機能A", description="説明A"),
            Feature(id=2, title="機能B", description="説明B",
                    dependencies=[1]),
        ],
    )

    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False
    ) as f:
        filepath = f.name

    try:
        bridge.save(filepath)
        loaded = ProgressBridge.load(filepath)
        assert loaded.project_name == "テストプロジェクト"
        assert len(loaded.features) == 2
    finally:
        os.unlink(filepath)


def test_next_feature_respects_dependencies():
    """依存関係を考慮した次タスクの選定"""
    bridge = ProgressBridge(
        project_name="テスト",
        features=[
            Feature(id=1, title="基盤", description="基盤機能"),
            Feature(id=2, title="応用", description="応用機能",
                    dependencies=[1]),
        ],
    )

    # 機能1が未完了なので機能2は選択されない
    next_f = bridge.next_feature()
    assert next_f is not None
    assert next_f.id == 1

    # 機能1を完了にすると機能2が選択される
    bridge.features[0].mark_done("abc123")
    next_f = bridge.next_feature()
    assert next_f is not None
    assert next_f.id == 2


def test_completion_ratio():
    """完了率の計算"""
    bridge = ProgressBridge(
        project_name="テスト",
        features=[
            Feature(id=1, title="A", description="",
                    status=FeatureStatus.DONE),
            Feature(id=2, title="B", description="",
                    status=FeatureStatus.TODO),
            Feature(id=3, title="C", description="",
                    status=FeatureStatus.TODO),
        ],
    )
    assert bridge.completion_ratio() == "1/3"


def test_session_continuity():
    """セッション間の継続性の検証"""
    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False
    ) as f:
        filepath = f.name

    try:
        # セッション1: 初期化と機能1の完了
        bridge1 = ProgressBridge(
            project_name="継続性テスト",
            session_id="session-001",
            features=[
                Feature(id=1, title="機能1", description=""),
                Feature(id=2, title="機能2", description=""),
                Feature(id=3, title="機能3", description=""),
            ],
        )
        bridge1.features[0].mark_done("commit-001")
        bridge1.technical_decisions.append(
            "REST APIを採用する"
        )
        bridge1.save(filepath)

        # セッション2: 読み込みと機能2の完了
        bridge2 = ProgressBridge.load(filepath)
        bridge2.session_id = "session-002"
        assert bridge2.completion_ratio() == "1/3"
        assert bridge2.next_feature().id == 2

        bridge2.features[1].mark_done("commit-002")
        bridge2.save(filepath)

        # セッション3: 読み込みと確認
        bridge3 = ProgressBridge.load(filepath)
        assert bridge3.completion_ratio() == "2/3"
        assert bridge3.next_feature().id == 3
        assert len(bridge3.technical_decisions) == 1
    finally:
        os.unlink(filepath)
```

**検証ポイント**:
- 進捗ファイルの保存と読み込みが正しく動作すること
- 依存関係が正しく考慮されること
- セッション間で状態が正確に引き継がれること

### 演習2: コンパクション戦略の適用

**目的**: コンテキストウィンドウの使用率を監視し、閾値に達した際に自動的にコンパクションを発動する仕組みを実装する。

**手順**:

1. 6.4節の`AutoCompactionManager`を実装する。

2. 以下のシナリオを再現し、コンパクションの動作を確認する。

```python
"""コンパクション戦略の動作確認シナリオ"""

def simulate_context_growth():
    """コンテキスト増大のシミュレーション"""
    manager = AutoCompactionManager(
        max_input_tokens=1000,  # テスト用に小さい値
        compaction_threshold=0.85,
        emergency_threshold=0.95,
    )

    messages = [
        {"role": "system", "content": "あなたはコーディングエージェントです。"},
    ]

    # ツールコールをシミュレート
    for i in range(20):
        # ツール呼び出し結果を追加（各200文字 ≒ 50トークン）
        messages.append({
            "role": "tool",
            "tool_call_id": f"call_{i}",
            "content": f"ツール結果 {i}: " + "x" * 200,
        })

        # コンパクションの確認
        messages = manager.check_and_compact(messages)

        tokens = manager._estimate_tokens(messages)
        ratio = tokens / manager.max_input_tokens
        print(
            f"Step {i+1}: "
            f"{tokens} tokens ({ratio:.1%}), "
            f"{len(messages)} messages"
        )
```

**検証ポイント**:
- 85%の閾値でツールエビクションが発動すること
- 95%の閾値で緊急圧縮が発動すること
- 圧縮後もシステムプロンプトと最新の結果が保持されること

### 演習3: 失敗パターンの再現と対策の検証

**目的**: 破滅ループ（パターン5）を人為的に再現し、`LoopDetectionMiddleware`による検出と対策の動作を確認する。

**手順**:

1. 6.8節の`LoopDetectionMiddleware`を実装する。

2. 以下のシナリオで破滅ループを再現する。

```python
"""破滅ループの再現と検出テスト"""

def test_doom_loop_detection():
    """破滅ループの検出テスト"""
    detector = LoopDetectionMiddleware(max_edits_per_file=3)

    # 同一ファイルへの繰り返し編集をシミュレート
    messages = []
    for i in range(5):
        messages.append({
            "role": "assistant",
            "content": f"editing src/api/orders.py を修正しました（試行{i+1}）",
        })
        result_messages, _ = detector.modify_request(
            messages, {}
        )

        looping = detector.check_for_loops()
        if looping:
            print(f"Step {i+1}: ループ検出! "
                  f"ファイル: {looping}")
            # 警告メッセージが注入されたか確認
            if len(result_messages) > len(messages):
                print("  → 警告メッセージが注入されました")
            break
        else:
            print(f"Step {i+1}: 正常")
```

**検証ポイント**:
- 3回以上の同一ファイル編集で警告が発動すること
- 警告メッセージにアプローチ変更の提案が含まれること
- 警告は1回のみ注入されること（二重注入されないこと）

### 演習のまとめ

3つの演習を通じて、以下の実装パターンを体験した。

1. **進捗ブリッジング**: ファイルベースの状態永続化により、セッション間の状態消失を解決する
2. **コンパクション**: 閾値ベースの自動圧縮により、コンテキストロットの進行を抑制する
3. **ループ検出**: ファイル編集の追跡により、破滅ループを早期に検出し、アプローチの再考を促す

これらのパターンは個別に使用するだけでなく、6.8節で示した`LongRunningAgentHarness`のようにMiddlewareパイプラインとして統合することで、長期実行エージェントの信頼性を総合的に向上させることができる。

---

> **Column: Nicholas Carliniの16並列コンパイラ — 「並列性はエージェントの本質的な特性」**
>
> AnthropicのNicholas Carlini氏が2026年2月に公開したCコンパイラ構築の事例（ANT-12）は、マルチエージェント並列実行の可能性を端的に示すものであった。
>
> 16のClaude Opus 4.6インスタンスが並列に動作し、約10万行のRustベースCコンパイラを構築した。約2,000のエージェントセッションが実行され、APIコストは約20,000ドルであった。
>
> この事例で最も興味深いのは、Carlini氏自身が「並列性こそがエージェントの本質的な特性」と指摘している点である。人間のエンジニアが16人で1つのプロジェクトを進める場合、Brooks's Lawが示すように、人数の増加がそのまま生産性の向上につながるとは限らない。コミュニケーションコスト、コードスタイルの不統一、マージコンフリクト——協調のオーバーヘッドが甚大になるからである。
>
> しかし、エージェントの場合は事情が異なる。各エージェントは同一のポリシーファイル（CLAUDE.md等）に従い、同一のコーディング規約に準拠する。コミュニケーションは構造化されたファイルとgitを通じて行われ、人間のような感情的な摩擦は存在しない。適切なハーネスを設計すれば、並列数の増加がほぼリニアに生産性の向上に寄与するのである。
>
> ただし、20,000ドルというAPIコストは、2026年の時点でも決して安くはない。この事例は「技術的に何が可能か」を示すものであり、すべてのプロジェクトで16並列を採用すべきだということを意味するものではない。読者の皆さんには、自身のプロジェクトの規模とコスト制約に合わせて、並列度を慎重に選択していただきたい。

---

## 本章のまとめ

- **長期実行の3つの根本的制約**: コンテキストロット（コンテキスト増大による性能劣化）、セッション間の状態消失、Time Blindness（時間盲目性）が相互に増幅し合い、長期実行エージェントの信頼性を脅かす（ANT-03, ANT-01）

- **Initializer + Coding Agentの2エージェント分離**: Initializerが環境セットアップと機能リスト作成に特化し、Coding Agentが増分的実装に集中することで、コンテキストの最適化、障害の局所化、プロンプト効率の向上が実現される（ANT-01）

- **進捗ブリッジングによる状態復元**: `claude-progress.txt`パターンとgit履歴の二重保証により、セッション間の状態消失を解決する。セッション起動プロトコルの定義が鍵となる（ANT-01, BLG-07）

- **3層のコンパクション戦略**: ツール結果のエビクション（LC-03）、会話履歴の圧縮、閾値ベースの自動発動（85%ルール: LC-04、95% auto-compact: LC-11）、そしてSQLite+MCPによる常時50%以下維持（TLDV-03）という段階的アプローチでコンテキストロットに対処する

- **推論サンドイッチの実証効果**: 計画（extra-high）→ 実装（high）→ 検証（extra-high）のバランス型配分は63.6%を達成し、全フェーズ最大推論の53.9%を約10ポイント上回った（LC-08）

- **マルチエージェント並列実行の可能性**: 16並列Claudeインスタンスによる10万行Cコンパイラ構築事例が、適切なハーネスのもとでの並列性のスケーラビリティを実証した（ANT-12）

- **3段階エージェント構造**: Manager → Planner → Programmer & Reviewerの責務分離と、計画段階でのHuman-in-the-Loop統合が、長期実行における方向性の逸脱を構造的に防止する（LC-17）

- **自己検証ループの必須性**: PreCompletionChecklistMiddlewareによるタスク完了前の検証強制と、トレーシングベースのフィードバックが、品質を担保する（LC-08）

- **5つの失敗パターンの連鎖**: コンテキスト消失、方向性の逸脱、無限ループ、品質劣化、破滅ループは連鎖的に発生する。LoopDetectionMiddleware（LC-08）をはじめとするMiddlewareパイプラインで統合的に対策することが有効である

---

## 参照文献

- [ANT-01] Justin Young, "Effective harnesses for long-running agents", Anthropic Engineering, 2025-11-26. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- [ANT-02] Erik Schluntz, Barry Zhang, "Building Effective Agents", Anthropic, 2024-12-19. https://www.anthropic.com/research/building-effective-agents
- [ANT-03] Prithvi Rajasekaran et al., "Effective Context Engineering for AI Agents", Anthropic Engineering, 2025-09-29. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- [ANT-06] Anthropic Engineering, "How We Built Our Multi-Agent Research System", 2025-06-13. https://www.anthropic.com/engineering/multi-agent-research-system
- [ANT-12] Nicholas Carlini, "Building a C Compiler with a Team of Parallel Claudes", Anthropic Engineering, 2026-02-05. https://www.anthropic.com/engineering/building-c-compiler
- [LC-03] LangChain Team, "Doubling Down on DeepAgents", LangChain Blog, 2025-10-28. https://blog.langchain.com/doubling-down-on-deepagents/
- [LC-04] Chester Curme, Mason Daugherty, "Context Management for Deep Agents", LangChain Blog, 2026-01-28. https://blog.langchain.com/context-management-for-deepagents/
- [LC-08] LangChain Accounts, "Improving Deep Agents with Harness Engineering", LangChain Blog, 2026-02-17. https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- [LC-09] Sydney Runkle, Vivek Trivedy, "Building Multi-Agent Applications with Deep Agents", LangChain Blog, 2026-01-21. https://blog.langchain.com/building-multi-agent-applications-with-deep-agents/
- [LC-11] LangChain Accounts, "Context Engineering for Agents", LangChain Blog, 2025-07-02. https://blog.langchain.com/context-engineering-for-agents/
- [LC-12] Nick Huang, "How agents can use filesystems for context engineering", LangChain Blog, 2025-11-21. https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/
- [LC-13] LangChain, "Agent Engineering: A New Discipline", LangChain Blog, 2025-12-09. https://blog.langchain.com/agent-engineering-a-new-discipline/
- [LC-17] LangChain Accounts, "Introducing Open SWE: An Open-Source Asynchronous Coding Agent", LangChain Blog, 2025-08-06. https://blog.langchain.com/introducing-open-swe-an-open-source-asynchronous-coding-agent/
- [BLG-05] Clay (Seawolf AI), "Harness Engineering and the Discipline of Long-Running Intelligence", Seawolf AI. https://www.seawolfai.net/harness-engineering-and-the-discipline-of-long-running-intelligence/
- [BLG-07] paddo.dev, "Agent Harnesses: From DIY Patterns to Product", 2025-11-28. https://paddo.dev/blog/agent-harnesses-from-diy-to-product/
- [OAI-01] Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11. https://openai.com/index/harness-engineering/
- [TLDV-03] [AIコーディング道場] 共同稽古, 2026-01-08. （社内ミーティング議事録）
- [TLDV-06] 定例）論文リサーチ, 2025-12-03. （社内ミーティング議事録）
