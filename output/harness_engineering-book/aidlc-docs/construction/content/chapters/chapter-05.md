# 第5章: プラットフォーム横断比較

> **読者レベル**: ★★☆（中級 — AI/LLMの基礎知識がある読者向け）
> **想定ページ数**: 約20ページ

> **本章の方針**: 個別プラットフォームの詳細仕様は陳腐化が速いため、**評価軸と選定基準**に重心を置く。具体的なバージョン情報・セットアップ手順はWeb補足（GitHub）で最新版を提供する。本章の比較は**2026年Q1時点**の情報に基づく。

第3章でエージェントハーネスの6つのコンポーネントを、第4章でポリシーとガードレールの設計手法を解説した。本章では、これらの概念が主要プラットフォームでどのように実装されているかを横断的に比較する。ハーネスエンジニアリングにおいてプラットフォーム選定は避けて通れない意思決定であるが、個々のAPIバージョンやセットアップ手順に依存した比較は半年で陳腐化する。そこで本章では、プラットフォームの「設計思想」と「アーキテクチャ上の選択」に焦点を当て、読者が自らの要件に照らして合理的な判断を下すための評価フレームワークを提供する。

---

## 5.1 比較の5軸

プラットフォームを評価するにあたり、本書では5つの評価軸を設定する。これらは、第3章で解説した6つのコンポーネント（Reasoning Engine、Planning & Orchestration、Tool Registry、Memory & Context、State & Persistence、Structured I/O）を、選定判断の観点から再構成したものである。

### アーキテクチャ設計思想

第一の軸は、プラットフォームが採用するアーキテクチャの設計思想である。ここで問うべきは、「そのプラットフォームは、エージェントの構築をどのような抽象レベルで捉えているか」という点である。

Harrison Chase氏が提唱した3層スタック——Framework / Runtime / Harness（LC-01）——は、この軸を理解するための有力なフレームワークとなる。フレームワーク層はモデルとの対話やツール定義を抽象化し、ランタイム層は状態管理や耐久実行を担い、ハーネス層は計画・サブエージェント・コンパクションといった「バッテリー込み」の機能を提供する（TLDV-01）。プラットフォームによっては3層すべてを単一の製品として提供するもの（垂直統合型）もあれば、特定の層に特化するもの（水平特化型）もある。

評価にあたっては以下の問いを立てる。

- **統合度**: 3層のうちどの範囲をカバーしているか。垂直統合型か、特定層への特化型か
- **モデル結合度**: 特定のLLMに最適化されているか、それともモデル非依存（Model-Agnostic）か
- **拡張モデル**: プラグイン、ミドルウェア、フックなど、どのような拡張メカニズムを提供しているか
- **オープンソース戦略**: コア部分はOSSか、プロプライエタリか。コミュニティの規模と活発さはどうか

フレームワークの世代という観点も重要である。LC-14が整理したように、エージェントフレームワークは3つの世代を経て進化してきた。第一世代のChaining（2023年）はLLMをデータとAPIに接続する初期アプローチであり、第二世代のLangGraph（2024年）は耐久性とステートフルネスのためのランタイムサポートを提供し、第三世代のDeepAgents（2025年）は計画・ツール呼び出しループ・サブエージェントオーケストレーションを備えた「バッテリー込み」ハーネスである（LC-14）。あるプラットフォームがどの世代の設計思想に立脚しているかは、その能力の上限を大きく左右する。

### コンテキスト管理戦略

第二の軸は、コンテキストウィンドウの管理戦略である。第2章で論じたように、コンテキストエンジニアリングはハーネスエンジニアリングの中核的な関心事である。長期実行エージェントにおいてコンテキストロット（Context Rot）——コンテキストの増大に伴う性能劣化——をどのように防ぐかは、プラットフォームの実用性を左右する決定的な要素である（ANT-03）。

評価にあたっては以下の問いを立てる。

- **コンパクション機構**: コンテキストウィンドウの自動圧縮・要約をどのように実装しているか。発動閾値はどこに設定されているか
- **コンテキスト分離**: サブエージェントやタスク単位でコンテキストをどう分離しているか
- **外部メモリ統合**: ファイルシステム、データベース、ベクトルストアなど、コンテキストウィンドウ外の記憶機構をどう活用しているか
- **ミドルウェアによるコンテキスト操作**: LLM呼び出しの直前にコンテキストを動的に変更するフック機構が存在するか

LC-08の実験が示したように、コンテキスト管理は単なる付加機能ではなく、エージェントの性能を決定づける基幹機能である。環境コンテキストの配信（ディレクトリ構造マッピング、利用可能ツールの発見、時間予算警告の注入）だけでも、ベンチマークスコアに測定可能な改善をもたらす。

### ツールエコシステムの成熟度

第三の軸は、ツールエコシステムの成熟度である。第3章で解説したTool Registry（ツールレジストリ）は、エージェントが外部世界と相互作用するための基盤であり、その成熟度はプラットフォームの実用性を直接的に規定する。

評価にあたっては以下の問いを立てる。

- **標準プロトコル対応**: MCP（Model Context Protocol）（ANT-15, STD-03）やAGENTS.md（OAI-09, STD-02）など、業界標準のツール接続プロトコルに対応しているか
- **ビルトインツールの充実度**: ファイルシステム操作、コード実行、Web検索など、基本的なツールがどの程度組み込まれているか
- **ツール発見機構**: Tool Search and Discovery（ANT-09）のように、利用可能なツールをオンデマンドで発見・ロードする仕組みがあるか
- **スキル機構**: SKILL.mdのようなプログレッシブ・ディスクロージャー（Progressive Disclosure）——必要な情報を段階的に開示する設計——に対応しているか（LC-15, ANT-10）

ツールエコシステムの評価においては、「数」よりも「設計」が重要である。LC-15が指摘するように、Claude Codeは約12個、Manusは20未満のツールで汎用的な機能を実現している。少数の原子的なツール（ファイルシステム操作、シェルコマンド実行など）を組み合わせることで、専門的なツールを多数用意するよりも柔軟性と認知負荷の低減を同時に達成できるのである。

### ガードレール・安全性機能

第四の軸は、ガードレールと安全性に関する機能の充実度である。第4章で解説したように、エージェントの安全な運用にはポリシー定義、実行時制約、サンドボックスなど多層的な防御が必要である。

評価にあたっては以下の問いを立てる。

- **ポリシーファイル機構**: `AGENTS.md`や`CLAUDE.md`のような宣言的なポリシー定義機構が存在するか
- **実行時ガードレール**: ループ検出、コスト制限、最大反復回数、タイムアウトなどの実行時制約をどう実装しているか
- **サンドボックス**: ファイルシステム分離やネットワーク分離をどの程度実装しているか（ANT-07）
- **権限モデル**: ツールの実行に対する承認フロー（Human-in-the-Loop）をどう設計しているか
- **監査とトレーサビリティ**: エージェントの行動ログをどの程度詳細に記録し、事後分析を可能にしているか

