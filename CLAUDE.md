# CLAUDE.md - プロジェクト規約

## プロジェクト概要

sec9（株式会社セクションナイン）を経営するshingo（吉田真吾）がAI-DLCを活用して顧客のビジネス要件アセスメントを実施・蓄積するリポジトリ。Claude Codeによる開発・運用を前提とする。

## AI-DLC ワークフロー

コアワークフロー: `.steering/aws-aidlc-rules/core-workflow.md`（変更不可）
フェーズ: INCEPTION → CONSTRUCTION → OPERATIONS

### 各ステージ実行前のルール読み込み手順

1. `.steering/aws-aidlc-rule-details/` から該当ステージのルールファイルを読み込む（変更不可）
2. Sec9社の拡張レイヤーに同名・関連ファイルがあれば追加で読み込む
3. 競合時の優先順位: `core-workflow.md` のプロセスフロー > 拡張レイヤー > `aws-aidlc-rule-details`

**拡張レイヤー:** `.steering/sec9-aidlc-rule-details/`

## 成果物の出力先

`core-workflow.md` 内の `aidlc-docs/` はすべて以下のパスに読み替えること:

```
output/{YYYYMMDD}_{company}/aidlc-docs/
```

- **company**: アセスメント対象企業の略称（英字小文字）
- **YYYYMMDD**: アセスメント開始日

**パス読み替え例（h2o向けアセスメントの場合）:**
- `aidlc-docs/aidlc-state.md` → `output/20260213_h2o/aidlc-docs/aidlc-state.md`
- `aidlc-docs/inception/requirements/` → `output/20260213_h2o/aidlc-docs/inception/requirements/`

**新規アセスメント開始時:** `output/{YYYYMMDD}_{company}/aidlc-docs/` を新規作成する。各案件ディレクトリは独立しており他の案件に影響しない。

**個人プロジェクト・執筆活動等:** `output/{project-name}/` に格納する（日付プレフィックス不要）。

## MCPサーバー利用ルール

| MCPサーバー | 用途 |
|------------|------|
| backlog-st9 | Sec9社 Backlog |
| circleback | ミーティング議事録 |
| aws-documentation | AWS公式ドキュメント |

**メール・商談**: `.steering/email-writing-rules.md` に従うこと（メール送信禁止・日程調整・ライティングルール等）

## ディレクトリ構造

```
.steering/
  aws-aidlc-rules/
    core-workflow.md                    # マスターワークフロー（変更不可）
  aws-aidlc-rule-details/               # ベースレイヤー（変更不可）
    common/
    inception/
    construction/
    operations/
  sec9-aidlc-rule-details/              # Sec9拡張レイヤー
    introduction.md / company-profile.md / service-catalog.md
    services/
      cost-optimization.md / genai-development.md / platform-engineering.md
      serverless-modern-apps.md / talent.md
  service-design-rule-details/          # サービスデザインルール
  technical-writing-rule-details/       # テクニカルライティングルール
  email-writing-rules.md                # メール・商談ルール

output/
  {YYYYMMDD}_{company}/aidlc-docs/      # クライアントワーク（アセスメント）
  {project-name}/                       # 個人PJ・執筆活動等

meetings/                               # ミーティング議事録（下記ルール参照）

scripts/                                # 自動同期スクリプト
```

## ミーティング議事録の同期ルール

`meetings/` ディレクトリには、Workspace CLI（`npx @anthropic-ai/workspace-cli`）で以下の Google Drive フォルダから更新されたミーティングをマークダウンファイルとして保存する。

- **ソース**: https://drive.google.com/drive/folders/1GCMKVhvx0Lrz0H-lN9SyIebu01jEMIAq

## 言語

- ドキュメント・コミュニケーション: 日本語
- コード・技術用語: 英語（業界標準に従う）
