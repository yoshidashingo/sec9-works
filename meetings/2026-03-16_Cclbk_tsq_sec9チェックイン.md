https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7282993.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260316%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260316T000946Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=69ac3aba2e2132ccf032d47643eff8776d4065c264ac44421c3c0b6fb4e6b1c598dc312067bfd754598b493a60522a944705fe3de2a091d35b7f07980298d8e7ccaf3cc616b6099f66959603ddd174d4a722b7379c4e6ce8c55ba14e5636d5e68875dceacc9eceecf5629fb7ef6682e7b1c4437649e1d86967a453eea8406207c731c277c7fcd0b6f6a9bd1075da4e70e7c09bcd8bbb3b4a9489a4dd854d52d2540e883ceff8dc66e661c8e1247817a088f681a033b0defad7fbaf930e54dd9b3ca06729e9baf878b2cad8abbb1f575b2c9424157c38c1d3da1fdd50e5a16f1af581d09bdb8746857a701537f87ffcd078fa4c68696d78a4e89321a93f9864b5


#### 概要
* AIDLCとスキルの違いを整理し、CLAUDE.mdをREADMEに統合する方針で短縮した
* データアナライザーのインセプション（CSV/Excel自動分析・可視化）を開始し、セキュリティベースラインを必須と決定
* AIDLCDocsのコードクオリティアセスメントに記録されている技術的負債（テスト不在・エラーハンドリング不十分・リンティング未設定）をAIで修正していく方針を確認
* WakuOSのIDP設定が完了し、招待を送る予定（issue **#39**）


#### AIDLCとスキルの違い
* スキルはコマンドツール、AIDLCはアジャイル・スクラム・エクストリームプログラミングといった開発方法論を規定するもの
* ただし開発ルールや仕組みをスキルに入れることも可能で、両者は重なる部分がある
* 湯が紹介した海外企業の事例では、コーディングルール・テストルール・デザインルールをすべてMCPスキルに入れ、Claude Codeが毎回参照する形で運用している
* AWSが公開しているAIDLCルールはまだスキル化されていないため、AIDLCスキルとして整備することも選択肢として挙がった


#### Claude Codeの設定確認
* bypass permission mode、Opus 1、MTextosCapableの設定を確認し、デフォルトと同一のためそのまま継続
* デフォルト設定はauto/mediumのまま（max設定への変更は見送り）
* AIDLCのDocsをすべてプロンプトに含めているためトークン消費が大きいが、Maxプランのため問題なし
* Claude CodeはコアワークフローにAIDLCの参照が定義されているため、プロンプトに明示的な指示がなくてもAIDLC Docsを参照する


#### CLAUDE.mdの整理
* プロジェクト概要・技術スタック・開発コマンド・コーディング規約はREADMEに移し、CLAUDE.mdには重複して書かない方針
* 手順の記載も不要と判断し、内容を短縮した
* 真吾がミーティング中に変更をプッシュ済み


#### データアナライザーの設計
* CSV・Excelの構造データをアップロードし、AIが自動的に分析・可視化する機能として設計
* フロントエンドは既存のアシスタント形式のパターンを踏襲
* セキュリティベースラインは必須とし、週**1**回の頻度で設定
* Extensionsディレクトリでオプトイン方式を採用する新しいアーキテクチャを確認


#### 技術的負債の修正方針
* AIDLCDocsのコードクオリティアセスメントに以下の技術的負債が記録されている
* テストコードが存在しない
* 一部エージェントでエラーハンドリングが不十分
* バックエンドのリンティングが未設定
* これらをAIで修正させていく方針
* パッケージ管理をpipからuvへ変更することも検討中


#### WakuOS認証の導入
* 先週/先々週に話題になっていた認証導入について、IDPをClerkからWakuOSに変更する方針
* 真吾がミーティング中にWakuOSのIDP設定を完了し、招待を送る予定（issue **#39**）