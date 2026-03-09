https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_6829878.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260224%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260224T010748Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=5d3e71b48599255eb2ef1f58aecc0309e2f4fcf4b91da3e03889f21dd7a237099627ce533d0137f298c19ed7d0cd1e19b761e65176f9c28bb456059efa5f0672c0cb6295bc82e1cc9a718e2d28dc8941ae6541f443fb6d2b7965be9b446bdeb70af2f5ecbd0cbbfc5825a24fc60e79d4f26315e82de107add49cbf73e9962ad8103798442a1659ad681814bb8cb374e6302141cd7e1a51776caa1e05b44c7398705c65b97ffde91b941e2e7ec4aed48b9c05ceed0dc46911795738b0218b0f58ca017bc693a89a332077c63fad4f0310c3f2e345333a223da3d1782d97e311a349f6a55519dba97b1e1e2ef9ec5928695df8d9e7f1c6473cd6168417e1eeb1d3


#### Overview
* H2O BCPプロジェクトのスコープが縮小され、現在はミドルウェアのみが対象となり、他のコンポーネントは後回しに
* 包括的DR設計書のドラフトが完成
* プロジェクト推進の最大の課題は社内政治で、部長レベルの攻略が重要
* チームメンバーがMCPとAIDLCを活用した自動化ワークフローを共有し、作業効率化を推進


#### H2O BCPプロジェクトのスコープ変更
* プロジェクトスコープがミドルウェアのみに縮小され、ボスは後回しになった
* 包括的DR設計書のドラフトが完成し、これに基づいて作業を進める方針
* 不確定な作業も含めて先に予算確保ができた
* **3月**分の発注はタカピーに出される予定
* Takahasiは先週分のキャッチアップができておらず、**今日1日**を使って追いつく作業に充てる


#### 社内調整と部長レベルの攻略
* H2Oの社内政治が最大の課題で、小山さんの下かつ濱野さんの上にいる部長レベルの攻略が最重要
* 三板さんだけでなく、部長レベルがバシッと決めてリードする必要がある
* 現在は各所に根回しを行っている段階
* 部長レベルが動けば、あとはベンダー間の調整のみになる見込み
* ベンダー間の綱引きは最終的にH2Oの意見が最優先される
* 濱野さんとの打ち合わせを**今週**中に設定予定で、夕方の時間帯が多いパターン


#### AI/MCP活用の自動化ワークフロー
* Shingoが仕事と個人作業を全自動化するため、1リポジトリに全てを統合
* ステアリングファイルにAIDLC、GAのサービス、コンサル手法、ブログのテクニカルライティングルール、メールライティングルールを全て格納
* MCPにバックログ（GAのKHI、Section-9のCircleBack）、Google Workspace、NotebookLM、AWS Documentation、TLDVを統合
* 議事録取得を夜間バッチで自動化し、毎晩GAはTLDVを使用、Section-9はCircleBackを使用してミーティングを同期
* Claude.mdでGAとSection-9のクライアントワークが混ざらないよう、フォルダ構成とMCP許可指定を分離
* Apple LaunchDで定期実行を登録し、SyncAllCronでMarketHackCronとSyncMeetingを実行
* 個人の投資用にマーケットハックマガジンやパウロのメルマガも毎晩チェック


#### AIDLCプラグインの紹介
* TakahasiがClaude AIDLCというリポジトリを作成
* プラグインをユーザールートに入れておけば、いつでもどこでも最新のAIDLCドキュメントをインジェクション可能
* AIDLC initコマンドで最新のAWS Labsワークフローから必要なものを取り込める
* updateコマンドで変更があった際に追従できる
* 新規プロジェクトだけでなく、既存プロジェクトの途中からでもAIDLCを導入可能