https://storage.googleapis.com/saved-meeting-recording.prod.circleback.ai/meeting_7149790_7149791.mp4?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=circleback-ai%40appspot.gserviceaccount.com%2F20260310%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260310T005317Z&X-Goog-Expires=86400&X-Goog-SignedHeaders=host&X-Goog-Signature=67b24f8e665b994b5ab7ca66218f9db67e384aa679f44550f368d179112bb7b1cef21768602931cb258bdf5893c91637ba6727de277039331afcd15fad1d6fd27890d7f93e68135a3d75ee53910309038d1276f643af4f3d6b7aa116a25471921ed0d61e1edf8dcc5041b57b4773d7904762b18e02312729c18adba3944bbef4b1f7b8f91ff8a9bfea66c6c2c0e4f5698ad331ecf06eb762b342fcede9f4b75d46b45df4280d59c62c13ad1b0771889326a4dfa0a2936f6a866d070d30d7f31b53bef21feb26f707929e8c1fd4f81b76f619105411a24469a863536b50e94a2586caa787b8b72db5188680a9049ffbb86172e3568e33e1d2940584aa3ad26f39


#### 概要
* 廣瀬AFTアカウントの不要リソース削除は完了、クロージャーはこれから
* クロージャー前にEFSが**4**つ（合計約**680**GB）残っており、要否確認が必要
* Michaelがドキュメントへの調査結果の反映を引き受けた


#### 廣瀬AFTアカウントのクロージャー進捗
* 不要リソースの削除は完了済み
* アカウントのクロージャーはまだ実施していない
* EFSの扱いが未解決のため、クロージャーは保留中


#### EFSリソースの扱い
* 対象のEFSは**4**つ、合計約**680**GBで、内訳は以下：
* 半球サービスウェブEFS
* 半芯サービスウェブ（MDAware）
* CMEFS（「俺に」と記載あり）
* アイダス（約**300**GB）— ビリングはCommon ETLのため、ETL用途と推定
* ICS関連のEFS（**36**TB）はつながっていなさそうで、ICSにマウントされているものとして不要と判断
* Athenaは**1**個あるが、ベースとなるS3はクロスリージョンコピーで対応するため問題なし
* 一旦すべてリストに含めておき、実際の移行作業の中で本当に必要かどうかを確認していく方針
* Michaelが調査結果を資料に反映する予定（現時点では未反映）