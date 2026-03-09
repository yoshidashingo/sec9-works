# 参照文献リスト: Harness Engineering 書籍

**最終更新**: 2026-02-22
**収録文献数**: 101件
**重要度凡例**: ★★★ 必読 / ★★ 推奨 / ★ 参考

---

## I. 一次ソース: OpenAI

### OAI-01. Harness engineering: leveraging Codex in an agent-first world
- **著者**: Ryan Lopopolo (Member of Technical Staff, OpenAI)
- **公開日**: 2026-02-11
- **URL**: https://openai.com/index/harness-engineering/
- **概要**: OpenAIチームが5ヶ月間、手書きコードゼロで約100万行・1,500 PRのソフトウェア製品を構築した実験を報告。エンジニアの役割が「コードを書く」から「環境設計・意図の明確化・フィードバックループの構築」へ変化したことを実証。Harness Engineeringという用語を広く普及させた記事。
- **重要度**: ★★★
- **関連章**: 第1章, 第3章, 第8章

### OAI-02. Unlocking the Codex harness: how we built the App Server
- **著者**: OpenAI Team
- **公開日**: 2026-02-04
- **URL**: https://openai.com/index/unlocking-the-codex-harness/
- **概要**: Codex App Server（JSON-RPCプロトコルベースの双方向API）の技術アーキテクチャを解説。JetBrains、Xcode、デスクトップアプリなど複数のクライアントに統一ハーネス層を提供する設計思想。
- **重要度**: ★★
- **関連章**: 第3章, 第5章

### OAI-03. Unrolling the Codex agent loop
- **著者**: Michael Bolin (Member of Technical Staff, OpenAI)
- **公開日**: 2026-01 (推定)
- **URL**: https://openai.com/index/unrolling-the-codex-agent-loop/
- **概要**: Codex CLIのコアエージェントループのロジックを詳解。ユーザー・モデル・ツール間のインタラクション管理、状態遷移、ツール呼び出しの内部アーキテクチャ。
- **重要度**: ★★
- **関連章**: 第3章, 第5章

### OAI-04. Inside OpenAI's in-house data agent
- **著者**: OpenAI
- **公開日**: 2026-01-29
- **URL**: https://openai.com/index/inside-our-in-house-data-agent/
- **概要**: OpenAI社内のデータ分析エージェントの構築事例。AIが信頼できるチームメートとしてデータ業務に統合された実例。
- **重要度**: ★
- **関連章**: 第8章

### OAI-05. Building more with GPT-5.1-Codex-Max
- **著者**: OpenAI
- **公開日**: 2025-12-18
- **URL**: https://openai.com/index/gpt-5-1-codex-max/
- **概要**: GPT-5.1-Codex-Max の紹介。コンパクション（複数コンテキストウィンドウにまたがる作業をネイティブにサポートする機能）を初搭載。プロジェクト規模のリファクタ、深いデバッグセッション、複数時間のエージェントループを実現。
- **重要度**: ★★
- **関連章**: 第5章

### OAI-06. OpenAI co-founds the Agentic AI Foundation
- **著者**: OpenAI / Linux Foundation
- **公開日**: 2025-12-09
- **URL**: https://openai.com/index/agentic-ai-foundation/
- **概要**: Linux Foundation傘下のAgentic AI Foundation (AAIF) の設立。AGENTS.md (OpenAI), MCP (Anthropic), goose (Block) が設立プロジェクトとして寄贈。60,000以上のOSSプロジェクトが採用。
- **重要度**: ★★★
- **関連章**: 第4章, 第9章

### OAI-07. Introducing upgrades to Codex
- **著者**: OpenAI
- **公開日**: 2025-09 (GPT-5-Codex更新: 2025-09-23)
- **URL**: https://openai.com/index/introducing-upgrades-to-codex/
- **概要**: Codexへのアップグレードと GPT-5-Codex のAPI提供開始を発表。
- **重要度**: ★
- **関連章**: 第5章

### OAI-08. Introducing AgentKit
- **著者**: OpenAI
- **公開日**: 2025-10-06
- **URL**: https://openai.com/index/introducing-agentkit/
- **概要**: OpenAI DevDay 2025で発表されたAgentKit。AIエージェント構築のためのツールキット。
- **重要度**: ★
- **関連章**: 第5章

### OAI-09. Custom instructions with AGENTS.md
- **著者**: OpenAI Developers
- **URL**: https://developers.openai.com/codex/guides/agents-md/
- **概要**: AGENTS.mdの仕様と使い方。リポジトリローカルなエージェント指示ファイルの設計パターン。プロジェクト概要、ビルド・テストコマンド、コードスタイル等の推奨セクション。
- **重要度**: ★★★
- **関連章**: 第4章

### OAI-10. A Practical Guide to Building Agents (PDF)
- **著者**: OpenAI
- **公開日**: 2025-04 (推定)
- **URL**: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **概要**: 34ページのエージェント構築実践ガイド。Model, Tools, Instructionsの3コア要素。設計パターン、マルチエージェント、ガードレールをカバー。
- **重要度**: ★★
- **関連章**: 第3章, 第4章

### OAI-11. OpenAI Agents SDK
- **著者**: OpenAI
- **公開日**: 2025-03-11
- **URL**: https://openai.github.io/openai-agents-python/
- **GitHub**: https://github.com/openai/openai-agents-python
- **概要**: Swarmプロジェクトから進化した軽量Pythonフレームワーク。Agents, Handoffs, Guardrails, Runnerの4つのプリミティブ。組み込みトレーシング機能。
- **重要度**: ★★
- **関連章**: 第5章

---

## II. 一次ソース: Anthropic

### ANT-01. Effective harnesses for long-running agents
- **著者**: Justin Young (Anthropic Engineering)
- **公開日**: 2025-11-26
- **URL**: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **概要**: 複数コンテキストウィンドウにまたがる長期実行エージェントのハーネス設計。Initializer Agent + Coding Agentの2エージェントアーキテクチャ。claude-progress.txtによる状態ブリッジング、4つの失敗パターンと対策。
- **重要度**: ★★★
- **関連章**: 第3章, 第6章