### コスト構造とスケーラビリティ

第五の軸は、コスト構造とスケーラビリティである。エージェントの本番運用においては、トークンコスト、API呼び出しコスト、インフラコストの予測と管理が不可欠である。

評価にあたっては以下の問いを立てる。

- **課金モデル**: トークンベース、タスクベース、サブスクリプションベースなど、どのような課金体系か
- **コスト最適化機構**: 推論計算の適応的配分（LC-08が実証した「推論サンドイッチ」パターンなど）をサポートしているか
- **水平スケーリング**: 複数エージェントの並列実行（ANT-12の16並列事例など）をどうサポートしているか
- **セルフホスティング**: オンプレミスやプライベートクラウドでの運用が可能か
- **トークン効率**: コンパクション、ツール結果のエビクション（不要な結果の除去）など、トークン消費を削減する機構が組み込まれているか

---

## 5.2 主要プラットフォーム概要

本節では、2026年Q1時点で主要なエージェント開発プラットフォームを概観する。各プラットフォームの「設計思想」と「ハーネスとしての特徴」に焦点を当て、5.3節での比較分析の基礎を提供する。

### OpenAI Codex エコシステム

OpenAIのエージェント開発エコシステムは、複数の製品とプロトコルから構成される垂直統合型のプラットフォームである。

**Codex CLI**は、ターミナルベースのコーディングエージェントである。ユーザーの自然言語指示をコード変更に変換し、ファイルシステムとの対話を通じてソフトウェア開発タスクを遂行する。OAI-01で報告された「5ヶ月間のゼロ手書きコード実験」は、このCodex CLIを中核としたワークフローで実現された。エージェントループの内部アーキテクチャ——ユーザー・モデル・ツール間のインタラクション管理と状態遷移——はOAI-03で詳細に解説されている。

**Codex App Server**は、JSON-RPCプロトコルベースの双方向APIを提供するサーバーコンポーネントである（OAI-02）。JetBrains、Xcode、デスクトップアプリケーションなど、複数のクライアントに対して統一されたハーネス層を提供する設計思想を持つ。これにより、エディタやIDEを問わず一貫したエージェント体験を実現することを目指している。

**`AGENTS.md`**は、リポジトリローカルなエージェント指示ファイルのオープンフォーマットである（OAI-09, STD-02）。プロジェクト概要、ビルド・テストコマンド、コードスタイルなどをマークダウン形式で記述し、エージェントにプロジェクト固有の文脈を提供する。2025年12月にLinux Foundation傘下のAgentic AI Foundation（AAIF）に寄贈され（OAI-06）、60,000以上のOSSプロジェクトで採用されている。Codex、Cursor、Devin、GitHub Copilotなど、複数のエージェントがこのフォーマットをサポートしている（STD-02）。

**AgentKit**は、2025年10月のOpenAI DevDayで発表されたエージェント構築ツールキットである（OAI-08）。より広範なエージェントアプリケーション——データ分析、カスタマーサポート、業務自動化など——の構築を支援する。

**OpenAI Agents SDK**は、Swarmプロジェクトから進化した軽量Pythonフレームワークであり、Agents、Handoffs、Guardrails、Runnerの4つのプリミティブで構成される（OAI-11）。組み込みトレーシング機能を持ち、エージェント間のタスク受け渡し（Handoff）パターンに特徴がある。

**モデルとの結合**: OpenAIエコシステムは、GPT-5.1-Codex-Maxに代表される自社モデルに最適化されている（OAI-05）。GPT-5.1-Codex-Maxの特筆すべき機能として、コンパクション——複数のコンテキストウィンドウにまたがる作業をネイティブにサポートする機能——がある。これはモデルレベルでのコンテキスト管理を意味し、ハーネス層とモデル層の境界が曖昧になる興味深い設計選択である。

```
OpenAI Codex エコシステムの構成:

┌─────────────────────────────────────────────────┐
│                 AGENTS.md                        │  ← ポリシー層
├─────────────────────────────────────────────────┤
│            Codex CLI / AgentKit                  │  ← ハーネス層
├─────────────────────────────────────────────────┤
│   Codex App Server (JSON-RPC)                    │  ← ランタイム層
├─────────────────────────────────────────────────┤
│   Agents SDK (Agents/Handoffs/Guardrails/Runner) │  ← フレームワーク層
├─────────────────────────────────────────────────┤
│   GPT-5.x-Codex シリーズ                         │  ← モデル層
└─────────────────────────────────────────────────┘
```

[図5.1: OpenAI Codex エコシステムの層構造]

### Anthropic Claude エコシステム

Anthropicのエージェント開発エコシステムは、安全性を設計原則の中核に据えた点に際立った特徴がある。

**Claude Code**は、Anthropicが提供するターミナルベースのコーディングエージェントである（ANT-13）。約12個のビルトインツール（ファイル読み書き、シェルコマンド実行、Web検索、Glob、Grepなど）を備え、少数の原子的ツールの組み合わせにより広範なタスクに対応する設計思想を持つ。TDD（テスト駆動開発）、コードベース探索、git操作、MCP設定などのベストプラクティスが公式に文書化されている。

サンドボックス機構は特に注目に値する。Linux環境ではbubblewrap、macOS環境ではseatbeltを用いたファイルシステム分離とネットワーク分離の2層境界を実装しており、許可プロンプトを84%削減している（ANT-07）。これにより、セキュリティと自律性のトレードオフを実用的な水準で解決している。

**Claude Agent SDK**は、もともとClaude Code SDKとして公開されていたものが、コーディング以外のエージェント構築への拡張を目的として改名された（ANT-14）。コンテキスト管理、権限モデル、セッション管理、MCP統合をコア機能として提供する。

**`CLAUDE.md`**は、`AGENTS.md`と同様のリポジトリローカルなポリシーファイルであるが、Anthropic固有の設計パターンに最適化されている（ANT-13）。第4章で解説したように、約100行のテーブル・オブ・コンテンツからdocs/ディレクトリへの誘導パターンが推奨される。

**MCP（Model Context Protocol）**は、AIアプリケーションの「USB-C」と喩えられるオープンプロトコルである（ANT-15, STD-03）。JSON-RPCベースのクライアント・サーバー通信を標準化し、ツール、リソース、プロンプトの3つのコアプリミティブを定義する（ANT-16）。2024年11月のオープンソース公開以来、急速に普及し、AAIFの設立プロジェクトの一つとなった（OAI-06）。MCPの重要な設計上の帰結として、コード実行によるMCPツール呼び出しの効率化がある。ANT-08の報告によれば、トークンを85%削減（約134kから約5k）しつつ、オンデマンドのツールロードを実現している。

