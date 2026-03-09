# /sync-meetings - ミーティング議事録同期

`meetings/CLAUDE.md` の同期ルールに従い、Google Drive から更新されたミーティング議事録を `meetings/` に同期する。

## 手順

1. `meetings/CLAUDE.md` を読み込み、同期ルールを確認する
2. Workspace CLI を実行して Google Drive フォルダから新規・更新ファイルを取得する

```bash
npx @anthropic-ai/workspace-cli gdrive \
  --folder-id 1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq \
  --output meetings/
```

3. 同期結果のサマリーを表示する（新規・更新・スキップ件数）