### ANT-02. Building Effective Agents
- **著者**: Erik Schluntz, Barry Zhang
- **公開日**: 2024-12-19
- **URL**: https://www.anthropic.com/research/building-effective-agents
- **概要**: AIエージェント構築の標準的ガイド。プロンプトチェーン、ルーティング、並列化、オーケストレーター・ワーカー等のデザインパターン。「シンプルに始め、必要な場合のみ複雑化する」原則。
- **重要度**: ★★★
- **関連章**: 第3章

### ANT-03. Effective Context Engineering for AI Agents
- **著者**: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield
- **公開日**: 2025-09-29
- **URL**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **概要**: コンテキストエンジニアリングをプロンプトエンジニアリングと区別して定義。コンテキストロット（コンテキスト増大による性能劣化）の概念。システムプロンプト調整、トークン効率的ツール設計、ランタイム検索、コンパクション等の実践戦略。
- **重要度**: ★★★
- **関連章**: 第2章, 第6章

### ANT-04. Writing Effective Tools for AI Agents -- Using AI Agents
- **著者**: Anthropic Engineering
- **公開日**: 2025-09-11
- **URL**: https://www.anthropic.com/engineering/writing-tools-for-agents
- **概要**: MCPによる大量ツール活用。ツールを決定論的システムと非決定論的エージェント間の新しいソフトウェア契約として定義。
- **重要度**: ★★
- **関連章**: 第5章

### ANT-05. The "Think" Tool
- **著者**: Anthropic Engineering
- **公開日**: 2025-03-20
- **URL**: https://www.anthropic.com/engineering/claude-think-tool
- **概要**: 複雑なマルチステップタスク中の構造化推論のための「think」ツール。航空会社カスタマーサービスで54%の相対的改善。ポリシー重視環境での推奨。
- **重要度**: ★★
- **関連章**: 第3章

### ANT-06. How We Built Our Multi-Agent Research System
- **著者**: Anthropic Engineering
- **公開日**: 2025-06-13
- **URL**: https://www.anthropic.com/engineering/multi-agent-research-system
- **概要**: オーケストレーター・ワーカー型マルチエージェントパターン。リードエージェントが戦略立案し、並列サブエージェントを生成。
- **重要度**: ★★
- **関連章**: 第3章, 第6章

### ANT-07. Beyond Permission Prompts: Making Claude Code More Secure and Autonomous
- **著者**: Anthropic Engineering
- **公開日**: 2025-10-20
- **URL**: https://www.anthropic.com/engineering/claude-code-sandboxing
- **概要**: Claude Codeのサンドボックス手法（Linux bubblewrap, macOS seatbelt）。許可プロンプト84%削減。ファイルシステム分離とネットワーク分離の2層境界。
- **重要度**: ★★
- **関連章**: 第4章, 第7章

### ANT-08. Code Execution with MCP: Building More Efficient Agents
- **著者**: Anthropic Engineering
- **公開日**: 2025-11-04
- **URL**: https://www.anthropic.com/engineering/code-execution-with-mcp
- **概要**: コード実行によるMCPツール呼び出しの効率化。トークン85%削減（約134kから約5k）。オンデマンドツールロード。
- **重要度**: ★★
- **関連章**: 第5章

### ANT-09. Introducing Advanced Tool Use
- **著者**: Anthropic Engineering
- **公開日**: 2025-11-24
- **URL**: https://www.anthropic.com/engineering/advanced-tool-use
- **概要**: Tool Search and Discovery、Programmatic Tool Calling、Learning from Examplesの3機能。単純な関数呼び出しからインテリジェントなオーケストレーションへの進化。
- **重要度**: ★★
- **関連章**: 第5章

### ANT-10. Equipping Agents for the Real World with Agent Skills
- **著者**: Barry Zhang, Keith Lazuka, Mahesh Murag
- **公開日**: 2025-10-16
- **URL**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- **概要**: Agent Skills: SKILL.mdファイルによる動的発見・ロード。プログレッシブ・ディスクロージャーの設計原則。汎用エージェントから特化エージェントへの変換。
- **重要度**: ★★
- **関連章**: 第4章

### ANT-11. Demystifying Evals for AI Agents
- **著者**: Anthropic Engineering
- **公開日**: 2026-01-09
- **URL**: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- **概要**: エージェント評価の階層的アプローチ: 自動eval、本番モニタリング、A/Bテスト、ユーザーフィードバック。20-50の実際の失敗から始める推奨。
- **重要度**: ★★
- **関連章**: 第7章

### ANT-12. Building a C Compiler with a Team of Parallel Claudes
- **著者**: Nicholas Carlini (Anthropic Safeguards)
- **公開日**: 2026-02-05
- **URL**: https://www.anthropic.com/engineering/building-c-compiler
- **概要**: 16並列Opus 4.6インスタンスで10万行のRustベースCコンパイラを構築。約2,000セッション、$20,000のAPIコスト。並列性によるエージェント特化の実証。
- **重要度**: ★★
- **関連章**: 第6章, 第8章

### ANT-13. Claude Code: Best Practices for Agentic Coding
- **著者**: Anthropic Engineering
- **公開日**: 2025-04-18
- **URL**: https://www.anthropic.com/engineering/claude-code-best-practices
- **概要**: TDD、コードベース探索、git操作、MCP設定、CLAUDE.mdファイル活用等のベストプラクティス。
- **重要度**: ★★★
- **関連章**: 第4章, 第8章

### ANT-14. Building Agents with the Claude Agent SDK
- **著者**: Anthropic
- **公開日**: 2025-09-29
- **URL**: https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk
- **概要**: Claude Code SDKからClaude Agent SDKへの改名。コーディング以外のエージェント構築への拡張。コンテキスト管理、権限モデル、セッション管理、MCP統合。
- **重要度**: ★★
- **関連章**: 第5章