**安全性への設計姿勢**: Anthropicのエコシステムは、Constitutional AI（ANT-17）やConstitutional Classifiers（ANT-18）といった研究成果に裏打ちされた安全性フレームワークを基盤としている。Responsible Scaling Policy（ANT-19）で定義されたAI Safety Level（ASL-1〜ASL-3+）は、能力に比例した保護のフレームワークであり、この思想がClaude CodeやClaude Agent SDKの権限モデルにも反映されている。

**高度なツール機能**: ANT-09で発表されたAdvanced Tool Useは、Tool Search and Discovery（ツールのオンデマンド発見・ロード）、Programmatic Tool Calling（プログラム的なツール呼び出し）、Learning from Examples（事例からの学習）の3機能を導入し、単純な関数呼び出しからインテリジェントなオーケストレーションへの進化を実現している。

```
Anthropic Claude エコシステムの構成:

┌─────────────────────────────────────────────────┐
│              CLAUDE.md / SKILL.md                │  ← ポリシー層
├─────────────────────────────────────────────────┤
│              Claude Code                         │  ← ハーネス層
│  （サンドボックス: bubblewrap / seatbelt）         │
├─────────────────────────────────────────────────┤
│          Claude Agent SDK                        │  ← ランタイム/フレームワーク層
│  （コンテキスト管理・権限モデル・セッション管理）    │
├─────────────────────────────────────────────────┤
│        MCP (Model Context Protocol)              │  ← ツール接続層
│  （ツール・リソース・プロンプト）                    │
├─────────────────────────────────────────────────┤
│   Constitutional AI / Safety Classifiers         │  ← 安全性基盤
├─────────────────────────────────────────────────┤
│        Claude (Opus / Sonnet / Haiku)            │  ← モデル層
└─────────────────────────────────────────────────┘
```

[図5.2: Anthropic Claude エコシステムの層構造]

### LangChain / LangGraph / DeepAgents

LangChainエコシステムは、Chase氏自身が明確に定義した3層スタック——Framework / Runtime / Harness——を最も忠実に体現するプラットフォームである（LC-01, TLDV-01）。モデル非依存の設計思想に立脚し、OpenAI、Anthropic、Google、オープンソースモデルなど、多様なLLMプロバイダーを横断して利用できる点が最大の特徴である。

#### 3層構造: LangChain → LangGraph → DeepAgents

**LangChain（Framework層）**は、LLMとの対話、ツール定義、外部サービスとの統合を抽象化するフレームワークである。バージョン1.0でミドルウェア（Middleware）の概念が導入され、エージェントの動作を拡張可能なフック機構で制御できるようになった（TLDV-01）。

**LangGraph（Runtime層）**は、耐久性とステートフルネスを提供するランタイム層である。グラフベースの状態管理、チェックポインティング、長時間実行エージェントの支援を中核機能とする。Chase氏の表現を借りれば「低レベルのエージェントランタイム」であり、細粒度の制御が必要な場面に適している（TLDV-01）。

**DeepAgents（Harness層）**は、LangChainとLangGraphの上に構築される「バッテリー込み」のハーネスである。Chase氏が直接定義した4つの組み込み機能——計画ツール、サブエージェント、ファイルシステムアクセス、自動要約・コンパクション——を備え、長時間実行される自律的なエージェントに最適化されている（TLDV-01）。

> deep agents, we think of as like an agent harness. We think it's really good for like longer running, more autonomous agents.
>
> （Deep Agentsはエージェントハーネスです。長時間実行される、より自律的なエージェントに適しています。）
> —— Harrison Chase（TLDV-01）

DeepAgentsの初期バージョン（LC-02）は、単純なツール呼び出しループが「浅い」エージェントにしかならないという問題提起から出発し、計画ツール、サブエージェント、ファイルシステムアクセス、詳細プロンプトの4機能で「深い」エージェントを実現することを目指した。v0.2（LC-03）ではプラガブルBackend抽象化（LangGraph State、LangGraph Store、ローカルファイルシステム）が導入され、大規模ツール結果のエビクションと会話履歴要約が実装された。

#### Middleware概念: modify model requestフック

LangChainエコシステムの中核的な拡張機構であるミドルウェアは、コンテキストエンジニアリングの実装基盤として極めて重要な位置を占める。LangChainのオープンソースエンジニアであるSydney Runkle氏は、2025年10月のVIPコミュニティコールで次のように説明している。

> it also exposes another core hook, which we're calling modify model request. And that is really critical in the context engineering space. Modifying your model request allows you to change basically anything under the sun related to the upcoming LLM call.
>
> （もう一つのコアフックとして、modify model requestを公開しています。これはコンテキストエンジニアリングの領域で極めて重要です。モデルリクエストの変更により、次のLLM呼び出しに関するほぼすべてを変更できます。）
> —— Sydney Runkle（TLDV-02）

modify model requestフックで変更可能な項目は以下の通りである（TLDV-02）。

- **モデル**: タスクの特性に応じて動的にモデルを切り替える
- **ツール**: 利用可能なツールセットを動的に追加・削除する
- **システムプロンプト**: コンテキストに応じてシステムプロンプトを書き換える
- **メッセージ履歴**: 過去の対話履歴を要約・フィルタリングする
- **モデル設定**: 温度（temperature）や推論レベルなどのパラメータを動的に調整する

プリビルトミドルウェアとして、human-in-the-loop（人間の承認を挟む）、summarization（要約）、planning/todoパターン（計画管理）、file systemパターン（ファイルシステム連携）が用意されている（TLDV-02）。さらに、LC-08で報告されたTerminal Bench 2.0の改善では、以下の専用ミドルウェアが実装された。

- **LocalContextMiddleware**: ディレクトリ構造のマッピング、利用可能ツールの発見、時間予算警告の注入を行う
- **PreCompletionChecklistMiddleware**: タスク完了前に検証パスを強制する
- **LoopDetectionMiddleware**: N回以上の同一ファイル編集を検出し、アプローチ変更を促すコンテキストを注入する

この設計は、`create_react_agent`から`create_agent` + middlewareへの進化として位置づけられている（TLDV-02）。従来の「反応的なエージェント」から、ミドルウェアスタックによって拡張可能な「構成的なエージェント」への転換である。

#### マルチエージェント: Subagents + Skills

DeepAgentsフレームワークは、マルチエージェント構成のために2つのプリミティブ——Subagents（サブエージェント）とSkills（スキル）——を提供する（LC-09）。

**Subagents**は、コンテキストの肥大化問題に対処するための委譲パターンである。メインエージェントのコンテキストウィンドウがほぼ満杯になったとき、専門的なタスクを独立したコンテキストを持つサブエージェントに委譲する。サブエージェントは独自のツールセット、システムプロンプト、さらにはモデルさえも持つことができ、タスクの結果のみがメインエージェントに返される（LC-09）。

