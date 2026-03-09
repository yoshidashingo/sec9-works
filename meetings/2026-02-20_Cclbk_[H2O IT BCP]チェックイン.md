https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_6773546.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260220%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260220T005426Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=601115cbbb070727f6ae9d82a7733564542b55bb5fe356482d84b0e3672394e51711779d7824edc7179cab65162d8f4916202eece30b8a92c4f39063b449c60d29e95943395071a54fdbfbf8890bb36a82920df5771f3cbef74e389ab8838f001db3e44a6ed3048ebef980fa6e6d4a1ae27161698c938aada8b8b34631a158184b0a3e28af56d9837b29f972164af350de8fbe44853694e7eaa5592cf190c385e61981f92eeed79df5298e4e6857797771c46ff6f103c3c87fa918993a667cf46a5c87569e89de49aca9534c83e1768a1ecf78650db61ced8f6e3c5ec74b433faa52789ec406ebd57d99b73467a1731d6e8abbb20e5dcc0bcd4f93703209d890


#### Overview
* NishiiがRDSバックアップコスト見積もりを更新し、プロビジョン容量分の無料枠を考慮した形に修正
* DR戦略として大阪リージョンへの日次バッチコピーを推奨—転送料とストレージコストは増えるがRPOを短縮可能
* **20TB**プロビジョン済みだが実際の使用量は**14TB**のため現在は同一リージョン内で課金なし
* **2月20日11:00 AM**に内部で詳細レビュー後、**2月20日午後**に浜野さんへ送付予定


#### RDSバックアップコスト見積もりの更新
* NishiiがRDSバックアップコスト見積もりを**2月19日**に更新し、プロビジョン容量分までの無料枠を考慮
* 現在は**3日分**のスナップショットのみ保持
* **60日間**保持する場合のストレージコストをシナリオとして試算
* **20TB**プロビジョン済みだが実際の使用量は**14TB**のため、同一リージョン内では課金が発生していない
* バックアップの変動率が不明なため、仮に**1%**の日次変更を想定してコスト試算


#### DR戦略オプションとRPO
* Nishiiが**2通り**のDR戦略オプションを用意
* オプション1: 東京リージョンで**60日間**バックアップを保持
* オプション2: 大阪リージョンへ日次バッチで転送—転送料と大阪でのストレージコストが発生するがRPOを短縮可能
* Nishiiは日次コピーを推奨—DR発動時に大阪の既存スナップショットから復元することで最も時間を短縮できる
* **18個**のイメージと**4つ**のRDSインスタンスを同時に操作する必要があり、作業量が多いため間違いのリスクも考慮
* **2月20日11:00 AM**に詳細をレビューし、**2月20日午後**に浜野さんへ送付予定