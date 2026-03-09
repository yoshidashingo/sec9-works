# パウロ メンバーシップ記事収集 HOWTO

## 概要

パウロ氏のnoteメンバーシップ「パウロのAIバブルを精査するメンバーシップ」の記事本文を、Gmailの通知メールから収集し `references/paulo-newsletter-articles.md` に蓄積する手順。

## 前提条件

- Sec9社のGoogleアカウントで shingo@sec9.co.jp 宛にnote通知が届いている
- MCPサーバー `google-workspace-sec9` が利用可能

## 自動収集

`scripts/sync-paulo-cron.sh` で自動収集される。手動実行も可能:

```bash
/Users/shingo/github/assessment/scripts/sync-paulo-cron.sh
```

## 手動収集手順

### 1. Gmailから記事メールを検索

```
ツール: mcp__google-workspace-sec9__search_gmail_messages
パラメータ:
  query: "from:noreply@note.com パウロ after:YYYY/MM/DD"
  user_google_email: "admin@sec9.co.jp"
  page_size: 10
```

### 2. メール本文をバッチ取得

```
ツール: mcp__google-workspace-sec9__get_gmail_messages_content_batch
パラメータ:
  message_ids: [検索結果のMessage IDリスト]
  user_google_email: "admin@sec9.co.jp"
  format: "full"
```

### 3. フィルタリング

- **採用**: From 表示名が「パウロ」のメールのみ
- **除外**: 購入確認、定期購読通知、他のnoteメール

### 4. references への書き込み

`references/paulo-newsletter-articles.md` に追記する。

記事フォーマット:
```markdown
## YYYY-MM-DD: 記事タイトル

記事本文（noteフッター「スキする」以降は除外）
```

- 日付降順（新しい記事が上）
- ヘッダーの記事数と期間を更新