```python
# Subagent定義の例（LC-09）
research_subagent = {
    "name": "research-agent",
    "description": "深い質問をより詳しく調査するために使用",
    "system_prompt": "優れた研究者です",
    "tools": [internet_search],
    "model": "openai:gpt-4o"
}
```

**Skills**は、SKILL.mdファイルによるプログレッシブ・ディスクロージャーを実現するパターンである（LC-09, LC-15, ANT-10）。

#### スキルとプログレッシブ・ディスクロージャー

スキル機構は、ハーネスのツールエコシステム設計において特筆すべき革新である。その核心は「プログレッシブ・ディスクロージャー」——必要な情報を必要な時点で段階的に開示する設計原則——にある（LC-15, ANT-10）。

従来のツール定義では、すべてのツールの詳細仕様がコンテキストウィンドウに常時ロードされていた。ツール数が増えるにつれてコンテキストウィンドウが圧迫され、エージェントの推論品質が低下する。これは第3章で解説した「コンテキスト混乱（Context Confusion）」の一般的な原因である。

SKILL.mdによるスキル機構は、この問題を以下のように解決する（LC-15）。

1. **デフォルト時**: YAML前置き（名前、説明、適用条件）のみがコンテキストにロードされる
2. **必要時**: エージェントがタスクの特性に基づいて判断し、完全なSKILL.mdファイルを読み込む
3. **動的生成**: エージェントが新しいタスクに遭遇した際、新しいスキルを自動的に作成できる

```
# スキルのファイル構造例
.deepagents/skills/
├── deploy/
│   └── SKILL.md          # デプロイ手順のスキル定義
├── review-pr/
│   └── SKILL.md          # PRレビューのスキル定義
└── database-migration/
    └── SKILL.md          # DB移行のスキル定義
```

このアプローチにより、Claude Codeが約12個、Manusが20未満のツールで汎用的な機能を実現している事実が理解できる（LC-15）。少数の原子的なツールにスキル機構を組み合わせることで、事実上無限のタスク対応能力を、最小限のコンテキスト消費で実現しているのである。

SubagentsとSkillsの使い分けについて、LC-09は以下のガイドラインを示している。

| 必要な処理 | 推奨パターン |
|----------|----------|
| 複雑な多段階作業の委譲 | Subagents |
| 手続きの再利用 | Skills |
| 特定タスク用の専門ツール | Subagents（焦点ツール） |
| 複数エージェント間の共有能力 | Skills |
| 大規模ツール集の管理 | Skills |

[表5.1: Subagents と Skills の使い分けガイドライン]

```
LangChain / LangGraph / DeepAgents の構成:

┌─────────────────────────────────────────────────┐
│         SKILL.md / Middlewares                    │  ← ポリシー/拡張層
├─────────────────────────────────────────────────┤
│            DeepAgents                            │  ← ハーネス層
│  （計画ツール・サブエージェント・コンパクション）     │
├─────────────────────────────────────────────────┤
│            LangGraph                             │  ← ランタイム層
│  （グラフ状態管理・チェックポイント・耐久実行）      │
├─────────────────────────────────────────────────┤
│            LangChain 1.0+                        │  ← フレームワーク層
│  （抽象化・ツール定義・Middleware）                 │
├─────────────────────────────────────────────────┤
│   任意のLLMプロバイダー                            │  ← モデル層
│  （OpenAI / Anthropic / Google / OSS）            │
└─────────────────────────────────────────────────┘
```

[図5.3: LangChain / LangGraph / DeepAgents の層構造]

### その他の主要プラットフォーム

以下では、上記3大エコシステム以外の注目すべきプラットフォームを概観する。いずれもハーネスエンジニアリングの観点から独自の設計選択を行っており、特定のユースケースにおいて有力な選択肢となりうる。

#### Google Agent Development Kit（ADK）

Googleが2025年4月にオープンソースとしてリリースしたADKは、Geminiモデルに最適化されたエージェントフレームワークである（PLT-03）。マルチエージェント設計を基本とし、双方向のオーディオ・ビデオストリーミングに対応する点がユニークである。Google Cloudとの深い統合により、エンタープライズ環境でのスケーラビリティに優位性がある。ただし、Gemini以外のモデルへの対応は限定的であり、モデル結合度が比較的高い。

#### Salesforce Agentforce

Salesforceは、エージェントハーネスを「エージェントの実行、状態、信頼性を管理するランタイム環境とインフラストラクチャ」と定義しており（PLT-01）、ビジネスプロセス自動化に特化したエコシステムを構築している。5つのエージェントタイプ——会話型、プロアクティブ、アンビエント、自律型、協調型——のアーキテクチャパターンを定義し（PLT-02）、CRM領域での豊富なドメイン知識を活用できる点が強みである。モデルスワップ可能な設計を採用しており（PLT-01）、特定のLLMへのロックインを回避する方針を打ち出している。

#### CrewAI

CrewAIは、ロールベースアーキテクチャを特徴とするフレームワークである（PLT-04）。Agent、Task、Crew、Flowの4つのプリミティブで構成され、Flow/Crewデュアルアーキテクチャ——Flowsが決定論的オーケストレーター、Crewsが自律協調チーム——を採用している。「ロール」というメタファーにより、非エンジニアにもエージェント設計が直感的に理解しやすい点が特徴である。一方で、ハーネスとしてのコンパクション機構やプログレッシブ・ディスクロージャーは、LangChainエコシステムほどには成熟していない。

#### Microsoft Agent Framework

Microsoftは、AutoGenとSemantic Kernelを統合したAgent Frameworkを2025年10月にパブリックプレビューとして公開した（PLT-06）。.NETとPythonの両方に対応し、グラフベースワークフロー、MCP統合、OpenTelemetryベースのオブザーバビリティをサポートする。Azure OpenAI Serviceとの深い統合により、エンタープライズレベルのセキュリティとコンプライアンスを容易に実現できる点が強みである。

#### Vercel AI SDK

Vercel AI SDK 6は、エージェントをファーストクラスの抽象として導入し、Agent interface、ツール実行承認パターン、MCP対応を備えたTypeScript中心のフレームワークである（PLT-05）。Web/フロントエンド開発者にとっては最も低い参入障壁を提供するが、長期実行エージェントやバックエンド中心のユースケースでは、ランタイム層やハーネス層の機能が他のプラットフォームに比べて限定的である。

---

