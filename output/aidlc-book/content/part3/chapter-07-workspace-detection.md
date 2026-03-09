# Chapter 7: Workspace Detection — プロジェクトの起点

---

**この章で学ぶこと**

- Workspace Detectionが「なぜ」AI-DLCの最初のステップなのか
- GreenfieldとBrownfieldの違いと、それがワークフローにどう影響するか
- `aidlc-state.md` と `audit.md` の役割と構造
- Claude Code を使ってECサイトプロジェクト（BookCart）を初期化する方法

---

## 7.1 Workspace Detectionとは

AI-DLCを使った開発は、必ず **Workspace Detection** から始まります。

「検出」と聞くと、何か難しいことをしているように聞こえるかもしれません。しかし実際にはシンプルな問いへの答えです。

> **「これは新しいプロジェクトなのか、それとも既存のプロジェクトなのか？」**

この答えによって、AI-DLCが選択するワークフローが大きく変わります。

### 7.1.1 GreenfieldとBrownfieldの定義

AI-DLCは、プロジェクトを2種類に分類します。

**Greenfield（グリーンフィールド）**

白紙の状態から始まる新規開発プロジェクトです。既存のコードベースは存在しません。フィールド（土地）が緑の草で覆われた何もない状態、つまり「まっさらな状態」というメタファーに由来します。

本パートのメインシナリオ（BookCart）はGreenfieldです。

**Brownfield（ブラウンフィールド）**

すでに稼働しているシステムが存在し、そこに手を加えるプロジェクトです。既存のコードベース、データベース、インフラが存在します。「枯れた土地」に建物を建てるイメージです。

Chapter 8では、Brownfieldの典型例として「レガシーECサイトを引き継いだケース」を扱います。

### 7.1.2 なぜ最初に判定するのか

GreenfieldとBrownfieldでは、その後のワークフローが根本的に異なります。

| ステージ | Greenfield | Brownfield |
|---------|-----------|-----------|
| Workspace Detection | 実行（新規初期化） | 実行（既存を検出） |
| **Reverse Engineering** | **スキップ** | **必須実行** |
| Requirements Analysis | 実行 | 実行 |
| 以降のステージ | 同じ | 同じ |

Brownfieldでは、既存のコードを理解する「Reverse Engineering」ステージが必要になります。これをスキップすると、AIが既存の仕様を誤解してコードを壊す可能性があります。最初の判定は、このリスクを防ぐために不可欠です。

---

## 7.2 検出プロセスのしくみ

### 7.2.1 Claude Codeがワークスペースを読み取るしくみ

Claude Codeは、AI-DLCを開始する指示を受けると、まず以下を確認します。

1. **カレントディレクトリの状態** — 既存ファイルの有無、コードの量
2. **CLAUDE.mdの内容** — プロジェクト規約や既存の指示がないか
3. **`.steering/`ディレクトリの有無** — AI-DLCのルールファイルが配置されているか

これらの情報を総合的に判断して、GreenfieldかBrownfieldかを自動判定します。

### 7.2.2 aidlc-state.mdの構造と意味

Workspace Detectionが完了すると、`aidlc-state.md`が生成されます。これはAI-DLCの「現在地」を記録するトラッキングファイルです。

```markdown
# AI-DLC State Tracking

## Project Information
- **Project Name**: BookCart（ECサイト）
- **Project Type**: Greenfield
- **Start Date**: 2026-03-01T00:00:00Z
- **Current Stage**: INCEPTION - Workspace Detection (Complete)

## Workspace State
- **Existing Code**: No
- **Reverse Engineering Needed**: No
- **Workspace Root**: /path/to/bookcart/

## Stage Progress

### 🔵 INCEPTION PHASE
- [x] Workspace Detection
- [ ] Requirements Analysis
...
```

主要なフィールドを解説します。

| フィールド | 意味 |
|-----------|------|
| `Project Type` | Greenfield または Brownfield |
| `Existing Code` | 既存コードの有無 |
| `Reverse Engineering Needed` | REが必要かどうか |
| `Workspace Root` | プロジェクトのルートディレクトリ |
| `Stage Progress` | 各ステージの完了状況（[x]/[ ]） |

`aidlc-state.md`は、会話をまたいでセッションが変わっても、AIがプロジェクトの現在地を正確に把握するためのランドマークです。

### 7.2.3 audit.mdによるトレーサビリティ

もうひとつ生成されるファイルが`audit.md`です。

```markdown
# AI-DLC Audit Log

## Workspace Detection
**Timestamp**: 2026-03-01T10:00:00Z
**User Input**: "AI-DLCを使ってECサイトを開発したいです。始めてください。"
**AI Response**: Workspace Detectionを実行。ディレクトリが空であることを確認し、
Greenfieldプロジェクトと判定。aidlc-state.md と audit.md を初期化。
**Context**: INCEPTION - Workspace Detection 完了。次は Requirements Analysis へ。
```

`audit.md`は、AIとユーザーのやり取りをすべて時系列で記録します。「なぜこの設計にしたのか」「いつ誰が承認したのか」が後から追えるため、チーム開発や長期プロジェクトで特に重宝します。

---