### ANT-15. Introducing the Model Context Protocol
- **著者**: Anthropic
- **公開日**: 2024-11-25
- **URL**: https://www.anthropic.com/news/model-context-protocol
- **概要**: MCPのオープンソース公開。AIアシスタントとデータソース、ビジネスツール、開発環境を接続する標準プロトコル。
- **重要度**: ★★★
- **関連章**: 第5章

### ANT-16. MCP Specification (2025-11-25)
- **著者**: MCP Community / Anthropic
- **URL**: https://modelcontextprotocol.io/specification/2025-11-25
- **概要**: MCPの公式仕様。JSON-RPCベースのクライアントサーバー通信、ライフサイクル管理、コアプリミティブ（ツール、リソース、プロンプト）。
- **重要度**: ★★
- **関連章**: 第5章

### ANT-17. Constitutional AI: Harmlessness from AI Feedback
- **著者**: Yuntao Bai et al.
- **公開日**: 2022-12
- **URL**: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
- **概要**: Constitutional AI (CAI) の基礎論文。自己批判と修正による教師あり学習 + RLAIF。ガードレール思想の理論的基盤。
- **重要度**: ★★
- **関連章**: 第4章

### ANT-18. Constitutional Classifiers: Defending Against Universal Jailbreaks
- **著者**: Anthropic Research
- **公開日**: 2025-02
- **URL**: https://www.anthropic.com/research/constitutional-classifiers
- **概要**: 自然言語ルール「憲法」から合成データで訓練されたセーフガード。ジェイルブレイク成功率を4.4%に低減。
- **重要度**: ★★
- **関連章**: 第4章

### ANT-19. Anthropic's Responsible Scaling Policy
- **著者**: Anthropic
- **公開日**: v1.0: 2023-09-19, v2.0: 2024-10-15, v2.2: 2025-05-14
- **URL**: https://www.anthropic.com/responsible-scaling-policy
- **概要**: AI Safety Level Standards (ASL-1〜ASL-3+)。バイオセーフティレベルに着想を得た、能力に比例した保護のフレームワーク。
- **重要度**: ★
- **関連章**: 第4章

### ANT-20. 2026 Agentic Coding Trends Report
- **著者**: Anthropic
- **公開日**: 2026
- **URL**: https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf
- **概要**: コーディングエージェントがソフトウェア開発をどう変えているかのトレンドレポート。
- **重要度**: ★
- **関連章**: 第8章

---

## III. 一次ソース: LangChain / LangGraph / DeepAgents

### LC-01. Agent Frameworks, Runtimes, and Harnesses - oh my!
- **著者**: Harrison Chase
- **公開日**: 2025-11-04
- **URL**: https://blog.langchain.com/agent-frameworks-runtimes-and-harnesses-oh-my/
- **概要**: エージェントスタック3層分類（Framework / Runtime / Harness）の標準定義。LangChain=Framework, LangGraph=Runtime, DeepAgents=Harness。ハーネスはフレームワークより高水準で、「バッテリー込み」の思想。
- **重要度**: ★★★
- **関連章**: 第1章, 第3章

### LC-02. Deep Agents
- **著者**: Harrison Chase
- **公開日**: 2025-07-30
- **URL**: https://blog.langchain.com/deep-agents/
- **概要**: DeepAgentsの初期発表。単純なツール呼び出しループは「浅い」エージェントにしかならないと主張。計画ツール、サブエージェント、ファイルシステムアクセス、詳細プロンプトの4機能。
- **重要度**: ★★
- **関連章**: 第3章, 第5章

### LC-03. Doubling Down on DeepAgents
- **著者**: LangChain Team
- **公開日**: 2025-10-28
- **URL**: https://blog.langchain.com/doubling-down-on-deepagents/
- **概要**: DeepAgents v0.2。プラガブルBackend抽象化（LangGraph State, LangGraph Store, ローカルファイルシステム）。大規模ツール結果のエビクション、会話履歴要約。
- **重要度**: ★★
- **関連章**: 第5章

### LC-04. Context Management for Deep Agents
- **著者**: Chester Curme, Mason Daugherty
- **公開日**: 2026-01-28
- **URL**: https://blog.langchain.com/context-management-for-deepagents/
- **概要**: 長期実行エージェントのコンテキストロット対策。max_input_tokensの85%で自動発動する3つの圧縮技術。
- **重要度**: ★★
- **関連章**: 第6章

### LC-05. State of Agent Engineering
- **著者**: LangChain
- **公開日**: 2026-01 (調査: 2025-11〜12, 回答者1,340名)
- **URL**: https://www.langchain.com/state-of-agent-engineering
- **概要**: 業界調査レポート。57.3%がエージェントを本番運用中。89%がオブザーバビリティを実装。モデル選択、アーキテクチャパターン、評価手法のデータ。
- **重要度**: ★★★
- **関連章**: 第1章, 第7章, 第8章

### LC-06. The rise of "context engineering"
- **著者**: LangChain
- **公開日**: 2025-06
- **URL**: https://blog.langchain.com/the-rise-of-context-engineering/
- **概要**: コンテキストエンジニアリングが正式な専門分野として台頭した経緯。Dex Horthy氏の2025年4月の命名から急成長。
- **重要度**: ★★
- **関連章**: 第2章

### LC-07. Not Another Workflow Builder
- **著者**: Harrison Chase
- **公開日**: 2025-10-10
- **URL**: https://blog.langchain.com/not-another-workflow-builder/
- **概要**: ビジュアルワークフロービルダーに対するコードファーストのハーネスアプローチの優位性を主張。
- **重要度**: ★
- **関連章**: 第8章