> **Column: フレームワークの世代交代は止まらない**
>
> LangChainのLC-14は、フレームワークの有用性について率直な見解を示している。「Agent frameworks are still useful, but only if they evolve as fast as the models do.」（エージェントフレームワークは依然として有用であるが、モデルと同じ速度で進化する場合に限る。）
>
> この指摘は、プラットフォーム選定における重要な視点を提供する。2023年のChainingから2024年のLangGraph、2025年のDeepAgentsへと、フレームワークの世代交代は約1年周期で起きている（LC-14）。この速度を考えると、2026年にもまた新たな世代が登場する可能性は十分にある。
>
> したがって、プラットフォームの選定において最も重視すべきは、現時点での機能の網羅性ではなく、**変化への適応力**である。コミュニティの活発さ、リリース頻度、モデルの進化に対する追従速度——これらの「動的な指標」こそが、長期的な投資判断の鍵となる。
>
> 同時に、オブザーバビリティの独立性も重要な設計判断である。LangSmithがLangChainのOSSツールから意図的に独立して構築された（LC-14）ように、フレームワークの世代交代が起きてもトレーシングやデバッグの基盤が影響を受けない設計は、運用の安定性を大きく高める。OpenTelemetryベースのフレームワーク非依存オブザーバビリティ（LC-14）は、この観点から推奨されるアプローチである。

---

## 5.3 比較分析

### 5軸 × 主要プラットフォーム比較表

以下の比較表は、5.1節で定義した5つの評価軸に沿って、主要プラットフォームを横断的に比較したものである。評価は2026年Q1時点の公開情報に基づく。

#### アーキテクチャ設計思想

| 評価項目 | OpenAI Codex | Anthropic Claude | LangChain/DeepAgents | Google ADK | Salesforce Agentforce | CrewAI | MS Agent Framework | Vercel AI SDK |
|---------|-------------|-----------------|---------------------|-----------|---------------------|--------|-------------------|-------------|
| スタック範囲 | 垂直統合（全層） | 垂直統合（全層） | 明示的3層分離 | フレームワーク中心 | ランタイム＋業務ロジック | フレームワーク中心 | フレームワーク＋ランタイム | フレームワーク中心 |
| モデル結合度 | 高（GPT系最適化） | 高（Claude系最適化） | 低（モデル非依存） | 中〜高（Gemini最適化） | 低（モデルスワップ可） | 低（モデル非依存） | 中（Azure OpenAI最適化） | 低（モデル非依存） |
| フレームワーク世代 | 第三世代相当 | 第三世代相当 | 明示的に第三世代 | 第二〜三世代 | 第二世代 | 第二世代 | 第二〜三世代 | 第二世代 |
| OSSコア | 部分的 | 部分的 | 完全OSS | 完全OSS | プロプライエタリ | 完全OSS | 完全OSS | 完全OSS |

[表5.2: アーキテクチャ設計思想の比較]

#### コンテキスト管理戦略

| 評価項目 | OpenAI Codex | Anthropic Claude | LangChain/DeepAgents | Google ADK | Salesforce Agentforce | CrewAI | MS Agent Framework | Vercel AI SDK |
|---------|-------------|-----------------|---------------------|-----------|---------------------|--------|-------------------|-------------|
| コンパクション | モデルネイティブ | auto-compact（95%閾値） | 85%閾値の3段階圧縮 | 基本的 | 限定的 | 基本的 | 基本的 | 限定的 |
| コンテキスト分離 | セッション単位 | サブエージェント単位 | Subagents/Skills | エージェント間 | エージェントタイプ別 | Crew/Agent単位 | グラフノード単位 | セッション単位 |
| 外部メモリ | ファイルシステム | ファイルシステム＋MCP | LangGraph Store＋FS | Google Cloud統合 | Salesforce Data Cloud | 基本的 | Semantic Memory | 限定的 |
| ミドルウェア | 限定的 | ツールフック | modify model request | コールバック | 限定的 | フック | パイプライン | 限定的 |

[表5.3: コンテキスト管理戦略の比較]

ここで特に注目すべきは、コンパクション機構の実装差異である。OpenAI Codex系はGPT-5.1-Codex-Maxのモデルネイティブなコンパクション（OAI-05）に依存する設計を選択した。これは、モデル自体が複数コンテキストウィンドウにまたがる作業を処理できるため、ハーネス側での複雑な圧縮ロジックが不要になるという利点がある。一方、LangChain/DeepAgentsは、max_input_tokensの85%で自動発動する3つの圧縮技術をハーネス側で実装している（LC-04）。Anthropic Claude Codeはコンテキストウィンドウ使用率95%で自動要約を発動するauto-compactを採用している。

モデルネイティブ vs ハーネス側実装というこの設計選択は、モデル依存度と制御性のトレードオフを体現している。モデルネイティブなアプローチは実装が簡潔になるが特定モデルへの依存度が高まる。ハーネス側実装はモデル非依存性を維持できるが、圧縮アルゴリズムの設計と調整が必要になる。

#### ツールエコシステムの成熟度

| 評価項目 | OpenAI Codex | Anthropic Claude | LangChain/DeepAgents | Google ADK | Salesforce Agentforce | CrewAI | MS Agent Framework | Vercel AI SDK |
|---------|-------------|-----------------|---------------------|-----------|---------------------|--------|-------------------|-------------|
| MCP対応 | AAIF経由 | ネイティブ | 統合対応 | 部分的 | 限定的 | コミュニティ | 統合対応 | 対応 |
| AGENTS.md対応 | ネイティブ | CLAUDE.md | 非対応（SKILL.md） | 非対応 | 非対応 | 非対応 | 非対応 | 非対応 |
| ビルトインツール数 | 多数 | 約12個 | 設定可能 | Gemini統合 | CRM特化 | ロール特化 | 設定可能 | 基本的 |
| ツール発見機構 | 基本的 | Advanced Tool Use | Skills＋Subagents | 基本的 | ドメイン特化 | 基本的 | 基本的 | 基本的 |
| プログレッシブ・ディスクロージャー | 部分的 | Agent Skills | SKILL.md | 非対応 | 非対応 | 非対応 | 非対応 | 非対応 |

[表5.4: ツールエコシステムの成熟度の比較]

ツールエコシステムにおいて、MCPとAGENTS.mdの標準化動向は特に重要である。両プロトコルがAAIFの設立プロジェクトとして寄贈された（OAI-06, STD-01）ことで、プラットフォーム横断的な相互運用性が今後急速に改善されると予想される。プラチナメンバーにはAWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAIが名を連ねており（STD-01）、業界全体としてのコミットメントは明確である。

プログレッシブ・ディスクロージャーの実装状況も差別化要因として注目すべきである。現時点でこの機構を本格的に実装しているのは、Anthropic（Agent Skills, ANT-10）とLangChain（SKILL.md, LC-15）のみであり、他のプラットフォームではツール定義の全量がコンテキストに読み込まれる設計のままである。コンテキストウィンドウが有限資源である以上、この差異は長期実行・多ツール環境において顕著な性能差をもたらしうる。

