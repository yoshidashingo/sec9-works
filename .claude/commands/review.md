# /review - Codex によるコードレビュー

`codex review` を使ってコードを非インタラクティブにレビューする。

## 引数の解釈

`$ARGUMENTS` を解析する:

- 引数なし → uncommitted 変更（staged + unstaged + untracked）をレビュー
- `--base <branch>` → 指定ブランチとの差分をレビュー
- `--commit <sha>` → 指定コミットの変更をレビュー
- その他のテキスト → カスタムレビュー指示として `codex review` に渡す

## 重要な制約

`codex review` は **`--uncommitted` / `--base` / `--commit` フラグと PROMPT を同時に使えない**。

## 実行手順

### ステップ1: コマンドの分岐

`$ARGUMENTS` をもとに以下のルールで分岐する:

| 引数の内容 | 使うコマンド |
|-----------|------------|
| 引数なし | `codex review --uncommitted` |
| `--base <branch>` のみ | `codex review --base <branch>` |
| `--commit <sha>` のみ | `codex review --commit <sha>` |
| それ以外のテキスト（ファイル名・指示など） | `codex review "<テキスト>"` ※フラグなし |

### ステップ2: codex review 実行

Bash ツールで実行する。

例:
- 引数なし → `npx --yes @openai/codex review --uncommitted`
- `--base main` → `npx --yes @openai/codex review --base main`
- `CLAUDE.md をレビューして` → `npx --yes @openai/codex review "CLAUDE.md をレビューして"`
- `セキュリティ観点で` → `npx --yes @openai/codex review "セキュリティ観点で"`

### ステップ3: 結果の提示

Codex の出力をそのままユーザーに提示する。エラーが発生した場合はエラー内容を表示し、考えられる原因（認証未設定、変更なし等）を案内する。

## 認証エラーが出た場合

以下を案内する:

```
codex login を実行して認証を完了してください:
npx @openai/codex login
```
