https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_6711490.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260217%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260217T235010Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=a0ac52e9527d0a47775bcb3df1600b0333ef8fff493fea13cabefd62cb9c379aff74becd19759d0a604c094a41205c25d80453400a0cda999b58da572a6b401816e5b4bbfc32b4216e108585e4897160d13d1cf80532bfdc9eaab45ea78d5ec820837ff1b357a25011e141ad8ea701e339490d8684ec24bf8b018f4a318c5f60ce76007c3bfa6c402e173bd79d0eb5412de19c0aaab9d142df4a94b1d39b4faa5224835df5486ca5ad434878f3d7877b426870cb5f1c47d81b45b6ceaf170c45abf5d5db54385819d369119ff2baf3fdb1310d7da3e76e4996a59d111ec21fcb6c40a432b81271236acab4534efe4fa4716e93ba1ca50ee04b462f2b8889c2af


#### Overview
* 湯が広告系デモを完成させ、AIを使ってDB保存まで実装した
* TaskZeroの定期タスク実装手順がドキュメントと実際で異なるため、高橋さんにGitHub issueで確認する必要がある
* Figmaマークダウンプラグインの改善が必要—処理が遅く出力が冗長なため、FigJamボードから構造化されたアイデアをクリーンに抽出できるよう改良する


#### 広告系デモの進捗
* 湯が広告系デモを作成し、AIを実装して結果をDBに保存する機能まで完成させた
* 現在は定期タスクではなく手動で実行している
* 定期タスク実装にはRepeatAPIを使用する予定
* 広告系APIの利用にはRepeatAPIが必要で、既に使用している
* 外部通信は定期タスクで問題なく使用可能


#### TaskZero定期タスク実装の課題
* ドキュメントに記載されている手順と実際のTaskZeroの実装手順が異なる
* 湯がGitHub issueで高橋さんに確認する予定
* 吉田真吾が美読ゼロのSlackチャンネルにも同じ内容を投稿するよう依頼した
* 高橋さんは今週忙しいが、書いておけば返信がもらえる見込み
* 定期タスクの実装方法がまだ完全に理解できていないため、詳細な操作方法を確認する必要がある


#### Figmaマークダウンプラグインの改善
* 湯が作成したFigmaからマークダウンに変換するプラグインの改善が必要
* **2月16日**のワークショップで使用したが、処理に時間がかかりすぎる
* 出力されるマークダウンが冗長で使いにくい
* マークダウン化の目的は、FigJamで出たアイデアをレポート化したりAIに指示しやすくするため
* ミーティング中にClaude webバージョンに不具合が発生したが、APIバージョンは正常に動作した
* 目標は、FigJamボードから不要な部分を削除し、構造化された必要な部分だけをクリーンなマークダウンとして抽出すること
* 吉田真吾がプロンプトを追加して冗長な部分を削除できるか試す予定
* 湯もプラグインを触ってみて改善点を検討する
* 吉田真吾がサイダスの仕事でも試してみる予定