#### ガードレール・安全性機能

| 評価項目 | OpenAI Codex | Anthropic Claude | LangChain/DeepAgents | Google ADK | Salesforce Agentforce | CrewAI | MS Agent Framework | Vercel AI SDK |
|---------|-------------|-----------------|---------------------|-----------|---------------------|--------|-------------------|-------------|
| ポリシーファイル | AGENTS.md | CLAUDE.md | SKILL.md | 基本的 | Agentforce設定 | ロール定義 | Semantic Kernel | 基本的 |
| サンドボックス | 環境分離 | 2層分離（ANT-07） | Docker/Modal対応 | Cloud Run | Salesforce Trust | 基本的 | Azure Container | 限定的 |
| ループ検出 | 基本的 | 組み込み | LoopDetectionMW | 限定的 | 限定的 | 基本的 | 基本的 | 限定的 |
| Human-in-the-Loop | 承認プロンプト | 権限モデル | Middleware | コールバック | 承認フロー | 基本的 | パイプライン | 承認パターン |
| 監査ログ | 組み込み | トレーシング | LangSmith統合 | Cloud Logging | Salesforce Audit | 基本的 | OpenTelemetry | 限定的 |

[表5.5: ガードレール・安全性機能の比較]

安全性機能において、Anthropicの優位性は明確である。Constitutional AIの研究成果（ANT-17）に裏打ちされた理論的基盤、Constitutional Classifiersによるジェイルブレイク成功率4.4%への低減（ANT-18）、bubblewrap/seatbeltによる2層サンドボックス（ANT-07）など、安全性が設計原則の中核に位置づけられている。

一方、LangChain/DeepAgentsは、ミドルウェアパターンによる柔軟なガードレール実装を強みとする。LC-08で実証されたLoopDetectionMiddlewareやPreCompletionChecklistMiddlewareは、ドメイン固有のガードレールをコードとして定義し、エージェントの動作に注入できる拡張性を持つ。TLDV-02で議論されたように、ガードレールをミドルウェアとして実装し、悪用検出のための統計的プロセス制御として活用するアプローチは、運用監視との統合という点で独自の価値がある。

#### コスト構造とスケーラビリティ

| 評価項目 | OpenAI Codex | Anthropic Claude | LangChain/DeepAgents | Google ADK | Salesforce Agentforce | CrewAI | MS Agent Framework | Vercel AI SDK |
|---------|-------------|-----------------|---------------------|-----------|---------------------|--------|-------------------|-------------|
| 課金モデル | トークン＋サブスク | トークン＋サブスク | OSS（インフラ自前） | トークン＋Cloud | ライセンス＋従量 | OSS＋Enterprise | Azure＋トークン | OSS＋Cloud |
| 推論コスト最適化 | モデルネイティブ | auto-compact | 推論サンドイッチ | 基本的 | 限定的 | 基本的 | 基本的 | 限定的 |
| 並列スケーリング | クラウドネイティブ | API並列 | LangGraph Platform | Cloud Run | Hyperforce | 基本的 | Azure Scale | Serverless |
| セルフホスティング | 不可 | API経由のみ | 完全対応 | 部分的 | 不可 | 完全対応 | Azure/オンプレ | 完全対応 |
| トークン効率化 | コンパクション | MCP最適化（85%削減） | エビクション＋要約 | 基本的 | 限定的 | 基本的 | 基本的 | 限定的 |

[表5.6: コスト構造とスケーラビリティの比較]

コスト構造において最も根本的な分岐点は、「プロプライエタリクラウドサービス」か「セルフホスティング可能なOSS」かという選択である。OpenAI CodexとAnthropic Claudeは前者に該当し、APIの利用料金がランニングコストの主要部分を占める。LangChain/DeepAgents、CrewAI、Vercel AI SDKは後者に該当し、インフラコストは自前で管理するが、ライセンス料は不要である。

LC-08が実証した「推論サンドイッチ」パターン——計画フェーズにextra-high、実装フェーズにhigh、検証フェーズにextra-highの推論コストを配分する——は、コスト最適化の実践的な手法として注目に値する。すべてのフェーズで最大推論を使用する場合の53.9%に対し、バランス型配分は63.6%を達成し、かつタイムアウト失敗を防止した（LC-08）。この結果は、「高い推論コスト = 高い性能」という単純な等式が成立しないことを示しており、コスト効率と性能の同時最適化が可能であることを実証している。

### ユースケース別推奨マトリクス

上記の5軸比較を踏まえ、代表的なユースケースに対する推奨プラットフォームを以下に整理する。推奨は、各ユースケースの主要な要件と5つの評価軸の重み付けに基づく。

| ユースケース | 第一推奨 | 第二推奨 | 主要な選定理由 |
|------------|---------|---------|-------------|
| コーディングエージェント（個人利用） | Claude Code | Codex CLI | サンドボックス、ビルトインツールの完成度 |
| コーディングエージェント（チーム運用） | DeepAgents + LangSmith | Codex + AGENTS.md | オブザーバビリティ、ミドルウェア拡張性 |
| 長期実行自律エージェント | DeepAgents | Claude Agent SDK | コンパクション、Subagents、スキル |
| エンタープライズ業務自動化 | Salesforce Agentforce | MS Agent Framework | ドメイン知識、既存システム統合 |
| マルチモーダルエージェント | Google ADK | OpenAI AgentKit | 音声・映像ストリーミング、マルチモーダルモデル |
| Webアプリ統合エージェント | Vercel AI SDK | LangChain | TypeScript対応、フロントエンド統合 |
| 研究・プロトタイピング | LangChain/LangGraph | CrewAI | モデル非依存性、柔軟な実験環境 |
| 高セキュリティ要件 | Claude Code | MS Agent Framework | Constitutional AI、サンドボックス、コンプライアンス |

[表5.7: ユースケース別推奨マトリクス]

ただし、この推奨マトリクスはあくまで出発点である。実際の選定においては、チームの技術スタック、既存インフラとの統合要件、コスト予算、セキュリティ要件、そして何よりも「変化への適応力」を総合的に考慮すべきである。

### ベンダーロックイン回避とマルチプロバイダー戦略

プラットフォーム選定において、ベンダーロックインのリスクは慎重に評価すべきである。特にモデル結合度の高いプラットフォーム（OpenAI Codex、Anthropic Claude、Google ADK）を選択する場合、モデルプロバイダーの価格改定、API仕様変更、サービス提供方針の変化がビジネスに直接影響を及ぼすリスクがある。

#### ロックインのレイヤー分析

ベンダーロックインは単一のレイヤーではなく、複数のレイヤーで同時に発生しうる。

