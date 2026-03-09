https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_6926592_6926593.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260227%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260227T010042Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=17011be4c81e17de5bbb2481f0bc60f45094456a42462bb8315448376ce470b6413cce0724103f996edbb550447ac66d431bc8d40a9d2f49db55f00d22061cf19e904a45902b23f26ab92ebde90f4ef3ab28eb715f999b11bf899dd223d27324cc3e92c6b45b023204090336412f9389ffcb27ede4c0032a68bca9b65d30e5373a14ddc2af60756acad163ae0d047a4e568f759aadfab8156967cfda7cc0366e90a784ec7311bff8390687ecc26c383394bc0df6995220caeda91875d4370caa6d660d6974f670054221d050ad87ecd7c21f4f4788dd76d712ef84bd29c439a016ab179a92d537834a69bf281a30014d5ea4b4c9af52bf2ec70ab254909e303c


#### Overview
* リポジトリ更新は完了し、Inception RequirementsとApplicationDesgは**12時間前**に最新版に更新済み
* 見積もりは**2,500〜2,600**日、構築が**93**日と算出されているが大幅な調整が必要
* **11時30分**までにプロポーザル内容をレビューして最終化し送付予定
* ドキュメントをBCP Specリポジトリに移動して全員でコラボレーションできる環境に整理
* オープンアイテム:MDWareの台数がRFPでは**27台**だが調査では**18台**、AWS Backupクロスリージョンコピーの実現可否調査が必要


#### リポジトリ更新状況の確認
* Michealがハムランさんからの資料を元にPOS側のリポジトリを再度更新し反映完了
* Inception RequirementsとApplicationDesgは**12時間前**の更新が最新版


#### 見積もり内容と工数調整
* 現在の見積もりは合計**2,500〜2,600**日、構築フェーズが**93**日
* **3ヶ月**もかからない想定で工数を大幅に削減する必要がある
* 真吾が**11時30分**までに金額部分を中心に調整して仕上げる予定
* プロポーザルはマークダウン形式で作成中で、提案内容、コスト、H2Oへの依頼事項を含む


#### ドキュメント管理とリポジトリ整理
* 真吾の個人作業フォルダに入っているためコラボレーションができない課題があった
* BCP、BCPテスト、BCP Specの**3つ**のリポジトリが存在
* ドキュメントをBCP Specリポジトリ(プライベート)に移動することを決定
* マークダウン、リファレンス資料(提案書、RFP、議事録)をBCP Specに格納予定
* 美咲がADLCベースで仕様書フォーマットの作成を開始済み


#### 作業分担
* 真吾:**11時30分**までにPOS側のフォワード内容を確認してプロポーザルを最終化
* 美咲:中間成果物と最終成果物の一覧案を作成、昨日Winxで作業していた内容を仕様に反映
* Micheal:オープンアイテムの確認と技術調査を実施
* なかぴーは**水曜日**から胃腸炎で体調不良のため不参加


#### オープンアイテムと技術調査
* MDWareの台数:RFPには**27台**と記載されているが調査結果では**18台**の不一致
* Michealがフェーズ1基盤設計の重要判断事項を調査予定
* FaceXバックアップのAWS Backupクロスリージョンコピーの実現可否調査が必要