### LC-08. Improving Deep Agents with Harness Engineering
- **著者**: LangChain Accounts
- **公開日**: 2026-02-17
- **URL**: https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- **概要**: モデル（GPT-5.2-Codex）を一切変更せず、ハーネスの最適化のみでTerminal Bench 2.0スコアを52.8から66.5へ13.7ポイント向上（Top 30→Top 5）。3つの最適化領域: Build & Self-Verification Loop、Environmental Context Delivery、Reasoning Compute Allocation。「推論サンドイッチ」パターン（計画: extra-high → 実装: high → 検証: extra-high）。LoopDetectionMiddleware、PreCompletionChecklistMiddleware。
- **重要度**: ★★★
- **関連章**: 第3章, 第6章, 第7章

### LC-09. Building Multi-Agent Applications with Deep Agents
- **著者**: Sydney Runkle, Vivek Trivedy
- **公開日**: 2026-01-21（最終更新: 2026-02-13）
- **URL**: https://blog.langchain.com/building-multi-agent-applications-with-deep-agents/
- **概要**: Deep Agentsフレームワークの2プリミティブ: Subagents（コンテキスト肥大化対策としての作業委譲）とSkills（SKILL.mdによる段階的能力開示）。両パターンの選択ガイドラインと組み合わせ手法。
- **重要度**: ★★
- **関連章**: 第3章, 第6章

### LC-10. Evaluating Deep Agents: Our Learnings
- **著者**: LangChain Accounts
- **公開日**: 2025-12-03
- **URL**: https://blog.langchain.com/evaluating-deep-agents-our-learnings/
- **概要**: Deep Agents評価の5パターン: (1) データポイントごとのカスタムテストロジック、(2) シングルステップ評価、(3) 完全なエージェントターン（Trajectory/Final Response/Other State）、(4) マルチターン会話、(5) 環境セットアップ（Dockerサンドボックス）。4アプリケーション（DeepAgents CLI、LangSmith Assist等）での実践知見。
- **重要度**: ★★
- **関連章**: 第7章

### LC-11. Context Engineering for Agents
- **著者**: LangChain Accounts
- **公開日**: 2025-07-02（最終更新: 2025-10-19）
- **URL**: https://blog.langchain.com/context-engineering-for-agents/
- **概要**: コンテキストエンジニアリングの4つの操作戦略: Write（外部永続化）、Select（必要時取得）、Compress（要約・トリミング）、Isolate（コンテキスト分離）。OSメタファー（LLM=CPU、コンテキストウィンドウ=RAM）。コンテキスト失敗モード: Context Poisoning, Distraction, Confusion, Clash。
- **重要度**: ★★★
- **関連章**: 第2章, 第3章, 第6章

### LC-12. How agents can use filesystems for context engineering
- **著者**: Nick Huang
- **公開日**: 2025-11-21
- **URL**: https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/
- **概要**: ファイルシステムを「エージェントがコンテキストを柔軟に保存・取得・更新できる単一インターフェース」として活用。4つの課題（トークンオーバーフロー、ウィンドウ不足、不正確な検索、静的知識ギャップ）とファイルシステムによる解決策。
- **重要度**: ★★
- **関連章**: 第3章, 第6章

### LC-13. Agent Engineering: A New Discipline
- **著者**: LangChain
- **公開日**: 2025-12-09
- **URL**: https://blog.langchain.com/agent-engineering-a-new-discipline/
- **概要**: エージェントエンジニアリングを「非決定論的なLLMシステムを信頼性の高い本番体験へと洗練させる反復的プロセス」と定義。3つの必須スキルセット: Product thinking、Engineering、Data science。build→test→ship→observe→refineサイクル。
- **重要度**: ★★
- **関連章**: 第1章, 第8章

### LC-14. On Agent Frameworks and Agent Observability
- **著者**: LangChain Accounts
- **公開日**: 2026-02-12
- **URL**: https://blog.langchain.com/on-agent-frameworks-and-agent-observability/
- **概要**: フレームワーク3世代: Chaining（2023）→ LangGraph（2024）→ DeepAgents（2025）。「Agent frameworks are still useful, but only if they evolve as fast as the models do」。フレームワーク非依存のオブザーバビリティ。OpenTelemetryベースのトレーシング。
- **重要度**: ★★
- **関連章**: 第3章, 第5章, 第7章

### LC-15. Using skills with Deep Agents
- **著者**: Lance Martin
- **公開日**: 2025-11-25
- **URL**: https://blog.langchain.com/using-skills-with-deep-agents/
- **概要**: SKILL.mdによるプログレッシブ・ディスクロージャー。デフォルトではYAML前置きのみロード、必要時に完全なSKILL.md読み込み。トークン効率性と認知負荷の低減。汎用エージェント（Claude Code約12ツール、Manus20未満）の効率性の背景。
- **重要度**: ★★
- **関連章**: 第4章, 第5章

### LC-16. Evaluating DeepAgents CLI on Terminal Bench 2.0
- **著者**: Vivek Trivedy, Eugene Yurtsev
- **公開日**: 2025-12-05
- **URL**: https://blog.langchain.com/evaluating-deepagents-cli-on-terminal-bench-2-0/
- **概要**: Terminal Bench 2.0（89タスク、ソフトウェアエンジニアリング・バイオロジー・セキュリティ・ゲーミング）でClaude Sonnet 4.5使用時に平均42.65%を達成し「Claude Code自体と同等」。Harborフレームワークによるコンテナ化エージェント評価。
- **重要度**: ★★
- **関連章**: 第7章

### LC-17. Introducing Open SWE: An Open-Source Asynchronous Coding Agent
- **著者**: LangChain Accounts
- **公開日**: 2025-08-06（最終更新: 2026-01-15）
- **URL**: https://blog.langchain.com/introducing-open-swe-an-open-source-asynchronous-coding-agent/
- **概要**: 3段階エージェント構造: Manager（ユーザーインタラクション）→ Planner（詳細計画）→ Programmer & Reviewer（サンドボックス実行・QA）。LangGraph Platform上で長時間実行対応。Human-in-the-Loopの計画段階統合。
- **重要度**: ★★
- **関連章**: 第6章, 第8章