**モデル層のロックイン**: 特定のモデルの独自機能（GPT-5.1-Codex-Maxのネイティブコンパクションなど）に依存すると、モデル切り替えのコストが増大する。対策としては、モデル固有の機能に依存する部分をハーネス側のアブストラクション層で吸収する設計が有効である。

**ツール層のロックイン**: 独自のツール定義フォーマットに依存すると、プラットフォーム間でのツールの再利用が困難になる。MCPの普及（STD-03）はこの問題を緩和する最も有望な動向である。MCPに準拠したツール定義は、対応する任意のプラットフォームで利用可能になる。

**オブザーバビリティ層のロックイン**: プラットフォーム固有のトレーシング・モニタリング機構に依存すると、プラットフォーム移行時にオブザーバビリティ基盤を再構築する必要が生じる。OpenTelemetryベースのフレームワーク非依存オブザーバビリティ（LC-14）は、この問題への有効な対策である。

**ポリシー層のロックイン**: `AGENTS.md`と`CLAUDE.md`は似た概念であるが互換性がない。AAIFによる標準化の進展（STD-01）が、この問題の緩和に寄与することが期待される。

#### マルチプロバイダー戦略の設計パターン

ベンダーロックインを回避しつつ各プラットフォームの強みを活かすために、以下の3つのマルチプロバイダー戦略が考えられる。

**パターン1: アブストラクション層戦略**

自社のエージェントアプリケーションとモデルプロバイダーの間にアブストラクション層を設ける。LangChain/LangGraphはまさにこの役割を果たす設計であり、モデルを切り替えてもハーネスのロジックを変更する必要がない。ただし、アブストラクション層自体への依存が新たなロックインとなりうる点には留意が必要である。

```python
# アブストラクション層によるモデル切り替えの例
from langchain.chat_models import init_chat_model

# 設定ファイルまたは環境変数でモデルを切り替え
model = init_chat_model(
    model="anthropic:claude-sonnet-4",  # 必要に応じて変更可能
    # model="openai:gpt-5.1-codex",
    # model="google:gemini-2.5-pro",
)
```

**パターン2: MCP統一ツール層戦略**

ツール層をMCPで統一し、プラットフォーム側はMCPクライアントとしてのみ機能させる。これにより、ツールの実装はプラットフォームから独立し、プラットフォーム移行時にもツール資産を保持できる。ANT-08の報告によれば、MCPによるツール実行はトークン効率の面でも有利であり（85%削減）、コスト最適化と可搬性を同時に実現できる。

**パターン3: ハイブリッド運用戦略**

タスクの特性に応じて複数のプラットフォームを使い分ける。たとえば、コーディングタスクにはClaude Code、データ分析にはOpenAI Codex、業務自動化にはSalesforce Agentforceというように、それぞれの強みを活かした分業である。この戦略の課題は、複数プラットフォームの運用・保守コストと、プラットフォーム間でのコンテキスト共有である。

#### AAIF標準化の影響

Agentic AI Foundation（AAIF）の設立（OAI-06, STD-01）は、ベンダーロックイン問題に対する業界レベルの解決策として注目に値する。AAIFはMCP、AGENTS.md、gooseを設立プロジェクトとし、プラチナメンバーにAWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAIが参画している。

この標準化の動向は、以下の点でプラットフォーム選定に影響を与える。

1. **ツール互換性の向上**: MCPの普及により、プラットフォーム間でのツール再利用性が高まる
2. **ポリシーファイルの収束**: AGENTS.mdの標準化が進めば、プラットフォーム固有のポリシーフォーマットが統一される可能性がある
3. **エコシステムの開放**: 60,000以上のOSSプロジェクトがAGENTS.mdを採用している現状（STD-02）は、エコシステムの相互運用性が既に臨界点に達していることを示唆する

ACD-08のシステマティックレビューが指摘するように、現在のエージェントフレームワークの課題は安全ガードレールとサービス指向パラダイムの評価にある。AAIFの標準化は、これらの課題に対する業界共通のアプローチを確立する可能性を秘めている。

---

> **Column: 「正しい選択」は存在しない — 選定プロセスの設計**
>
> 本章の比較表を見て、「結局どれが一番良いのか」という問いを抱く読者は少なくないだろう。しかし、ハーネスエンジニアリングの実践においては、「唯一の正解」は存在しない。
>
> Manusの開発チームが6ヶ月で5回ハーネスを書き直した事例（BLG-02）が示すように、最良のハーネスは反復的な改善を通じてのみ到達できる。BLG-06が指摘する3原則——「再アーキテクチャを受け入れる」「ビルダーにとってのより高い抽象レベル」「シンプルさは不可欠」——は、プラットフォーム選定にも当てはまる。
>
> 重要なのは、最初の選択を「正しく」行うことよりも、選択を見直し、必要に応じて移行できる設計にしておくことである。MCP対応のツール層を維持する、OpenTelemetryベースのオブザーバビリティを採用する、ビジネスロジックをプラットフォーム固有のAPIから分離する——こうした「移行可能性の設計」こそが、急速に進化するAIエージェント領域で生き残るための鍵である。
>
> BLG-11の「12 Factor Agents」が説くように、本番対応エージェントの構築は一度きりの設計作業ではなく、継続的な適応のプロセスである。プラットフォームの選定もまた、そのプロセスの一部として位置づけるべきである。

---

## 本章のまとめ

- **5つの評価軸**: プラットフォーム比較には、アーキテクチャ設計思想、コンテキスト管理戦略、ツールエコシステムの成熟度、ガードレール・安全性機能、コスト構造とスケーラビリティの5軸を用いるべきである。個別の機能比較は陳腐化が速いが、設計思想に基づく比較は長期的な判断基準として有効である
- **3つの主要エコシステム**: OpenAI Codex（垂直統合・モデルネイティブ機能）、Anthropic Claude（安全性中心設計・MCPエコシステム）、LangChain/DeepAgents（明示的3層分離・モデル非依存）がハーネスエンジニアリングの3大エコシステムを形成しており、それぞれ異なる設計哲学に立脚している
- **ミドルウェアとスキルの革新**: LangChainのmodify model requestフック（TLDV-02）とSKILL.mdによるプログレッシブ・ディスクロージャー（LC-15, ANT-10）は、コンテキストエンジニアリングとツール管理における重要な革新であり、これらの機構の有無がプラットフォームの実用性を大きく左右する
- **AAIF標準化の影響**: MCP、AGENTS.md、gooseのAAIFへの寄贈（OAI-06, STD-01）は、プラットフォーム間の相互運用性を高め、ベンダーロックインのリスクを長期的に低減する方向に作用する
- **選定は反復プロセス**: プラットフォームの選定は一度きりの意思決定ではなく、継続的な評価と移行可能性の設計を含む反復プロセスとして捉えるべきである。変化への適応力——コミュニティの活発さ、リリース頻度、モデル進化への追従速度——が最も重要な選定基準である（LC-14）

