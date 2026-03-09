https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7087355_7087365.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260306%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260306T024854Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=6b513d428fb3d9230ba8fb39bf6fd45571acd8ec3e7b88240ea65b1165f9bbfb891b4b4911c52b8e3e610ce9ff6b22df6aa995e028be988c9c21f24d01d5f59ae783fb15be2f1d60ffc0d4f37473bf8ba9dd3b868d6575b57c9fe9a226377185a040a781b78722d207377aeb430e5ec05a4ff1b9f52bc9dbf1c78e732ae80bedb57bb9ec5f2b011bd7b0471da7cc604725fb908fffc3522735b41fb0c5295cd31189a407b10b6d0189ea5e30242725c3147e5affa7d4c43d76260366cdb80f4b539a966d1072be392af54ac5ec5d503fa5f573dcaa46d3be71812c46183fa426587cbb7e28e4ee9fe1706dedbdc9209ccac4171267e43d754cc19fee13cced61


#### 概要
* DR手順書のプルリクが上がっており、内容の確認とTerraformコードの検証が次のステップ
* 検証項目は時間計測を除外し、実現可否の確認に絞ることで合意
* 大阪リージョンの利用にはControl Tower / SCPの変更が必要で、適用だけで約**45**分かかるため、まずそこから着手する方針
* 納品ドキュメントはまだ未作成 — 提案書の内容をもとに作成が必要


#### DR手順書のレビュー
* たむさんがTerraformのプルリクを提出済みで、DR手順書が含まれている
* 実行環境（ローカル vs ワークスペース）の違いによる影響は小さいとShingo判断
* プルリクのレビューをMichaelに依頼


#### 検証項目の絞り込み
* **20TB**転送の時間計測は除外 — コストに見合わず、結果も環境依存で正確な数値にならないため
* 検証の目的は「できる・できない」の確認に絞る
* 具体的に確認すべき点として、Terraformの依存関係によるエラーやリソース上限（クォータ緩和）の有無を挙げた


#### Terraformコードの検証
* Michaelは生成されたコードが一発で通る可能性は低いと見ている
* 通常の進め方として、低レイヤー（VPC → IAM/SG）から段階的に適用して修正していく方針
* Shingoは**6月末**を待たずに早めに完成させたい意向


#### アカウントと大阪リージョンの準備
* テスト用アカウントはSection-9ではなくH2OのModernization組織配下に**2**つ作成する
* 大阪リージョンが現在制限されているため、Control Tower / SCPの変更が必要 — 適用に約**45**分、失敗時は巻き戻しも発生しうる
* クロスアカウント構成になるためKMS対応も必要；ADは今回のスコープ外；FSxの復元可否は検証が必要
* まずControl Tower / SCPの整備からスタートし、その後アカウントを作成して大阪リージョンを有効化する流れ（来週**3月9日**週に実施予定）


#### 納品ドキュメントの作成
* 確認したところ納品用ドキュメントはまだ作成されていない
* RFPは存在するが、それは納品ドキュメントではない
* 提案書の内容をもとに納品用ドキュメントを作成する必要がある