### LC-18. Debugging Deep Agents with LangSmith
- **著者**: LangChain Accounts
- **公開日**: 2025-12-10
- **URL**: https://blog.langchain.com/debugging-deep-agents-with-langsmith/
- **概要**: Deep Agentsのデバッグ課題（長大プロンプト、長い実行トレース、マルチターン会話）と解決策。LangSmith Polly: AI支援トレース分析。LangSmith Fetch CLI: コーディングエージェントからの直接トレースアクセス。
- **重要度**: ★★
- **関連章**: 第7章

---

## IV. 一次ソース: その他プラットフォーム

### PLT-01. What Is an Agent Harness? (Salesforce)
- **著者**: Salesforce
- **公開日**: 2026-01 (推定)
- **URL**: https://www.salesforce.com/agentforce/ai-agents/agent-harness/
- **概要**: エージェントハーネスを「エージェントの実行、状態、信頼性を管理するランタイム環境とインフラストラクチャ」と定義。モデルスワップ可能な設計。
- **重要度**: ★★
- **関連章**: 第3章, 第5章

### PLT-02. Agentic Patterns and Implementation with Agentforce (Salesforce)
- **著者**: Salesforce Architects
- **公開日**: 2025
- **URL**: https://architect.salesforce.com/fundamentals/agentic-patterns
- **概要**: 5つのエージェントタイプ（会話型, プロアクティブ, アンビエント, 自律型, 協調型）のアーキテクチャパターン。
- **重要度**: ★
- **関連章**: 第5章

### PLT-03. Agent Development Kit (Google)
- **著者**: Google
- **公開日**: 2025-04-09 (v1.0: 2025-05-22)
- **URL**: https://google.github.io/adk-docs/get-started/about/
- **概要**: Gemini最適化のオープンソースフレームワーク。マルチエージェント設計、双方向オーディオ・ビデオストリーミング。
- **重要度**: ★★
- **関連章**: 第5章

### PLT-04. Introduction to CrewAI
- **著者**: CrewAI
- **公開日**: 2025
- **URL**: https://docs.crewai.com/en/introduction
- **概要**: ロールベースアーキテクチャ（Agent, Task, Crew, Flow）。Flow/Crewデュアルアーキテクチャ: Flowsが決定論的オーケストレーター、Crewsが自律協調チーム。
- **重要度**: ★★
- **関連章**: 第5章

### PLT-05. AI SDK 6 (Vercel)
- **著者**: Vercel
- **公開日**: 2025-12-22
- **URL**: https://vercel.com/blog/ai-sdk-6
- **概要**: エージェントをファーストクラス抽象として導入。Agent interface、ツール実行承認パターン、MCP対応。TypeScript中心。
- **重要度**: ★
- **関連章**: 第5章

### PLT-06. Introduction to Microsoft Agent Framework
- **著者**: Microsoft
- **公開日**: 2025-10-01 (パブリックプレビュー)
- **URL**: https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
- **概要**: AutoGenとSemantic Kernelを統合した.NET/Python対応フレームワーク。グラフベースワークフロー、MCP統合、OpenTelemetryオブザーバビリティ。
- **重要度**: ★★
- **関連章**: 第5章

---

## V. 業界記事・ブログ（英語）

### BLG-01. The importance of Agent Harness in 2026
- **著者**: Philipp Schmid (Staff Engineer, Google DeepMind)
- **公開日**: 2026-01-05
- **URL**: https://www.philschmid.de/agent-harness-2026
- **概要**: ハーネスを「AIモデルをラップして長期実行タスクを管理するインフラ」と定義。モデルパリティ問題と「持続性」（durability）の重要性。
- **重要度**: ★★★
- **関連章**: 第1章, 第3章

### BLG-02. 2025 Was Agents. 2026 Is Agent Harnesses.
- **著者**: Aakash Gupta
- **公開日**: 2026-01-07
- **URL**: https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e
- **概要**: 「モデルはコモディティ、ハーネスこそがモート」。Manusが6ヶ月で5回ハーネスを書き直した事例。
- **重要度**: ★★★
- **関連章**: 第1章

### BLG-03. AI Agents in Production: The Harness Dissected
- **著者**: Leopoldo Garcia Vargas
- **公開日**: 2025-12-16
- **URL**: https://aienhancedengineer.substack.com/p/ai-agents-in-production-the-harness
- **概要**: ハーネスの6つの標準コンポーネント: Reasoning Engine, Planning & Orchestration, Tool Registry, Memory & Context, State & Persistence, Structured I/O。モデル非依存設計。
- **重要度**: ★★★
- **関連章**: 第3章

### BLG-04. From Prompts to Harnesses (Seawolf AI)
- **著者**: Clay (Seawolf AI)
- **公開日**: 2025-12-08
- **URL**: https://www.seawolfai.net/from-prompts-to-harnesses-the-discipline-behind-long-running-intelligence/
- **概要**: 「プロンプティングは可能性を生む。ハーネスは進歩を生む。」次世代AIはハーネスで定義される。
- **重要度**: ★★
- **関連章**: 第1章, 第2章

### BLG-05. Harness Engineering and the Discipline of Long-Running Intelligence (Seawolf AI)
- **著者**: Clay (Seawolf AI)
- **URL**: https://www.seawolfai.net/harness-engineering-and-the-discipline-of-long-running-intelligence/
- **概要**: Harness Engineeringの規律としての体系化。長期実行インテリジェンスのための設計原則。
- **重要度**: ★★
- **関連章**: 第6章

### BLG-06. AI Agent Harness, 3 Principles for Context Engineering
- **著者**: Hugo Bowne-Anderson
- **公開日**: 2025-12-12
- **URL**: https://hugobowne.substack.com/p/ai-agent-harness-3-principles-for
- **概要**: 3原則: (1) 再アーキテクチャを受け入れる, (2) ビルダーにとってのより高い抽象レベル, (3) シンプルさは不可欠。Manusが5回書き直し。
- **重要度**: ★★
- **関連章**: 第3章, 第8章

