https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7445096_7445097.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260323%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260323T010319Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=1d2919f0fcc15228f4a68a7a272b8dfcb16472d6b5f4d50cb9ffad05a504ebf6f4b4d85340d8852cb258b5008e333eb2448b262a7a100434a45a94d33d3fb532eaa985c5b83696c7ab8e1f9af4206eb8292cf4583f2342726cafa7de2778724a6c3caf8053145676baf111c816ceff3a5e7dd541a82ce9860cc72c361765a58a773a51ab756538865532d90bbad58fd427b50de4857f6ce36023261682fbed8062436c29a3556092bf2d475c2e5ecb16c45990513d806ad665be9a70b218ba15dfa232003c0bc41344f8d4122998028d8729b0a8bb5934d6bfbd02968cfb34101c6a51c6995a5023b1c799b2774f25efd3403223bba6a1cd6e388df8857a2c7e


#### 概要
* BacklogをGanttチャート利用のため有料プランにアップグレード済み、乙部さんが依存関係を整理してスケジュールを詰める
* MichaelがTokyoリージョン・Osakaリージョンの検証を完了、有効化に向けて問題なし
* BacklogはClaudeのMCP連携前提の構成にしており、全員がMCPまたはcurlで設定しておく必要あり
* 課題管理表はまだ未完成、リポジトリのMarkdownで管理する方向で進行中


#### バックログとGanttチャートの整備
* 真吾がGanttチャートを使えるようにBacklogをプランアップグレードした
* 乙部さんがタスクの前後関係を意識しながらGanttを詰めていく
* 親子関係が未設定のタスクやマイルストーンが未入力のものが残っており、乙部さんが整理する
* 例として、タスク **58** 番などは親タスクにして手順書作成などを子タスクに分割する想定
* Ganttを引き直すことで全体のスケジュールが圧縮される見込みで、それで問題ない
* バーンダウンチャートはBacklogの「フォーム」から確認できる


#### スケジュールと進捗確認
* 真吾はBacklogの全タスクが完了になれば案件完了になるよう一通り洗い出して登録済み
* 個々のタスク進捗確認よりも、実際にぶつかっている課題や品質に影響する問題を話せる状態にしたいと真吾は考えている
* Shinichi は今週（**3月23日**週）と来週（**3月30日**週）が多忙


#### 非推奨機能の検証
* MichaelがTokyoリージョンとOsakaリージョンで検証を実施、問題なさそうなので有効化する予定
* デプリケーション（非推奨機能）周辺の検証が今後の課題になると真吾とMichaelが確認した


#### 課題管理表とドキュメント整備
* 乙部さんはスプレッドシートではなくリポジトリのMarkdownで課題管理表を作る方向に切り替えた（濱野さんの意見を受けて）
* 課題管理表はまだ未完成で、引き続き進める
* エジソーさんにGoogle Driveを用意してもらい、クライアントと同じ課題管理表を共同編集できる環境を整える予定
* BacklogのMCPトークンを発行してもらうことも検討中（濱田さんと話した内容）


#### BacklogのMCP・Claude連携
* BacklogはClaudeでぶん回す前提の構成で作られており、タスクを一つ一つ目で追う想定ではない
* 全員がBacklogのMCPまたはcurlを設定して、タスク全体を把握できる状態にしておくよう真吾が求めた
* プロジェクト管理をAI時代に合わせてレベルアップしていく方針