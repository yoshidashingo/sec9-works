# magazines/ - メルマガアーカイブ

## 同期ソース

Gmail から `gws` CLI（Google Workspace CLI）で取得し、マークダウンに変換する。

## 対象メルマガ

| メルマガ名 | 検索クエリ | 差出人 |
|-----------|-----------|--------|
| Market Hack Magazine | `from:noreply@note.com subject:"Market Hack Magazine"` | note (広瀬隆雄) |
| パウロのメルマガ | `from:noreply@note.com "パウロのAIバブルを精査するメンバーシップ"` | note (パウロ) |

## 同期コマンド

```bash
/sync-magazines
```

または直接スクリプトを実行:

```bash
python3 .claude/scripts/sync-magazines.py
```

## 増分同期の仕組み

1. `magazines/_sync-state.json` で最終同期日時を管理
2. Gmail API で基準日以降のメルマガを検索
3. HTMLメール本文から記事テキストを抽出し、html2text でマークダウンに変換
4. 同一内容のファイルはスキップ

## ファイル命名規則

```
{YYYY-MM-DD}_{source}_{sanitized-subject}.md
```

- `source`: `market-hack` または `paulo`
- 件名から不要な定型文を除去

例: `2026-03-08_market-hack_イランの濃縮ウランは無傷.md`