### BLG-07. Agent Harnesses: From DIY Patterns to Product
- **著者**: paddo.dev
- **公開日**: 2025-11-28
- **URL**: https://paddo.dev/blog/agent-harnesses-from-diy-to-product/
- **概要**: DIYパターン（進捗ファイル、構造化機能リスト、セッション起動プロトコル）からプロダクトへの進化。
- **重要度**: ★★
- **関連章**: 第6章

### BLG-08. 'The digital harness' (World Economic Forum)
- **著者**: World Economic Forum
- **公開日**: 2026-01-21
- **URL**: https://www.weforum.org/stories/2026/01/deploying-the-digital-harness-to-scale-ai-responsibly/
- **概要**: デジタルハーネスの概念: AIの加速する能力を人間の目的と社会的価値に整合させるフレームワーク。馬具のアナロジー。
- **重要度**: ★★
- **関連章**: 第1章, 第9章

### BLG-09. Agent Frameworks vs Runtimes vs Harnesses (Analytics Vidhya)
- **著者**: Analytics Vidhya
- **公開日**: 2025-12-08
- **URL**: https://www.analyticsvidhya.com/blog/2025/12/agent-frameworks-vs-runtimes-vs-harnesses/
- **概要**: 3層スタックの包括的比較: Framework → Runtime → Harness。各層の役割と使い分け。
- **重要度**: ★★
- **関連章**: 第3章

### BLG-10. What is an agent harness? (Parallel.ai)
- **著者**: Parallel Web Systems
- **URL**: https://parallel.ai/articles/what-is-an-agent-harness
- **概要**: エージェントハーネスの定義と4コンポーネント: Memory Management, Context Management, Planning & Tool Orchestration, Human-in-the-Loop Controls。
- **重要度**: ★
- **関連章**: 第3章

### BLG-11. 12 Factor Agents
- **著者**: Dexter Horthy (HumanLayer)
- **公開日**: 2025-04
- **URL**: https://www.humanlayer.dev/12-factor-agents
- **概要**: 12 Factor Appsに着想を得た、本番対応AIエージェント構築の方法論。Harness Engineering運動に影響を与えた基礎的文献。
- **重要度**: ★★★
- **関連章**: 第2章, 第4章

### BLG-12. Context Engineering Our Way to Long-Horizon Agents (Sequoia Capital Podcast)
- **著者/ホスト**: Sonya Huang, Pat Grady (Sequoia); ゲスト: Harrison Chase (LangChain)
- **公開日**: 2026-01 (推定)
- **URL**: https://sequoiacap.com/podcast/context-engineering-our-way-to-long-horizon-agents-langchains-harrison-chase/
- **概要**: 長期ホライズンエージェントの台頭。初期スキャフォールディングからハーネスベースアーキテクチャへの進化。
- **重要度**: ★★
- **関連章**: 第2章, 第6章

---

## VI. 業界記事・ブログ（日本語）

### JP-01. ハーネスエンジニアリング - エージェントファーストの世界で Codex を活用する
- **著者**: npaka
- **公開日**: 2026-02-12
- **URL**: https://note.com/npaka/n/nb4c5488e82fd
- **概要**: OpenAI記事の日本語要約。手作業コードなしで製品を構築した実験の解説。
- **重要度**: ★★
- **関連章**: 第1章, 第3章

### JP-02. AIの戦場は「モデル」から「ハーネス」へ
- **著者**: CONTEXT
- **公開日**: 2025-11-03
- **URL**: https://note.com/getcontext/n/nbd7aa75632e7
- **概要**: モデル性能競争からハーネス（統合技術）への転換を論じる。475人のAI研究者の76%がスケールアップだけではAGIに到達しないと回答。
- **重要度**: ★★
- **関連章**: 第1章

### JP-03. AIエージェントの長距離走を可能にする「ハーネス」設計
- **著者**: piyo_feed
- **URL**: https://note.com/piyo_bird/n/nf02db013cad4
- **概要**: Anthropic「Effective harnesses for long-running agents」の日本語詳細解説。2種類の特化型エージェントによる構成。
- **重要度**: ★★
- **関連章**: 第6章

### JP-04. コンテキスト・エンジニアリングとは何か
- **著者**: 森正弥
- **公開日**: 2025-09-01
- **URL**: https://note.com/masayamori/n/n343363451ccb
- **概要**: プロンプトエンジニアリングとの違い: 「言語による問いの最適化」vs「推論に必要な全体設計の最適化」。
- **重要度**: ★★
- **関連章**: 第2章

### JP-05. コンテキスト・エンジニアリングとは何か (HCAII)
- **著者**: 博報堂DYホールディングス Human Centered AI Institute
- **URL**: https://hcaii.com/articles/0012/
- **概要**: AIエージェント開発に不可欠なコンテキストエンジニアリングの概要。ツール仕様・知識ベースのアクセス条件の体系化。
- **重要度**: ★
- **関連章**: 第2章

### JP-06. AIコードレビューにおけるコンテキストエンジニアリングの技術と実践
- **著者**: CodeRabbit
- **URL**: https://www.coderabbit.ai/ja/blog/the-art-and-science-of-context-engineering-ja
- **概要**: 意図・環境・会話の3種類のコンテキストの取り扱い。AIコードレビューにおける実践手法。
- **重要度**: ★
- **関連章**: 第2章

---

## VII. 学術論文・研究

### ACD-01. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- **著者**: Qizheng Zhang, Changran Hu, Shubhangi Upasani et al.
- **公開日**: 2025-10-06 (改訂 2026-01-29)
- **URL**: https://arxiv.org/abs/2510.04618
- **概要**: ACEフレームワーク: コンテキストを進化するプレイブックとして扱い、生成・リフレクション・キュレーションを通じて蓄積・精緻化。+10.6%の改善。
- **重要度**: ★★
- **関連章**: 第2章

### ACD-02. A Survey of Context Engineering for Large Language Models
- **著者**: Lingrui Mei, Jiayu Yao et al.
- **公開日**: 2025-07
- **URL**: https://arxiv.org/abs/2507.13334
- **概要**: コンテキストエンジニアリングを正式な学問分野として確立。Context Retrieval and Generation, Context Processing, Context Managementの3基盤コンポーネント。
- **重要度**: ★★★
- **関連章**: 第2章

