# Harness Engineering 書籍 - 要件確認質問

**Harness Engineering の定義**: AIエージェントを自律的かつ信頼性高く動作させるための環境設計・ポリシー・ガードレール・フィードバックループを包括する方法論。Prompt Engineering → Context Engineering → Harness Engineering という進化系の最新段階。

以下の質問にお答えください。各質問の [Answer]: タグの後に、選択肢のアルファベットを記入してください。
選択肢に該当するものがない場合は、最後の「Other」を選択し、詳細を記述してください。

---

## Question 1
本書のスコープとして、Harness Engineeringのどの範囲をカバーしますか？

A) 包括的に扱う（Prompt Engineering → Context Engineering → Harness Engineeringの進化系全体を俯瞰し、Harness Engineeringを中心に据える）
B) Harness Engineering に特化（Context Engineeringまでは前提知識として簡潔に触れ、ハーネス設計・運用に集中）
C) 実践ガイドとして（理論は最小限に、具体的なツール・パターン・実装例中心）
D) Other (please describe after [Answer]: tag below)

[Answer]:A

---

## Question 2
本書の主なターゲット読者は誰ですか？

A) AIエンジニア・MLエンジニア（エージェント開発の実務者）
B) ソフトウェアエンジニア全般（AI活用開発に移行したい開発者）
C) テックリード・アーキテクト（組織にAIエージェント基盤を導入したい意思決定者）
D) 経営層・プロダクトマネージャー（AIエージェント戦略を理解したい非エンジニア）
E) Other (please describe after [Answer]: tag below)

[Answer]:A,B,C

---

## Question 3
本書で取り上げるべき主要なプラットフォーム・ツールとして重視するものはどれですか？

A) OpenAI Codex / ChatGPT エコシステム中心
B) Anthropic Claude Code / Claude エコシステム中心
C) マルチプラットフォーム（OpenAI, Anthropic, LangChain, Salesforce Agentforce等を横断的に）
D) プラットフォーム非依存（概念・原則中心で、特定ツールに依存しない）
E) Other (please describe after [Answer]: tag below)

[Answer]:C

---

## Question 4
本書に含めたい主要テーマとして、特に重視するものはどれですか？（複数ある場合はOtherで列挙してください）

A) エージェントハーネスのアーキテクチャ設計（6つの標準コンポーネント: Reasoning Engine, Planning & Orchestration, Tool Registry, Memory & Context, State & Persistence, Structured I/O）
B) ポリシー・ガードレール設計（AGENTS.md, Golden Principles, ルールファイル体系, 品質ドキュメント）
C) 長期実行エージェントの運用パターン（セッション継続性, 進捗ブリッジング, 自動リファクタリング, 増分開発）
D) 組織導入・チーム運用（Agent-first開発文化への移行, PRフロー変革, 人間とエージェントの役割分担）
E) Other (please describe after [Answer]: tag below)

[Answer]:A,B,C,D

---

## Question 5
書籍の想定ページ数・ボリュームはどの程度ですか？

A) 100〜200ページ程度（コンパクトな入門書・エッセンシャルガイド）
B) 200〜400ページ程度（標準的な技術書）
C) 400ページ以上（包括的なリファレンス）
D) 特に決めていない（内容に応じて柔軟に）
E) Other (please describe after [Answer]: tag below)

[Answer]:D

---

## Question 6
書籍の言語は何ですか？

A) 日本語
B) 英語
C) 日英バイリンガル（日本語メインで英語の原典を併記）
D) Other (please describe after [Answer]: tag below)

[Answer]:A

---

## Question 7
この書籍の独自の価値・差別化ポイントとして考えているものはありますか？

A) AI-DLC（本リポジトリで使用しているワークフロー）のような実践的フレームワークを体系化して紹介
B) 日本企業・日本語コンテキストでのHarness Engineering導入事例・ベストプラクティスを提供
C) Prompt → Context → Harness の進化を俯瞰し、次世代のAI開発パラダイムを提示する概念書
D) 特にまだ決めていない（提案してほしい）
E) Other (please describe after [Answer]: tag below)

[Answer]:A,D

---

## Question 8
出版形態はどれを想定していますか？

A) 商業出版（出版社から刊行）
B) 自費出版・セルフパブリッシング
C) 電子書籍のみ（Kindle, Zenn Book等）
D) 社内技術資料・教育テキストとして
E) Other (please describe after [Answer]: tag below)

[Answer]:A

---

## Question 9
企画書・目次・参照文献の成果物は、どのような活用を想定していますか？

A) 出版社への企画提案用
B) 実際の執筆開始前の全体設計・ロードマップとして
C) 社内や顧客向けのプレゼンテーション・提案資料として
D) 複数の用途に使いたい（上記の組み合わせ）
E) Other (please describe after [Answer]: tag below)

[Answer]:B

---

## Question 10
参照文献の収集方針として希望するものはどれですか？

A) 一次ソース中心（OpenAI, Anthropic, LangChain等の公式ブログ・ドキュメント）
B) 学術論文・研究ペーパー中心（arXiv等のAIエージェント研究）
C) 実践事例・業界記事中心（Medium, Substack, 技術ブログ等）
D) 上記すべてを網羅的に（一次ソース + 学術 + 実践事例）
E) Other (please describe after [Answer]: tag below)

[Answer]:D

---