> **[コラム] aidlc-state.md はなぜ必要か — Claude Codeのコンテキスト管理のしくみ**
>
> Claude Codeとの会話セッションには、コンテキストウィンドウ（一度に扱える情報量）の上限があります。長いプロジェクトでは、昨日の会話の内容を「忘れて」しまうことがあります。
>
> `aidlc-state.md`はこの問題を解決します。セッションの始まりにClaude Codeが`aidlc-state.md`を読み込むことで、「前回どこまで進んだか」「次に何をすべきか」を即座に把握できます。
>
> これはAI-DLCの設計上の重要な工夫のひとつです。AIの弱点（長期記憶の欠如）をファイルシステムで補っているわけです。

---

## 7.3 ハンズオン: BookCartプロジェクトの初期化

ここからは実際に手を動かして、AI-DLCを開始する流れを体験します。

### 7.3.1 サンプルリポジトリのセットアップ

**目標**: Next.jsプロジェクトを作成し、AI-DLCを開始できる状態にする

**1. GitHubリポジトリの作成**

GitHubで`bookcart`という名前の新しいリポジトリを作成し、ローカルにクローンします。

```bash
git clone https://github.com/your-username/bookcart.git
cd bookcart
```

**2. Next.jsプロジェクトの初期化**

```bash
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

プロンプトへの回答例:
- Would you like to use TypeScript? → **Yes**
- Would you like to use Tailwind CSS? → **Yes**
- Would you like to use ESLint? → **Yes**
- Would you like to use App Router? → **Yes**

**3. `.steering/`ディレクトリの配置**

AI-DLCのルールファイルを配置します。本書のサポートリポジトリから`.steering/`ディレクトリをコピーするか、以下のコマンドで最小構成を作成します。

```bash
mkdir -p .steering/aws-aidlc-rules
mkdir -p .steering/aws-aidlc-rule-details/{common,inception,construction,operations}
```

`.steering/aws-aidlc-rules/core-workflow.md`（AI-DLCのマスターワークフローファイル）をサポートリポジトリから取得して配置してください。

**4. CLAUDE.mdの作成**

プロジェクトルートに`CLAUDE.md`を作成します。これはClaude Codeへのプロジェクト規約ファイルです。

```markdown
# CLAUDE.md - BookCart プロジェクト規約

## プロジェクト概要

書籍・雑貨を販売するB2C ECサイト（学習用サンプル）

## 技術スタック

- フロントエンド / バックエンド: TypeScript + Next.js（App Router）
- CSS: Tailwind CSS
- 言語: TypeScript

## AI-DLC 設定

- ワークフロー: `.steering/aws-aidlc-rules/core-workflow.md`
- ルール詳細: `.steering/aws-aidlc-rule-details/`

## 言語

- ドキュメント: 日本語
- コード・技術用語: 英語
```

### 7.3.2 Workspace Detectionの実行

**目標**: Claude CodeがGreenfieldと判定する流れを観察する

Claude Codeを起動して、以下のように指示します。

```
AI-DLCを使ってECサイトの開発を始めたいです。まずWorkspace Detectionを実行してください。
```

Claude Codeは以下の手順で動きます。

1. カレントディレクトリを確認（Next.jsの初期ファイルが存在、`aidlc-state.md`は未生成）
2. `CLAUDE.md`を読み込み
3. `.steering/aws-aidlc-rules/core-workflow.md`を読み込み
4. Greenfieldと判定（既存のアプリケーションコードなし）
5. `aidlc-state.md`と`audit.md`を生成

**確認ポイント**:
- プロジェクトルートに`aidlc-docs/`ディレクトリが生成されたか
- `aidlc-docs/aidlc-state.md`に`Project Type: Greenfield`が記録されているか
- `aidlc-docs/audit.md`にWorkspace Detectionのログが記録されているか

### 7.3.3 生成成果物のレビュー

生成された`aidlc-state.md`を開いて、各フィールドを確認しましょう。

```bash
cat aidlc-docs/aidlc-state.md
```

以下の点を確認してください。

| 確認項目 | 期待値 |
|---------|-------|
| `Project Type` | `Greenfield` |
| `Existing Code` | `No` |
| `Reverse Engineering Needed` | `No` |
| `Current Stage` | `INCEPTION - Workspace Detection (Complete)` |

`Project Type`が`Brownfield`と判定された場合は、既存コードを別ディレクトリに移動するか、AIに「Greenfieldプロジェクトとして扱ってください」と明示的に指示してください。

---

## まとめ

- **Workspace Detection** は、GreenfieldとBrownfieldを自動判定するAI-DLCの最初のステージ。
- **Greenfield** は新規開発、**Brownfield** は既存システムへの追加・修正。両者でその後のワークフローが変わる。
- **`aidlc-state.md`** はAIの「現在地」を記録するトラッキングファイルであり、セッションをまたいで状態を保持する。
- **`audit.md`** はAIとユーザーのやり取りを時系列で記録し、意思決定のトレーサビリティを担保する。
- CLAUDE.mdと`.steering/`ディレクトリを正しく配置することで、Claude CodeがAI-DLCのルールに従って動作する。

---

## チェックリスト

- [ ] GitHubリポジトリを作成してNext.jsプロジェクトを初期化した
- [ ] `.steering/`ディレクトリとAI-DLCルールファイルを配置した
- [ ] `CLAUDE.md`を作成してプロジェクト規約を記述した
- [ ] Claude Codeに「Workspace Detectionを実行して」と指示した
- [ ] `aidlc-docs/aidlc-state.md`が生成され、`Project Type: Greenfield`が記録されていることを確認した
- [ ] `aidlc-docs/audit.md`にWorkspace Detectionのログが記録されていることを確認した