### ACD-03. Context Engineering for Multi-Agent LLM Code Assistants
- **著者**: Muhammad Haseeb
- **公開日**: 2025-08-09
- **URL**: https://arxiv.org/abs/2508.08322
- **概要**: マルチエージェントLLMコードアシスタントのためのコンテキストエンジニアリング手法。意図明確化、セマンティック文献検索、ドキュメント合成、マルチエージェントコード生成の統合。
- **重要度**: ★
- **関連章**: 第2章, 第6章

### ACD-04. Agentic AI: Architectures, Taxonomies, and Evaluation
- **著者**: Arunkumar V, Gangadharan G.R., Rajkumar Buyya
- **公開日**: 2026-01-08
- **URL**: https://arxiv.org/abs/2601.12560
- **概要**: CLASSic次元（Cost, Latency, Accuracy, Security, Stability）によるエージェンティックAIの評価。アーキテクチャ選択と具体的障害モードの対応付け。
- **重要度**: ★★
- **関連章**: 第3章, 第7章

### ACD-05. A Practical Guide for Designing, Developing, and Deploying Production-Grade Agentic AI Workflows
- **著者**: Eranga Bandara, Ross Gore et al.
- **公開日**: 2025-12
- **URL**: https://arxiv.org/abs/2512.08769
- **概要**: 本番グレードのエージェンティックAIワークフローの設計・開発・デプロイの実践ガイド。
- **重要度**: ★★
- **関連章**: 第7章, 第8章

### ACD-06. Measuring Agents in Production
- **著者**: Melissa Z. Pan et al.
- **公開日**: 2025-12-02 (改訂 2026-02-03)
- **URL**: https://arxiv.org/abs/2512.04123
- **概要**: 本番AIエージェントの95%が失敗。68%が最大10ステップで人間介入を必要。検証・ガードレール・スケーラブルメモリ・解釈可能性が重要領域。
- **重要度**: ★★★
- **関連章**: 第7章

### ACD-07. Building a Foundational Guardrail for General Agentic Systems via Synthetic Data
- **著者**: (Various)
- **公開日**: 2025-10-10
- **URL**: https://arxiv.org/abs/2510.09781
- **概要**: 合成データによるガードレールシステムの訓練。エージェント計画を実行前段階で予測的に分析する外部モニター。
- **重要度**: ★★
- **関連章**: 第4章

### ACD-08. Agentic AI Frameworks: Architectures, Protocols, and Design Challenges
- **著者**: (Various)
- **公開日**: 2025-08-13
- **URL**: https://arxiv.org/abs/2508.10146
- **概要**: 主要エージェントフレームワーク（CrewAI, LangGraph, AutoGen等）のシステマティックレビュー。安全ガードレールとサービス指向パラダイムの評価。
- **重要度**: ★★
- **関連章**: 第5章

### ACD-09. The AI Agent Code of Conduct: Automated Guardrail Policy-as-Prompt Synthesis
- **著者**: (Various)
- **公開日**: 2025-09
- **URL**: (arXiv)
- **概要**: 自然言語ポリシー文書を動的で強制可能なガードレールに変換するフレームワーク。プロンプトベースの分類器でランタイム時に最小権限ポリシーを強制。
- **重要度**: ★★
- **関連章**: 第4章

### ACD-10. A Comprehensive Survey of Self-Evolving AI Agents
- **著者**: (Various)
- **公開日**: 2025-08
- **URL**: https://arxiv.org/abs/2508.07407
- **概要**: 基盤モデルと生涯エージェンティックシステムを橋渡しする自己進化型エージェントのパラダイム。インタラクションデータと環境フィードバックに基づく自動強化。
- **重要度**: ★
- **関連章**: 第6章

---

## VIII. 関連書籍（英語）

### BK-01. AI Engineering: Building Applications with Foundation Models
- **著者**: Chip Huyen
- **出版社**: O'Reilly Media
- **公開日**: 2025-01-07
- **ISBN**: 978-1098166304
- **概要**: ファンデーションモデルを用いたアプリケーション構築の包括的ガイド。532ページ。Amazon 4.7, Goodreads 4.46。
- **重要度**: ★★
- **関連章**: 第2章, 第3章

### BK-02. Prompt Engineering for LLMs
- **著者**: John Berryman, Albert Ziegler
- **出版社**: O'Reilly Media
- **公開日**: 2024-11
- **ISBN**: 978-1098156152
- **概要**: LLMとの効果的なコミュニケーション技術。プロンプト設計の理論と実践。
- **重要度**: ★★
- **関連章**: 第2章

### BK-03. Building Applications with AI Agents
- **著者**: Michael Albada
- **出版社**: O'Reilly Media
- **公開日**: 2025-10-21
- **ISBN**: 978-1098176501
- **概要**: マルチエージェントシステムの設計と実装の実践ガイド。
- **重要度**: ★★
- **関連章**: 第3章, 第5章

### BK-04. AI Agents in Action
- **著者**: Micheal Lanham
- **出版社**: Manning Publications
- **公開日**: 2025-03-25 (第2版: 2026年夏予定)
- **ISBN**: 978-1633436343
- **概要**: AIエージェントの設計・実装・デプロイの包括的ガイド。
- **重要度**: ★★
- **関連章**: 第3章

### BK-05. Build a Large Language Model (From Scratch)
- **著者**: Sebastian Raschka
- **出版社**: Manning Publications
- **公開日**: 2024
- **ISBN**: 978-1633437166
- **概要**: PyTorchでLLMをゼロから実装するステップバイステップガイド。LLM内部構造の理解に有用。
- **重要度**: ★
- **関連章**: 第2章

---

## IX. 関連書籍（日本語）

