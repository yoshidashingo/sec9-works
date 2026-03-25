https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7509602.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260324%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260324T235624Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=4a23db57ca7d6b4d4ea0a96adfce5a1b0f6a798e3513c37560c9f1b083a72a0bd952ea063949e7ac8e162b90d3ae3f9b3f1d07685d643171125d1d5d709d8784e61964bcf0e4c51e818fa7c5598373e273b9e543db174b639fa76d42b15be61c838d15435124b5df9b150f7d03ada96efae49e99d0d068ebe5a76603cdad6d0f83a6b7e481910e644dbe610d0fccb1f2d7df66368764492dbb721c8889c7b43e4de83aecccc6608ab6a0098d4999b427eb9a00956722f64a9dc27b0400d1c74a772a2aea4af9067511dc2421b691b440fc4daa88bcb0e50b7c03c21edb4f55397488cc40217c425ba000cae164ac794ea1b6413302a610dda52a3d0ddc19deda


#### 概要
* デプロイ問題は解消済み、過去のPR（**2**件のレビュー待ちを除く）はすべてデプロイ完了
* ストーリーボットの画像生成は、OpenAI APIキーが最新モデルに対応していないためブロック中
* 吉田真吾がストーリーボードUIを全面的に作り直す方針を示し、スプレッドシート形式の新しい設計イメージを共有


#### デプロイ修正とPRの状況
* 前回のデプロイ失敗の原因は、吉田真吾が導入したテストライブラリとReactバージョンの競合だった
* Tangがバージョンを変更して競合を解消し、過去のPRはすべてデプロイ済み
* 現在レビュー待ちのPRが**2**件残っている


#### 画像生成モデルのAPIキー問題
* ストーリーボットで画像を生成すると**4**枚出力されるが、内容がほぼ同じという問題がある
* 原因はOpenAIの画像生成モデル名の変更で、Tangがモデル名を修正したが、現在のAPIキーでは最新の画像生成モデルが使えない
* 最新モデルに対応した新しいOpenAI APIキーが必要で、それが揃うまでテストは不可


#### ストーリーボードUIの再設計
* 吉田真吾は現在のUIでは方向性が違うとして、作り直しが必要と判断
* 目指す形はExcelのようなスプレッドシート形式で、シーン1・シーン2・シーン3…と列で並べる構成
* 各シーンには手書きスケッチ・画像・動画の**3**要素を持たせ、最終的にすべての動画を結合して1本の長い動画にする
* 現在の「Turbo / HiFi」オプションは意味がないと吉田真吾は考えており、削除方向
* 吉田真吾がGoogle Sheetsでイメージを画面共有し、レイアウトの方向性を確認した