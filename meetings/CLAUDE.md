# meetings/ - ミーティング議事録

## 同期ソース

Google Drive フォルダから Workspace CLI で同期する。

- **Google Drive**: https://drive.google.com/drive/folders/1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq

## 同期手順

1. Workspace CLI で Google Drive フォルダ内のファイル一覧を取得する
2. `meetings/` 内の既存ファイルと比較し、新規・更新されたファイルを特定する
3. 新規・更新分をマークダウンファイルとして `meetings/` に保存する

```bash
npx @anthropic-ai/workspace-cli gdrive \
  --folder-id 1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq \
  --output meetings/
```

## ファイル命名規則

```
{YYYY-MM-DD}_{sanitized-meeting-name}.md
```

- 英数字・ハイフン・アンダースコアのみ残す
- スペースはハイフンに変換
- 日本語は除去
- 80文字で切り詰め、すべて小文字
- 同名・同日のファイルが既に存在する場合は末尾に `_2`, `_3` を付与
