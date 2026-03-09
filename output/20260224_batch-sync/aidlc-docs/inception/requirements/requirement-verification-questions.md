# 情報同期バッチ処理 - 要件確認質問

以下の質問に回答をお願いします。各質問の `[Answer]:` タグの後に選択肢の記号を記入してください。

---

## Question 1
この「情報同期バッチ処理」で同期する対象データは何ですか？

A) 既存の同期対象と同じもの（ミーティング議事録、Paulo記事、Market Hack記事）を別実装で動かす
B) 新しいデータソースを追加したい（具体的なデータソースがある）
C) 既存の同期処理をclaude -p版とAgent SDK版の2方式で書き直す（リファクタリング・比較検証）
D) 具体的なデータソースは未定で、まず2方式のテンプレート・雛形を作りたい
E) Other (please describe after [Answer]: tag below)

[Answer]:A

## Question 2
Claude Agent SDKはどの言語のSDKを想定していますか？

A) Python SDK（anthropic-sdk-python の agent 機能）
B) TypeScript/Node.js SDK（@anthropic-ai/sdk の agent 機能）
C) Claude Agent SDK（anthropic/claude-agent-sdk - Python）
D) 両方（PythonとTypeScript）のサンプルを作りたい
E) Other (please describe after [Answer]: tag below)

[Answer]:A

## Question 3
2方式（claude -p と Agent SDK）の関係性はどういう位置づけですか？

A) 比較検証が目的：同じデータソースを2方式で実装して性能・コスト・信頼性を比較する
B) 段階的移行：現行の claude -p を将来的にAgent SDKに移行する準備として
C) 使い分け：用途に応じて適切な方式を選べるようにする
D) 教育目的：ブログ・書籍等のコンテンツとして両方式の実装例を作る
E) Other (please describe after [Answer]: tag below)

[Answer]:C

## Question 4
Agent SDK版の実行環境はどこを想定していますか？

A) ローカルマシン（現在のcronと同様にmacOSで実行）
B) クラウド（AWS Lambda、Cloud Functions等）
C) Docker コンテナ（ローカルまたはクラウド）
D) まだ決めていない（設計段階で検討したい）
E) Other (please describe after [Answer]: tag below)

[Answer]:A

## Question 5
既存の sync-all-cron.sh との統合方針はどうしますか？

A) sync-all-cron.sh に新しいスクリプトを追加する（既存パターン踏襲）
B) 別のエントリポイント（別のcronジョブ）として独立させる
C) claude -p版は sync-all-cron.sh に追加、Agent SDK版は独立して実行
D) まだ決めていない（設計段階で検討したい）
E) Other (please describe after [Answer]: tag below)

[Answer]:D

## Question 6
Agent SDK版で使いたいMCPサーバーやツールの制約はありますか？

A) 既存のMCPサーバー（google-workspace, tldv, backlog等）をAgent SDKからも使いたい
B) MCPサーバーは不要。REST APIやSDKを直接呼び出す方式にする
C) MCPサーバーとREST APIの両方を検討したい
D) まだ決めていない
E) Other (please describe after [Answer]: tag below)

[Answer]:A

## Question 7
成果物のスコープについて。今回のAI-DLCで期待するゴールは？

A) 設計文書のみ（要件定義・アーキテクチャ設計まで）
B) 設計文書＋実装コード（動作するバッチ処理を完成させる）
C) 設計文書＋プロトタイプ（最小限の動作確認ができるレベル）
D) Other (please describe after [Answer]: tag below)

[Answer]:B
