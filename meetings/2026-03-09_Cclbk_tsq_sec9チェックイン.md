https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7117207.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260309%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260309T000810Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=5118036c612ea49423e24b95296d6d843e3a59b794e4dbb63b948032d6c1f8b04dd97243fd3af164910df448b9a5c8d008f9da6a6790cf4e2192d60e7f0955bdbf339ef222c93cff1ce82e482428c9b14ac44e73ca8cf36573194b87730633fdbd2139fd1e40b2ba4c4ac267689f8a53189a33c03bf9f1dae26b0eef7c61a03d4932ae02123e5043c3b1f40119fc0d2591b25ab4f17ec779d5a3e6b3fa90941557bef95b917f1cea3fe311c163a8629912f111d532a20a2612b7e4f24517614066dee9834f32b28b51624d07d409194095b19959538fad303931e2423e8d2bc84f36b7abb96bf9aca8243e51d78d3c3d29f3bf859897ace5236f7584c367c82d


#### 概要
* Gemini APIを使ったYouTube動画分析ツール（通称「YouTube更新君」）の開発チェックイン
* チャンネル登録をタスク入力からデータテーブル管理に変更することを決定
* Incoming WebhookからSlackアプリへの移行を決定し、必要なAPI設定を整理した


#### Gemini APIでYouTube動画分析
* YouTube動画のURLを渡すとGemini APIがタイトル・公開日・概要を返す機能をデモした
* 現状はタスク作成時のサンプルゴール欄にチャンネルのハンドルを手動で入力する仕様


#### 不正確な要約とプロンプト改善
* MacBook Neoの動画に対して「架空の製品」と誤った要約が生成された
* 湯はプロンプトを改善すれば誤情報は減らせると判断した


#### チャンネル登録のデータテーブル化
* 現状は1チャンネルずつタスクを作成する必要があり、複数チャンネルの一括管理ができない
* 吉田が「お気に入りチャンネル」用の専用テーブルを別途作成し、そこからチャンネルハンドルを取得する方式に変更するよう指示した
* テーブルへの行追加は手動で行い、その後AIに指示してチャンネル情報を取得する流れ


#### Slackアプリの新規作成
* Incoming Webhookではなく、Slackアプリとして新規作成することを決定した
* Slackアプリで実現したい機能：エージェントとのマルチターン会話、ファイル添付、ツール承認、セッション継続
* チャンネルへの要約投稿に加え、メンションでチャンネルをお気に入り登録できる機能も追加したい
* TaskZero専用のSlackアプリは存在せず、今回作るYouTube更新君のアプリがそのまま使われる


#### SlackアプリのAPI設定
* 必要な情報：Bot Token、Signing Secret
* 必要な権限スコープ：`app_mentions:read`、`im:read`、`chat:write`
* Signing Secretはすでに取得済み
* イベントサブスクリプション用のURLはTaskZero側で生成する必要があり、できたら共有するよう吉田が依頼した
* 湯がコラボレーターとして追加されることを希望し、ZoomチャットにメールアドレスをShareした