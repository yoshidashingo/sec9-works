# Sec9 Works

sec9（株式会社セクションナイン）が、顧客のビジネス要件に対するアセスメントを実施・蓄積するリポジトリ。Claude Codeを活用した開発・運用を前提とする。

## 前提条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) がインストールされていること
- リポジトリをクローンし、ルートディレクトリで `claude` コマンドを実行できること

## リポジトリ構成

```
.
├── CLAUDE.md                    # Claude Codeへの指示書（プロジェクト規約）
├── README.md                    # 本ファイル
├── .gitignore
├── .claude/                     # Claude Code設定
│   ├── settings.local.json
│   └── commands/                # カスタムスラッシュコマンド
├── .steering/                   # AI-DLCフレームワーク定義
│   ├── aws-aidlc-rules/         #   コアワークフロー（変更不可）
│   ├── aws-aidlc-rule-details/  #   ベースレイヤー（変更不可）
│   ├── sec9-aidlc-rule-details/ #   Sec9拡張レイヤー
│   ├── service-design-rule-details/ # サービスデザインルール
│   ├── technical-writing-rule-details/ # テクニカルライティングルール
│   └── email-writing-rules.md   #   メール・商談ルール
├── output/                      # 成果物格納先
│   ├── {YYYYMMDD}_{company}/    #   クライアントワーク（アセスメント）
│   │   ├── aidlc-docs/          #     AI-DLC成果物
│   │   └── references/          #     参考資料
│   └── {project-name}/          #   個人PJ・執筆活動等
├── meetings/                    # ミーティング議事録（meetings/CLAUDE.md 参照）
└── scripts/                     # 自動同期スクリプト
```

## AI-DLC とは

本リポジトリでは **AI-DLC（AI-Driven Development Life Cycle）** というフレームワークに従ってアセスメントを進める。AI-DLCは、AIモデルがプロジェクトの複雑さやリスクに応じて必要なステージを判断し、適応的に実行する構造化されたワークフローである。

### 3フェーズ構成

| フェーズ | 目的 | 主なステージ |
|---------|------|------------|
| **INCEPTION** | WHAT/WHYの決定 | Workspace Detection, Requirements Analysis, Workflow Planning, Application Design, Units Generation |
| **CONSTRUCTION** | HOWの決定・実装 | Functional Design, NFR Requirements, Infrastructure Design, Code Generation, Build and Test |
| **OPERATIONS** | デプロイ・運用 | （将来拡張用プレースホルダー） |

### ルールの二層構造

AI-DLCのルール詳細は二層で管理されている:

- **ベースレイヤー** (`aws-aidlc-rule-details/`): AI-DLC標準ルール。**変更不可**。
- **拡張レイヤー** (`sec9-aidlc-rule-details/`): Sec9独自の知見・ノウハウ・サービスメニュー。ベースレイヤーを上書きせず補完・拡張する。

Claude Codeは各ステージ実行時に両レイヤーのルールを自動的に読み込み、統合して適用する。

## 利用方法

### 新しいアセスメントの開始

1. リポジトリルートで Claude Code を起動する:
   ```
   claude
   ```

2. Claude Codeに対して、アセスメント対象の概要を伝える:
   ```
   新しい案件として{顧客名}についてAI-DLCでアセスメントを開始したい。
   状況は...
   ```

3. Claude Code が `CLAUDE.md` のルールに従い、AI-DLCワークフローを自動的に開始する:
   - `output/{YYYYMMDD}_{company}/aidlc-docs/` ディレクトリが自動作成される
   - INCEPTION フェーズから順にステージが実行される
   - 各ステージで承認ゲートが設けられ、方向性を確認しながら進行する

### 既存アセスメントの再開

Claude Code を起動すると、`aidlc-state.md` を検出して前回の続きから再開できる。

### 参考資料の格納

顧客から提供された資料やプロジェクトの参考情報は、各案件の `references/` ディレクトリに格納する。Claude Code はこれらを読み込んで分析に活用する。

## 成果物の管理

- `output/` ディレクトリは `.gitignore` で管理対象外としている（顧客の機密情報を含むため）
- 必要に応じて案件ごとに別途バックアップや共有手段を用意すること
- 各アセスメントは独立しており、他のアセスメントの成果物には影響しない

## 注意事項

- `.steering/aws-aidlc-rules/` および `.steering/aws-aidlc-rule-details/` 配下のファイルは**変更しないこと**
- `CLAUDE.md` はClaude Codeが参照するプロジェクト規約であり、変更する場合は合意を取ること
- Sec9拡張レイヤー (`sec9-aidlc-rule-details/`) の更新はSec9社内の知見に基づいて行う