### JBK-01. やさしく学ぶLLMエージェント
- **著者**: 井上顧基、下垣内隆太、松山純大、成木太音
- **出版社**: オーム社
- **公開日**: 2025-02-15
- **ISBN**: 978-4-274-23316-6
- **概要**: LLMエージェントの基本からマルチエージェントシステムの設計まで。306ページ。
- **重要度**: ★★
- **関連章**: 第3章

### JBK-02. AIエージェント開発／運用入門
- **著者**: 御田稔、大坪悠、塚田真規
- **出版社**: SBクリエイティブ
- **公開日**: 2025-10-01
- **ISBN**: 978-4-8156-3660-9
- **概要**: AIエージェントの基礎から開発・運用フェーズまで。実践的なノウハウの体系化。
- **重要度**: ★★
- **関連章**: 第3章, 第7章

### JBK-03. いちばんやさしいAIエージェントの教本
- **著者**: 古川渉一
- **出版社**: インプレス
- **公開日**: 2025-08-26
- **ISBN**: 978-4-295-02192-6
- **概要**: AIエージェントの仕組みや先行ビジネスモデルの入門書。
- **重要度**: ★
- **関連章**: 第3章

### JBK-04. Azure OpenAIエージェント・RAG 構築実践ガイド
- **著者**: アバナード株式会社、菅原允ほか
- **出版社**: 日経BP
- **公開日**: 2025-10-04
- **概要**: Microsoft Agentic World構想とAzure OpenAIサービスを基盤とした実践的構築方法。
- **重要度**: ★
- **関連章**: 第5章

---

## X. 標準化・ガバナンス

### STD-01. Agentic AI Foundation (AAIF)
- **著者**: Linux Foundation / OpenAI / Anthropic / Block
- **公開日**: 2025-12-09
- **URL**: https://aaif.io/
- **概要**: MCP, AGENTS.md, gooseを設立プロジェクトとするオープン標準化団体。プラチナメンバー: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI。
- **重要度**: ★★★
- **関連章**: 第9章

### STD-02. AGENTS.md Specification
- **URL**: https://agents.md/
- **概要**: AIコーディングエージェントのためのオープンフォーマット。60,000以上のOSSプロジェクトが採用。Codex, Cursor, Devin, GitHub Copilot等がサポート。
- **重要度**: ★★★
- **関連章**: 第4章

### STD-03. Model Context Protocol (MCP)
- **URL**: https://modelcontextprotocol.io/
- **概要**: AIアプリケーションの「USB-C」。外部データソースやツールへの標準化された接続方法。
- **重要度**: ★★★
- **関連章**: 第5章

---

---

## XI. 社内ミーティング議事録・VIPコール（TLDV）

### TLDV-01. LangChain Community VIPs: Call with Harrison and OSS Team
- **日時**: 2025-12-09
- **参加者**: Harrison Chase (LangChain CEO), 著者ほか
- **概要**: Harrison Chaseが「Agent Harness」を3層構造（Framework → Runtime → Harness）の最上位として直接定義。「deep agents, we think of as like an agent harness」と発言。Deep Agentsの4つの組み込み機能（planning tools, sub-agents, file system access, automatic summarization/compaction）を具体的に説明。ARC-AGIベンチマークでハーネスを活用した事例。Deep Agents時代の評価の変化（2,000行プロンプト、100+ツールコール）。
- **重要度**: ★★★
- **関連章**: 第1章, 第3章, 第5章, 第7章

### TLDV-02. LangChain Community VIPs: Call with OSS and LangSmith Teams
- **日時**: 2025-10-02
- **参加者**: Sydney Runkle (LangChain), Chester, Mason, Eugene, 著者ほか
- **概要**: Middleware概念とContext Engineeringの関係を解説。modify model requestフックがcontext engineeringの中核。変更可能項目: モデル、ツール、システムプロンプト、メッセージ履歴、モデル設定。プリビルトmiddlewares: human-in-the-loop, summarization, planning/todo, file system。ガードレールのmiddleware実装パターン。create_react_agent → create_agent + middlewareへの進化。
- **重要度**: ★★★
- **関連章**: 第3章, 第4章, 第5章

### TLDV-03. [AIコーディング道場] 共同稽古
- **日時**: 2026-01-08
- **概要**: CLAUDE.md、スキル機能、コンテキストウィンドウ問題の実践的議論。Claude Memプラグイン調査報告（SQLite + MCPサーバーによるコンテキスト管理）。Claude Code 2.1アップデート共有。CLAUDE.md肥大化問題の実体験。
- **重要度**: ★★
- **関連章**: 第4章, 第6章

### TLDV-04. [AIコーディング道場] 共同稽古
- **日時**: 2025-11-04
- **概要**: スペック駆動開発（SDD: Spec Driven Development、「人間はコード書くな」ポリシー）の紹介。Claude Codeスキル機能の実践。コンテキスト管理の重要性（コード量増大による精度劣化、MCP厳選の知見）。
- **重要度**: ★★
- **関連章**: 第4章, 第6章, 第8章

### TLDV-05. ジェネラティブエージェンツ様 生成AI最新動向セッション
- **日時**: 2025-12-09
- **概要**: エージェント設計の進化（ReAct → Workflow → Deep Agents）の日本語コンテキストでの紹介。「ディープエージェント」用語の直接使用。AnthropicによるBun開発元買収のインパクト。金融分野でのドメイン特化ガードレールの必要性に関する議論。
- **重要度**: ★★
- **関連章**: 第1章, 第3章, 第9章

### TLDV-06. 定例）論文リサーチ
- **日時**: 2025-12-03
- **概要**: IBM論文: コンテキストウィンドウ溢れ問題の解決策として外部実行時メモリ + ポインタ方式を提案（ツール出力をコンテキスト外に保存しポインタで参照）。NVIDIA論文: エージェントセキュリティのためのガードレールエージェント群（グローバルセーフティ、攻撃、防御、評価の4エージェント）。リスクベースの防御配置原則。
- **重要度**: ★★
- **関連章**: 第3章, 第4章, 第6章

---

*以上 101件*
