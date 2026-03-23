https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7444334.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260322%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260322T235524Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=44bb7fdaaaf3e07ade92c528d719dee0a3541136c423c8a24df71375efb6ff7755349ce660f3d5312863e4d8928fa6a0a606f24a4e058ed0e37a27a17603ac61139339453ac8b01cc45aaad0bc43bbee273efda667150b46d9e18fc6f68b76027d8414f3085aaad3786ff93549cd9401e84e378f9dbb2104d26709867743a0d1b9558dc31dbe8b5b065e7224f3c757a063a539664cab400b3e128b9e49840b5c923cd42ac63483ff9b3e947209c087659b7e4fec6ac340fd3bcf207d0427502fd89dc86971a012f317f0f49fb1addec11f7a9a4dc60c8f7f8a35d6d18884424858ec8ff812a8e69cc6c0078cdcab69820f79fc59ee1964c486c4d0270bc04cbc


#### 概要
* 湯がWorker OS、GA Copilot、MiDoc Zeroの進捗をデモ形式で共有
* MiDoc Zeroはデプロイ失敗中（Reactライブラリの競合が原因）で対応が必要
* MiDoc ZeroのSuperhuman比較はAIを使って調査する方針に


#### Worker OSのデモ
* 湯がWorker OS（Clerkからリファクタリング）をデモし、ログイン後に休眠画面へ遷移する動作を確認
* Shingoは開発環境にはログインできることを確認
* Clerkは現時点で完全に動作しているため、Worker OSのブランチは残しつつClerkも引き続き使える状態を維持する方針


#### デプロイ環境と課金の問題
* Worker OSのワークスペースには開発環境とプロダクション環境の**2**つがあり、プロダクション環境の利用にはIDとキーの取得のために課金が必要
* 開発環境は無料で利用できるが、プロダクション環境へのデプロイには課金が必要で、これが問題として挙がった


#### GA Copilotへのテスト追加
* 湯がGA CopilotのCIアクションに自動テストを追加し、TypeScriptのエラーチェック後にテストを実行する流れを構築
* 前回のミーティングで吉田さんから「テストがない」と指摘されたことへの対応


#### デプロイ失敗とライブラリの競合
* MiDoc ZeroはPRマージ時に自動デプロイされる設定だが、最新のマージでデプロイが失敗
* 原因は自動テストのPRに追加したReactライブラリが既存ライブラリと競合しているため
* Shingoは競合の解消にAIを活用するよう指示


#### Superhuman比較とMiDoc Zeroの方向性
* MiDoc ZeroのユーザーはGoogleログインで直接認証しており、Clerk/Worker OSは経由していない
* 現状はSuperhumanに勝てていないとShingoは見ており、AI機能とUXの両面で差があると指摘
* SuperhumanのAI機能と公式サイトをDeep Researchで調査し、MiDoc Zeroが上回れる機能を洗い出す方針
* ShingoはAI部分の作り直しも視野に入れている