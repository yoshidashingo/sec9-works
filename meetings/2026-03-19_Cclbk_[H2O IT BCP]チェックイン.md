https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7385016_7385017.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260319%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260319T005659Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=ae8b950035824267984806ce7ecb54523aeecdb28e0de0eef1a7f9d3b0e58ee3bd4ce80d872697e042bb676a94619e4679ad1d9f5b27d20a305ce25fa9524e73136afe9188cb5fa0ba32c063ac5e671f27413ffd7b3ebfdf321add4def0f2c1c63d7ca200a354dc5c11500f40daf28574635bed424baaf2af499da9b872b76d144c0b6daa1a950cb494faa3829948f22ce1803d5b0e66b6b82387ab62f832c8ea79b31acf715b8e6d4c5a4486e949778f2d4ca5e29783b0f384fa74256e24733ceaf1b76ebb38f807d98ab3f210ac3ae51b2874204aa6024d37a8b565afe8073ec7abea4a9c49c0a7d4342cafe5b09e3f5507af670dc464f7868ddd2780d1f45


#### 概要
* 昨日（**3月18日**）浜田さんとの顔合わせは完了したが、具体的な進展はなく、キックオフは**来週（3月23日）以降**に設定される見込み
* MDware/POSのアカウント分離、バックアップ系リソースの移行スコープ、見積書・注文書の送付先など、設計着手前に確認が必要な論点が複数残っている
* 明日（**3月20日**）は祝日のため定例スキップ、次回は**月曜3月23日**


#### キックオフ日程の調整
* 昨日の浜田さんとの打ち合わせでは「何を確認していくか」の方向性を確認するにとどまり、具体的な動きはまだない
* すでに提示している日程をベースに、来週以降でキックオフが設定される見込み


#### MDware/POSのアカウント分離
* 昨日の定例で、MDwareとPOSのDRP環境はアカウントを分けた方がよいのではという意見が出た
* POSは監査基準が厳しいため、アカウント分離の必要性自体は乙部も妥当と判断している
* 今回のプロジェクトでやるのか、後回しでよいのかを竹内さんまたは今井さんに確認する予定で、設計開始前に結論をもらいたい状態


#### バックアップ系リソースの移行スコープ
* アカウントを分離する場合、バックアップ用のLambda（"backup"という名前）やStep Functionsが複数システムから共通で呼ばれているため、それぞれのアカウントに持たせる必要が生じる可能性がある
* Michaelは、Osaka regionでの環境構築はSection-9のスコープだが、既存環境からの引っ越し（移行）自体は別スコープではないかという見方をしている
* 乙部は、アカウント分離を進める場合に誰が移行を担当するかも含めて確認が必要と認識している
* 真吾は、このインパクトだけは先に調べておくべきと指摘した


#### 見積書・注文書の送付先
* 吉田さん（真吾）から見積書・注文書を送る必要があるが、送付先が海人さんなのか今井さん・竹内さんなのか未確定
* 乙部が今井さんまたは竹内さんに確認する