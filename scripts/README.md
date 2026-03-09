# 自動同期スクリプト

## 概要

このディレクトリには、各種データソースから自動的に情報を取得・同期し、GitHubに自動コミット・プッシュするスクリプトが含まれています。

## アーキテクチャ

```
sync-all-cron.sh          ← crontabから呼ばれる唯一のエントリポイント
  ├── sync-meetings-cron.sh    (tldv + circleback)
  ├── sync-paulo-cron.sh       (gmail → paulo newsletter)
  └── sync-market-hack-cron.sh (gmail → market hack magazine)

git-sync-helper.sh        ← 共通git操作（ロック・stash・push リトライ）
```

### 自動化の流れ

1. `sync-all-cron.sh` が3つの同期スクリプトを**順次実行**
2. 各スクリプトがClaude Codeでデータソースから最新情報を取得
3. `git-sync-helper.sh` が排他ロック付きでcommit & push

## スクリプト一覧

### sync-all-cron.sh（エントリポイント）
- **目的**: 全同期スクリプトの順次実行ラッパー
- **実行時間**: 毎晩 1:00
- **機能**: プロセスロック（`/tmp/assessment-sync-all.lock`）で重複実行を防止

### sync-meetings-cron.sh
- **目的**: GA社（tldv）とSec9社（circleback）の議事録を自動同期
- **出力先**: `output/ga/meetings/`, `output/sec9/meetings/`

### sync-paulo-cron.sh
- **目的**: Pauloニュースレターの記事を自動取得
- **出力先**: `output/shingo/paulo-newsletter/`

### sync-market-hack-cron.sh
- **目的**: Market Hack Magazineの記事を自動取得
- **出力先**: `output/shingo/market-hack-magazine/`

### git-sync-helper.sh（共通ヘルパー）
- **目的**: git操作の排他制御・安全なcommit & push
- **機能**:
  - ロックファイル（`/tmp/assessment-git.lock`）で排他制御
  - `git stash` → `git pull --rebase` → `git stash pop` でunstaged changes安全処理
  - push失敗時は `git pull --rebase` してリトライ（最大3回）

## launchd設定

crontabの代わりにmacOS推奨のlaunchdを使用。

```bash
# 登録済みplistファイル
~/Library/LaunchAgents/com.shingo.assessment-sync.plist
# 毎日 01:00 に sync-all-cron.sh を実行

# 状態確認
launchctl list | grep assessment-sync

# 手動登録（初回・再起動後など）
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.shingo.assessment-sync.plist

# 登録解除
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.shingo.assessment-sync.plist
```

## ログ

各スクリプトの実行ログは `logs/` ディレクトリに保存されます：
- `logs/sync-all_YYYYMMDD_HHMMSS.log` — ラッパー全体ログ
- `logs/sync-meetings_YYYYMMDD_HHMMSS.log`
- `logs/sync-paulo_YYYYMMDD_HHMMSS.log`
- `logs/sync-market-hack_YYYYMMDD_HHMMSS.log`

ログは30日以上経過したものが自動的に削除されます。

## 手動実行

```bash
# 全体を順次実行
./scripts/sync-all-cron.sh

# 個別実行
./scripts/sync-meetings-cron.sh
./scripts/sync-paulo-cron.sh
./scripts/sync-market-hack-cron.sh
```

## トラブルシューティング

### スクリプトが実行されない場合

1. 実行権限を確認
   ```bash
   ls -la scripts/*.sh
   ```

2. cron設定を確認
   ```bash
   crontab -l
   ```

3. ログファイルを確認
   ```bash
   tail -f logs/sync-all_*.log
   ```

4. 手動実行してエラーを確認
   ```bash
   bash -x ./scripts/sync-all-cron.sh
   ```

### ロックファイルが残っている場合

プロセスが異常終了するとロックファイルが残ることがあります。5分（git lock）/ 1時間（sync-all lock）でタイムアウトしますが、手動削除も可能です：

```bash
rm -f /tmp/assessment-git.lock /tmp/assessment-sync-all.lock
```

### macOSでの注意事項

#### Full Disk Access権限

macOSでcronを動作させるには、ターミナルアプリまたは`cron`デーモンにFull Disk Access権限が必要な場合があります。

1. **システム設定** > **プライバシーとセキュリティ** > **フルディスクアクセス**
2. `cron` または使用しているターミナルアプリを追加
