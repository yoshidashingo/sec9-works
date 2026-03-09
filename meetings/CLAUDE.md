# meetings/ - ミーティング議事録

## 同期ソース

Google Drive フォルダから `gws` CLI（Google Workspace CLI）で同期する。

- **Google Drive フォルダID**: `1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq`
- **CLI**: `gws` (`npm install -g @googleworkspace/cli`)

## 同期コマンド

```bash
/sync-meetings
```

または直接スクリプトを実行:

```bash
bash .claude/scripts/sync-meetings.sh
```

## 増分同期の仕組み

1. `meetings/` 内の最新ファイルの更新日時を基準にする（1日マージン付き）
2. Google Drive API で基準日以降に更新されたドキュメントを取得
3. 内容が同一のファイルはスキップ、変更があれば上書き、新規は追加

## ファイル命名規則

Google Docs のドキュメント名をそのまま使用し、以下のサニタイズのみ行う:

- `/` と `:` を `_` に置換
- 末尾のスペースを除去
- 拡張子 `.md` を付与

例: `2026-03-09_Cclbk_[H2O]コワーク.md`

## 定期実行

`/ralph-loop` で日次実行する場合:

```
/ralph-loop "/sync-meetings を実行して結果を報告" --max-iterations 1
```
