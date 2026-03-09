https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7117898_7117899.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260309%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260309T010154Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=8a93352927e8692f5594ac48612925547c7c8ff15f414ce72cee072797436456e8335faaaf45c779eba8cfd8b8c0051f54f61bb73289389a81f5bce322bf8ae98cf8233841180aa8296cb44b05c23ce7f85ef6ef53ed536a39634c78a289151b58da7f588a4aad12717c896111edd06c43daa4e73132db00b49d6c468bccc1829668f19d9de263c62471ef1cdfbd5311673c5bdb38864591d27ca453ce44e8075531b2db5069d37dd0cdad718393f0c7fbe253d35d0eb8a2380b764e62bc5b22289129a49f045d795dd2562b5185c4785ef14aaa5547c4d6a48bc9cbbd4aff3abc3d37f1c6242dbdbb81052135fdd52a3a329bdcac102592dc418af0c485a6c1


#### 概要
* アーキテクチャドキュメントのレビューが進行中で、相違点は美咲が判断できるものは自分で解消し、判断がつかないものはチームでMob形式で確認する方針に決定
* Michaelが不要リソースの削除を進めており、約**$200**/月のAWSコスト削減を見込んでいる
* 先週末の発注期限を濱野さんが守れなかったため、今週頭（**3月9日**週）に小山さんとの調整を経て発注が動く見通し
* たかぴぃは体調不良で欠席


#### アーキテクチャドキュメントのレビュー進捗
* 美咲が吉田（真吾）作成のドキュメントとMichaelがまとめたアーキテクチャデザインを突き合わせてレビューを進め、いくつか相違点が出てきた
* 相違点は事実ベースのものはスペック側に反映する方向で、判断がつかないものだけMob elaborationで確認する方針に決定
* MichaelはSCP周りの設定をSection-9環境で先に試している段階で、吉田ドキュメントの取り込みはまだ


#### AWSコスト削減
* Michaelが不要リソースの削除を進めており、約**$200**/月の削減を見込んでいる
* 主な対象はElastic IPなど、割り当てているだけで課金されるIPv4リソース


#### H2OのAI内製化・運用方針
* 真吾がイベントで小山さんと会話し、H2O側の方針として以下が共有されていることを確認
* BCPは必要だが大阪リージョンに存在しないリソースがある点は認識済み
* NECのAWSツールやNRAのAWSツールは汎用性に限界があるため、AIを活用した内製化を先に進め、その後で対応できるベンダーを選定する方向
* 運用はフィリピンチームでしっかり固めたいという意向があり、24時間対応できる体制が必要


#### AILDCの運用フェーズでの役割
* AILDCのオペレーションはまだプレースホルダーの状態で、当面入ってこない見通し
* 真吾の見立てでは、運用フェーズのコンテキストはAILDCではなくDevOps AgentやAWSスキルなどの周辺領域で育っていく
* Section-9としてはAILDCはインセプションとコンストラクションのフェーズで価値を発揮できれば十分という認識


#### Section-9独自のOpsルール拡張
* Well-ArchitectedのOperational Excellenceピラーのベストプラクティスをベースに、Section-9独自の拡張ルールを自作する方向で真吾とMichaelが合意
* 実装方法は既存ディレクトリの隣に`SectionOpsRuleDetails`のようなディレクトリを切るだけでよいという認識


#### 発注の見通し
* 濱野さんから先週末（**3月6日**）までに発注が決まらなかったと連絡があり、今週頭に仕切り直しの予定
* 真吾はイベントで小山さんに直接プレッシャーをかけており、小山さんの一声で動くと見ている
* 真吾は年末に発注が来ていれば既に完了していたと指摘しており、早期完了を強く望んでいる