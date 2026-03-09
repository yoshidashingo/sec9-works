https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_6954755_6959223.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260302%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260302T010858Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=1e670913bf817ecce7346b9ebaab506aac312365f9a1295cb376f0680a1132a0e85f731c00570788763b2a41f34e104dcb3b51b4d7c089c53a7b2074e3895206825c964f2f3e8af8be3e7b2e04db6354b4317b6ffbd94beba965694d74683681095b3d950344d4265a434d06101bfa647aaae09534aaa5f0dd79fdd3cb0567d1b9e98081f63ca8701f1ba56347e89ebc28451a8218c74b4f26643c29b741bcf1073ea10fa252f3fff02f6cf03e8a15a6fc107bc961f598c43e82756878ddbbab4f564705e4bfafa3d5c9b75ca43a673f09efbcf78a19a558f7275cb26f96ec0047b243ebc8f3423cbd456715bcf3f436802b753a19b810cd4f40be8980519e09


#### Overview
* 真吾はH2O BCPプロジェクトの仕様書、提案書、リサーチ結果、テストを統合する新しいブランチを作成中
* キックオフミーティングは**3月15日**に予定されているが、チームはその前に作業を進める方針
* AWS Operations Rulesの独自拡張を作成する計画—AIDLCにはAWS特有のオペレーション詳細が含まれないため、Section-9の重要な資産となる
* 月次AWS利用料は**340万円**で、今後月次レビューを実施して無駄なコストを削減する
* Claude Codeの新機能SimplifyとBatchが登場し、エンジニアリングの仕事がAIハーネス作りとマネジメントに移行している


#### H2O BCPプロジェクトの作業状況
* 真吾は納品ドキュメントを作成中で、H2O BCPディレクトリに専用ブランチを作成予定
* 新ブランチでスペック、提案書、リサーチ結果、テスト全体を統合する作業を実施
* Michaelは自分のブランチを真吾のブランチに取り込む形で進める
* 竹内さんと乙部さんを含むチーム全員が既存環境のAPI/IAMアクセスを取得予定
* キックオフは**3月15日**だが、チームは事前に作業を進める方針で合意


#### Claude Codeの新機能(SimplifyとBatch)
* Simplifyはコードレビューとレトロスペクティブのためのスキル
* Batchはコードマイグレーションに使用し、超並列で実行可能
* **2週間前**に議論したCOBOLマイグレーションにBatchスキルが適用できる可能性
* エージェントチームとは異なるユースケースを想定している


#### AIによるエンジニアリングの変化と将来
* 真吾は「**2026年**に俺らのキャリアは終わった」と表現するほどAIの影響を実感
* 実務の**9割**はClaude Codeが実行しており、エンジニアの価値は承認ゲートとハーネス作りに移行
* 全員がCTO的な役割になっていくと予測
* AWSの初期と同様に、AI機能の発表を追い続けることが仕事になる
* 営業とブランディングの重要性が増している


#### AWSコスト管理と月次レビュー
* 今月のAWS利用料は**340万円**で、真吾は「何もやってないのに高すぎる」と懸念
* APN費用は**2,500ドル**だが、**3,000ドル**のクレジットで相殺される
* Cloudflareは**1円**も払わずに動作しているのと対照的
* 月次で棚卸しを実施し、無駄な高額サービスがないか確認する方針で合意
* 削減できても数万円程度と予想されるが、見落としを防ぐため実施


#### AWS Operations Rulesの独自拡張
* 真吾はAWS Operations Rulesの独自拡張を作成する計画
* AIDLCのオペレーションフェーズにはAWS特有の詳細が含まれない—InceptionやConstructionはグローバルなスコープだが、オペレーションは基盤と一体化している
* AIDLCチームはAWSロックインと誤解されることを避けたいため、AWS特有のルールは作らないと予測
* Section-9の実際の仕事はAWSオペレーションの細かいディテールなので、誰かが作る必要がある
* InceptionとConstructionフェーズのAWS拡張も検討—例えばApp Runnerのような「ほぼディスコン確定」のサービスを推奨しないようにする
* このカスタムルールとハーネスの深掘りがSection-9の資産になる