---

## 参照文献

- [OAI-01] Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world", OpenAI, 2026-02-11. https://openai.com/index/harness-engineering/
- [OAI-02] OpenAI Team, "Unlocking the Codex harness: how we built the App Server", OpenAI, 2026-02-04. https://openai.com/index/unlocking-the-codex-harness/
- [OAI-03] Michael Bolin, "Unrolling the Codex agent loop", OpenAI, 2026-01. https://openai.com/index/unrolling-the-codex-agent-loop/
- [OAI-05] OpenAI, "Building more with GPT-5.1-Codex-Max", 2025-12-18. https://openai.com/index/gpt-5-1-codex-max/
- [OAI-06] OpenAI / Linux Foundation, "OpenAI co-founds the Agentic AI Foundation", 2025-12-09. https://openai.com/index/agentic-ai-foundation/
- [OAI-08] OpenAI, "Introducing AgentKit", 2025-10-06. https://openai.com/index/introducing-agentkit/
- [OAI-09] OpenAI Developers, "Custom instructions with AGENTS.md". https://developers.openai.com/codex/guides/agents-md/
- [OAI-11] OpenAI, "OpenAI Agents SDK". https://openai.github.io/openai-agents-python/
- [ANT-03] Prithvi Rajasekaran et al., "Effective Context Engineering for AI Agents", Anthropic Engineering, 2025-09-29. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- [ANT-07] Anthropic Engineering, "Beyond Permission Prompts: Making Claude Code More Secure and Autonomous", 2025-10-20. https://www.anthropic.com/engineering/claude-code-sandboxing
- [ANT-08] Anthropic Engineering, "Code Execution with MCP: Building More Efficient Agents", 2025-11-04. https://www.anthropic.com/engineering/code-execution-with-mcp
- [ANT-09] Anthropic Engineering, "Introducing Advanced Tool Use", 2025-11-24. https://www.anthropic.com/engineering/advanced-tool-use
- [ANT-10] Barry Zhang, Keith Lazuka, Mahesh Murag, "Equipping Agents for the Real World with Agent Skills", Anthropic Engineering, 2025-10-16. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- [ANT-13] Anthropic Engineering, "Claude Code: Best Practices for Agentic Coding", 2025-04-18. https://www.anthropic.com/engineering/claude-code-best-practices
- [ANT-14] Anthropic, "Building Agents with the Claude Agent SDK", 2025-09-29. https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- [ANT-15] Anthropic, "Introducing the Model Context Protocol", 2024-11-25. https://www.anthropic.com/news/model-context-protocol
- [ANT-16] MCP Community / Anthropic, "MCP Specification (2025-11-25)". https://modelcontextprotocol.io/specification/2025-11-25
- [ANT-17] Yuntao Bai et al., "Constitutional AI: Harmlessness from AI Feedback", Anthropic, 2022-12. https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
- [ANT-18] Anthropic Research, "Constitutional Classifiers: Defending Against Universal Jailbreaks", 2025-02. https://www.anthropic.com/research/constitutional-classifiers
- [ANT-19] Anthropic, "Anthropic's Responsible Scaling Policy". https://www.anthropic.com/responsible-scaling-policy
- [LC-01] Harrison Chase, "Agent Frameworks, Runtimes, and Harnesses - oh my!", LangChain Blog, 2025-11-04. https://blog.langchain.com/agent-frameworks-runtimes-and-harnesses-oh-my/
- [LC-02] Harrison Chase, "Deep Agents", LangChain Blog, 2025-07-30. https://blog.langchain.com/deep-agents/
- [LC-03] LangChain Team, "Doubling Down on DeepAgents", LangChain Blog, 2025-10-28. https://blog.langchain.com/doubling-down-on-deepagents/
- [LC-04] Chester Curme, Mason Daugherty, "Context Management for Deep Agents", LangChain Blog, 2026-01-28. https://blog.langchain.com/context-management-for-deepagents/
- [LC-08] LangChain Accounts, "Improving Deep Agents with Harness Engineering", LangChain Blog, 2026-02-17. https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- [LC-09] Sydney Runkle, Vivek Trivedy, "Building Multi-Agent Applications with Deep Agents", LangChain Blog, 2026-01-21. https://blog.langchain.com/building-multi-agent-applications-with-deep-agents/
- [LC-14] LangChain Accounts, "On Agent Frameworks and Agent Observability", LangChain Blog, 2026-02-12. https://blog.langchain.com/on-agent-frameworks-and-agent-observability/
- [LC-15] Lance Martin, "Using skills with Deep Agents", LangChain Blog, 2025-11-25. https://blog.langchain.com/using-skills-with-deep-agents/
- [ACD-08] (Various), "Agentic AI Frameworks: Architectures, Protocols, and Design Challenges", arXiv:2508.10146, 2025-08-13. https://arxiv.org/abs/2508.10146
- [BLG-02] Aakash Gupta, "2025 Was Agents. 2026 Is Agent Harnesses.", 2026-01-07. https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e
- [BLG-06] Hugo Bowne-Anderson, "AI Agent Harness, 3 Principles for Context Engineering", 2025-12-12. https://hugobowne.substack.com/p/ai-agent-harness-3-principles-for
- [BLG-11] Dexter Horthy, "12 Factor Agents", HumanLayer, 2025-04. https://www.humanlayer.dev/12-factor-agents
- [PLT-01] Salesforce, "What Is an Agent Harness?", 2026-01. https://www.salesforce.com/agentforce/ai-agents/agent-harness/
- [PLT-02] Salesforce Architects, "Agentic Patterns and Implementation with Agentforce", 2025. https://architect.salesforce.com/fundamentals/agentic-patterns
- [PLT-03] Google, "Agent Development Kit", 2025-04-09. https://google.github.io/adk-docs/get-started/about/
- [PLT-04] CrewAI, "Introduction to CrewAI", 2025. https://docs.crewai.com/en/introduction
- [PLT-05] Vercel, "AI SDK 6", 2025-12-22. https://vercel.com/blog/ai-sdk-6
- [PLT-06] Microsoft, "Introduction to Microsoft Agent Framework", 2025-10-01. https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
- [STD-01] Linux Foundation / OpenAI / Anthropic / Block, "Agentic AI Foundation (AAIF)", 2025-12-09. https://aaif.io/
- [STD-02] "AGENTS.md Specification". https://agents.md/
- [STD-03] "Model Context Protocol (MCP)". https://modelcontextprotocol.io/
- [TLDV-01] LangChain Community VIPs: Call with Harrison Chase and OSS Team, 2025-12-09. (非公開コミュニティコール)
- [TLDV-02] LangChain Community VIPs: Call with OSS and LangSmith Teams, 2025-10-02. (非公開コミュニティコール)
