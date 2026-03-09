# AI-DLC (AI駆動開発ライフサイクル) を完全理解する

[https://www.facebook.com/yoshidashingo1:title=吉田真吾] ([https://twitter.com/yoshidashingo:title=@yoshidashingo]) です。

## 全12回シリーズ

AI-DLC (AI-Driven Development Life Cycle) を、隣接する開発手法との比較を交えながら基礎から順を追って解説するブログシリーズです。ソフトウェア開発の基本的な流れを知っているエンジニアや、AI活用に関心のある開発リーダーを主な対象読者としています。前半 (第1回〜第7回) はAI-DLCの概念と設計思想を既存手法と絡めて解説し、後半 (第8回〜第12回) はワークフロー定義ファイルの中身を1行ずつ読み解きます。
[https://aws.amazon.com/jp/blogs/news/ai-driven-development-life-cycle/:embed:cite]

[https://prod.d13rzhkk8cj2z0.amplifyapp.com/:embed:cite]

---

## [前半] AI-DLCの考え方を完全理解する

前半では、まずAI-DLCの全体像を俯瞰した上で、ワークフローの実行順序に沿って各ステージを解説します。歴史的な開発手法との比較を挟むことで、AI-DLCが「なぜそう設計されているのか」を理解しやすくなる構成にしています。

### AI-DLCを完全理解する 第1回: 「AI-DLC」って何？
- AI-DLCの全体像と設計思想
- SDLCの歴史を振り返る: Waterfall → V-Model → RUP → Agile → DevOps
- AI-DLCは何が新しいのか: 「適応型ワークフロー」という発想
- 3フェーズ (INCEPTION / CONSTRUCTION / OPERATIONS) の俯瞰
- ALWAYSステージとCONDITIONALステージの意味

### AI-DLCを完全理解する 第2回: はじめかた ― まず「現状を知る」
- Workspace Detection: プロジェクトの初期調査
- Reverse Engineering: 既存コードベースの読み解き
- Brownfield vs Greenfield という概念
- 比較: TOGAFの「Architecture Vision」、レガシーコード改善の考え方

### AI-DLCを完全理解する 第3回: 「何を作るか」を決める ― 要件定義はここまで進化した
- Requirements Analysis: 3段階の深度 (Minimal / Standard / Comprehensive) 
- User Stories: ユーザー視点で要件を語る
- 質問ファイル方式という独自の仕組み
- 比較: アジャイルのユーザーストーリー、EARS記法、DDDのユビキタス言語

### AI-DLCを完全理解する 第4回: 設計図を描く ― 計画と分割の技術
- Workflow Planning: どのステージを実行するか決める
- Application Design: コンポーネントとサービスの設計
- Units Generation: 作業単位への分割
- 比較: SAFeのPI Planning、C4 Model、マイクロサービスの分割戦略

### AI-DLCを完全理解する 第5回: ビジネスロジックと品質を設計する ― Construction前半戦
- Per-Unit Loop: ユニット単位で回す設計サイクル
- Functional Design: 技術に依存しないビジネスロジック設計
- NFR Requirements / NFR Design: 非機能要件の扱い方
- 比較: DDDの戦術的設計、AWS Well-Architected Framework、ISO 25010

### AI-DLCを完全理解する 第6回: コードを生み出し、テストで守る ― Construction後半戦
- Infrastructure Design: 論理設計を物理インフラに落とす
- Code Generation: 計画→承認→生成のプロセス
- Build and Test: 6種類のテスト戦略
- 比較: Infrastructure as Code、TDD/BDD、CI/CDパイプライン

### AI-DLCを完全理解する 第7回: AI-DLCを貫く設計思想 ― 適応・監査・承認のしくみ
- OPERATIONS Phase: 将来への布石
- Adaptive Depth: 複雑さに応じて深さを変える
- aidlc-state.md: 進捗の記録と再開
- audit.md: すべてのやり取りを残す監査証跡
- 承認ゲート: 人間が最終判断を握る設計
- 比較: GitOps、SOC2/ISO27001の監査、Stage Gate Process

---

## [後半] ワークフロー定義ファイルを徹底解読する

後半では、前半で培った概念理解をもとに、実際のワークフロー定義ファイルを1行ずつ読み解いていきます。core-workflow.mdから始めて共通設定、各フェーズの順にディレクトリ構造を辿ることで、実装レベルの理解を積み上げます。

### AI-DLCを完全理解する 第8回: core-workflow.md を読み解く ― AI-DLCの「憲法」
- ファイル冒頭の宣言: なぜ「他の全ワークフローをオーバーライド」するのか
- 4つのMANDATORYルール
- INCEPTION / CONSTRUCTION / OPERATIONS の定義構造
- Key Principles (8原則) の深掘り
- チェックボックス追跡と監査ログの書き方ルール

### AI-DLCを完全理解する 第9回: commonディレクトリの全貌 ― AI-DLCの屋台骨
- process-overview.md: 技術リファレンスとしての全体図
- welcome-message.md / session-continuity.md: 開始と再開のお作法
- question-format-guide.md: 質問は必ずファイルで、選択肢＋[Answer]タグ
- depth-levels.md / terminology.md: 言葉と深さの統一ルール
- overconfidence-prevention.md: 「聞きすぎるくらい聞け」の思想
- content-validation.md / ascii-diagram-standards.md: 図表の品質管理
- workflow-changes.md / error-handling.md: 変更とエラーへの備え

### AI-DLCを完全理解する 第10回: inceptionディレクトリ徹底解説 ― 計画フェーズの7ファイル
- workspace-detection.md: 唯一「承認不要」のステージ
- reverse-engineering.md: 8種の成果物テンプレート
- requirements-analysis.md: AIがプロダクトオーナーの視点で要件を整理する
- user-stories.md: 最大ボリューム、23ステップの全容
- workflow-planning.md: Mermaidフローチャートの自動生成
- application-design.md: 4つの設計成果物
- units-generation.md: UOW (Unit of Work) の分割ロジック

### AI-DLCを完全理解する 第11回: constructionディレクトリ徹底解説 ― 実装フェーズの6ファイル
- functional-design.md: ドメインエンティティとビジネスルールの設計
- nfr-requirements.md: 8カテゴリの質問で非機能要件を洗い出す
- nfr-design.md: パターンで品質を組み込む
- infrastructure-design.md: 論理→物理のマッピング
- code-generation.md: Brownfieldの「コピーファイル禁止」ルール
- build-and-test.md: 6種のテスト × 5つの成果物

### AI-DLCを完全理解する 第12回: Operationsと拡張レイヤー ― AI-DLCの未来とカスタマイズ
- operations.md: プレースホルダーが示す将来ビジョン
- GA拡張レイヤー: ベースレイヤー＋拡張レイヤーの二層構造
- ルール読み込みの優先順位
- 自社に合わせたAI-DLCのカスタマイズ方法
- シリーズ総括: AI-DLCが変える開発の未来

---

## [独立記事] テーマ別の深掘り

メインシリーズを補完する独立記事です。特定のテーマについて、シリーズの複数回にまたがる内容を横断的に整理しています。

### AIワークフローの駆動方式で理解するAIエージェント
- 事前定義型ワークフロー (Pre-defined Workflow) と適応型ワークフロー (Adaptive Workflow) の比較
- 適応型ワークフローの4つの構成要素: ステアリングファイル・ワークフロー定義・ルールブック・メモリ

### Claude Codeで実践する仕様駆動開発入門
- バイブコーディングの問題点とVerification Debt
- 仕様駆動開発の原則: 仕様は情報源、プロセスはルールブックが駆動
- AI-DLCのステアリングとスキル化の功罪

### AI-DLCワークフローはハルシネーションをどう防いでいるか
- 5つのメカニズムの多層防御: 過信防止・構造化Q&A・承認ゲート・監査証跡・コンテンツ検証
- overconfidence-prevention.mdが運用フィードバックから生まれた経緯
- 「発生の抑制」「波及の防止」「事後検証の可能性」という3層構造
- プロンプト指示による制御の限界
