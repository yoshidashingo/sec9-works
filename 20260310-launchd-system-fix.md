# launchd 定期タスク修正記録 (2026-03-10)

## 対象タスク

| ジョブ | plist | スケジュール | 内容 |
|--------|-------|-------------|------|
| `com.sec9.sync-meetings` | `~/Library/LaunchAgents/com.sec9.sync-meetings.plist` | 毎日 23:00 | Circleback/tldv 議事録を Google Drive から同期 |
| `com.sec9.sync-magazines` | `~/Library/LaunchAgents/com.sec9.sync-magazines.plist` | 毎日 00:00 | Gmail からメルマガを取得・保存 |

## 発生していた問題

両タスクとも launchd から実行すると失敗していた。

### 問題1: macOS TCC (Transparency, Consent, and Control) によるアクセス拒否

**症状:**

```
shell-init: error retrieving current directory: getcwd: cannot access parent directories: Operation not permitted
/bin/bash: /Users/shingo/Documents/GitHub/sec9-works/.claude/scripts/sync-meetings-cron.sh: Operation not permitted
```

```
/Library/Developer/CommandLineTools/usr/bin/python3: can't open file '...': [Errno 1] Operation not permitted
```

**原因:**

macOS の TCC (プライバシー保護機構) が `~/Documents/` ディレクトリへのアクセスを制御している。launchd から起動されるプログラム（`/bin/bash`, `/usr/bin/python3`）は、ユーザーが明示的にフルディスクアクセスを許可しない限り `~/Documents/` 配下のファイルを読み書きできない。

ターミナルから直接実行すると Terminal.app にフルディスクアクセスが付与されているため問題なく動作するが、launchd は Terminal.app を経由せず直接プログラムを起動するため TCC の制限を受ける。

**対策:**

「システム設定 > プライバシーとセキュリティ > フルディスクアクセス」に以下を追加:

- `/bin/bash`（sync-meetings で使用）
- `/usr/bin/python3`（sync-magazines で使用）

### 問題2: launchd の StandardOutPath/StandardErrorPath が `~/Documents/` 内を指定

**症状:**

フルディスクアクセスを付与しても、plist の `StandardOutPath` / `StandardErrorPath` が `~/Documents/GitHub/sec9-works/logs/` を指している場合、launchd がログファイルを開く段階（スクリプト実行前）で失敗する。`LastExitStatus = 19968`（exit code 78）が返り、ログは一切書き込まれない。

**原因:**

launchd デーモンがログファイルを開く処理は、ProgramArguments で指定したプログラムのフルディスクアクセス権限とは別に評価される。`~/Documents/` はユーザーのプライバシー保護対象ディレクトリのため、launchd のリダイレクト先としては使用できない。

**対策:**

ログ出力先を TCC 保護外のディレクトリに変更:

```
変更前: /Users/shingo/Documents/GitHub/sec9-works/logs/sync-meetings-*.log
変更後: /Users/shingo/.local/log/sync-meetings-*.log
```

### 問題3: Google Workspace CLI (gws) の認証情報が復号できない

**症状:**

```json
{
  "encryption_valid": false,
  "encryption_error": "Could not decrypt. May have been created on a different machine."
}
```

`gws auth login` を何度実行しても `credentials.enc` が復号できない。

**原因:**

gws は認証情報を AES-256-GCM で暗号化し `~/.config/gws/credentials.enc` に保存する。暗号化キーは macOS Keychain（サービス名: `gws-cli`, アカウント: `encryption-key`）に格納される設計だが、Keychain への書き込みがサイレントに失敗していた。

結果、暗号化された `credentials.enc` は作成されるが、復号に必要なキーが Keychain に存在しないため、常に復号エラーとなる。gws にはフォールバックとして `~/.config/gws/.encryption_key` ファイルへの保存機構もあるが、これも機能していなかった。

**対策:**

手動で OAuth2 認証フローを実行し、平文の `credentials.json` を作成:

1. `client_secret.json` から client_id/client_secret を取得
2. OAuth2 認証 URL を生成してブラウザで認証
3. 認証コードを `https://oauth2.googleapis.com/token` に送信して refresh_token を取得
4. `authorized_user` 形式の `~/.config/gws/credentials.json` を作成
5. 壊れた `credentials.enc` を削除

gws は以下の優先順位で認証情報を探す:

1. `GOOGLE_WORKSPACE_CLI_TOKEN` 環境変数（アクセストークン）
2. `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` 環境変数（credentials ファイルパス）
3. `~/.config/gws/credentials.enc`（暗号化）
4. `~/.config/gws/credentials.json`（平文）

`.enc` が存在すると復号を試みてエラーになるため、削除が必要。

### 問題4: launchd 環境で gws の認証情報が参照できない

**症状:**

launchd からスクリプトを実行すると `gws drive files list` が無応答でタイムアウト。

**原因:**

sync-meetings スクリプトは `.env.gws` から `GOOGLE_WORKSPACE_CLI_CLIENT_ID` と `GOOGLE_WORKSPACE_CLI_CLIENT_SECRET` を読み込むが、`GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`（refresh_token を含む認証情報ファイルのパス）が設定されていなかった。launchd 環境では Keychain アクセスもできないため、gws が認証情報を見つけられない。

**対策:**

1. `.env.gws` に `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` を追加
2. 両 plist の `EnvironmentVariables` にも同変数を追加:

```xml
<key>GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE</key>
<string>/Users/shingo/.config/gws/credentials.json</string>
```

## 修正したファイル一覧

| ファイル | 修正内容 |
|---------|---------|
| `~/Library/LaunchAgents/com.sec9.sync-meetings.plist` | ログ出力先を `~/.local/log/` に変更、`GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` 環境変数追加 |
| `~/Library/LaunchAgents/com.sec9.sync-magazines.plist` | 同上 |
| `.env.gws` | `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` 追加 |
| `~/.config/gws/credentials.json` | 手動 OAuth フローで新規作成（平文） |
| `~/.config/gws/credentials.enc` | 削除（復号不能のため） |

## 動作確認結果

### sync-meetings

```
=== 2026-03-10 19:37:20 議事録同期開始 ===
増分同期: 2026-03-09T10:28:51.000Z 以降の更新を取得
対象ファイル: 6件
  [1/6] スキップ(同一): 2026-03-10_Cclbk_VINX様週次定例
  ...
=== 同期結果 ===
新規: 0件、スキップ: 6件、エラー: 0件
LastExitStatus = 0
```

### sync-magazines

```
増分同期: 2026/03/08 以降のメルマガを取得
--- Market Hack Magazine ---
  [1/3] 保存: 2026-03-09_market-hack_トランプ大統領「イランへの攻撃はほぼ完了した」.md
  ...
=== 同期結果 ===
新規: 1件、スキップ: 3件、エラー: 0件
commit & push 完了
LastExitStatus = 0
```

## 今後の注意事項

- **gws の credentials.json は平文**のため、git にコミットしないこと（`.gitignore` で除外済み）
- **macOS アップデート後**にフルディスクアクセスの設定がリセットされる場合がある。タスクが失敗したら最初にフルディスクアクセスの設定を確認すること
- **gws のバージョンアップ**で Keychain 問題が修正された場合は、`credentials.enc` に戻すことを検討
