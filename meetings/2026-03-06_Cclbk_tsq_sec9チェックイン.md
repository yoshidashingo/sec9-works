https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7084008.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260305%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260305T234241Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=329e916f3b7e14a472136021192daf2bf984cd8af38607f8f3375d96ccdc48001becac9b0068badf612b377c71111501aabc4c2771c3bb74aa46aff2b6512660942af66432ea551b3a752e1e9e1e52b9cad8e26306418e09cffba9018f99d1feb896117acf384d0d2e38f6a57a3b3e716339c7b1346ff17b1ccf12c51e51aaead19fdfe2a814727280c5e61aeab3b0bc3f98cbaeab3039749cb57c929061866873835f28751f75753a6920e7b6f5c290cb88d1fb7be951233f2cba53cb8a5cd048b50b33833002d0acf15312380931b2667b941ffac073d3e5577cf3b3c6e3d80e14458f24e7fa4e77d8dfb4f16779395abf7e567b38fb19894167842d4ea7fe


#### Overview
* YouTube通知アプリをリンク通知からGemini APIを使った動画サマリー付き通知に改善する方針で合意
* WorkOSの調査を開始することを決定 — 次回チェックインは**3月9日（月）**


#### YouTube通知アプリの改善
* 現状はYouTubeチャンネルの更新動画を取得してClaude AIでサマリーを作成しSlack通知する仕組みだが、真吾はタイトルとリンクだけでは面白くないと指摘
* NotebookLM APIは利用不可のためClaudeに切り替えた経緯があるが、動画の中身を理解したサマリーが必要という方向に変更
* YouTubeの文字起こしは投稿者が字幕をアップロードしているかどうかに依存するため、動画によって取得できないケースがある
* 湯が**約2週間前**（2月下旬）にGemini APIを試したところ、URLを渡すだけで動画を直接分析できることを確認済み
* トークン消費が多い可能性があるため、真吾は最も安いモデルを使うよう指示
* 通知フォーマットの合意内容：URL・公開日・Geminiによる動画サマリーの**3点**のみ（サムネや国旗などは不要）
* 想定ユーザーはYouTubeを大量に視聴しているが時間がない人で、本当に面白い動画だけを効率よく見つけられるようにすることが目的


#### Gemini APIの設定
* 既存の**GACopilotProject**のAPIキー（Gemini / JQL用）を流用することに決定
* 湯がAPIキーのキャプチャを取得して共有する


#### WorkOSと認証ツールの調査
* 湯がjCompilerの認証調査について確認し、YouTubeアプリ対応が終わり次第進める予定
* 真吾はWorkOSが急速に強化されており、AnthropicとOpenAIも採用していると共有
* 真吾の見立て：モデルやエージェントフレームワーク、アプリケーション層は競争が激しく差別化が難しいため、認証・認可やサンドボックス・ランタイム環境といったニッチなツール層が最も競争優位を持てる
* WorkOSはそのようなツールの代表例として分析対象に設定し、真吾も自身で調査を進める