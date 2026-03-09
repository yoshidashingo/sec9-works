# LC-09. Building Multi-Agent Applications with Deep Agents

- **著者**: Sydney Runkle, Vivek Trivedy
- **公開日**: 2026-01-21（最終更新: 2026-02-13）
- **URL**: https://blog.langchain.com/building-multi-agent-applications-with-deep-agents/
- **重要度**: ★★
- **関連章**: 第3章, 第6章

## 概要

複雑なタスクを複数の専門化されたエージェントに分散するDeep Agentsフレームワークの2つの主要プリミティブ（Subagents と Skills）を紹介。

## 主要コンセプト

### 1. Subagents（サブエージェント）

**対処する問題**: 「コンテキストの肥大化」— エージェントのコンテキストウィンドウがほぼ満杯になる状況

**用途**:
- 複数ステップの作業委譲
- ドメイン特化の実装
- 異なるモデルの使用
- 並列化による遅延削減

**実装例**:
```python
research_subagent = {
    "name": "research-agent",
    "description": "深い質問をより詳しく調査するために使用",
    "system_prompt": "優れた研究者です",
    "tools": [internet_search],
    "model": "openai:gpt-4o"
}
```

**ベストプラクティス**:
- 明確な説明文の記述
- 詳細なシステムプロンプトの設定
- 必要なツール集の最小化

### 2. Skills（スキル）: 段階的能力開示

SKILL.mdファイルで特化した能力を定義するパターン。

**特徴**:
- スキル説明は事前にコンテキストに読み込まれる
- 詳細な指示は必要時のみ読み込まれる
- agentskills.io仕様に準拠

**ファイル構造**:
```
.deepagents/skills/
├── deploy/SKILL.md
└── review-pr/SKILL.md
```

### 3. パターン選択ガイドライン

| 必要な処理 | 推奨パターン |
|----------|----------|
| 複雑な多段階作業の委譲 | Subagents |
| 手続きの再利用 | Skills |
| 特定タスク用の専門ツール | Subagents（焦点ツール） |
| 複数エージェント間の共有能力 | Skills |
| 大規模ツール集の管理 | Skills |

## 理論的根拠

Anthropicの「コンテキスト回転」に関する研究とHumanLayerの「dumb zone」概念を参照。両パターンの組み合わせも推奨。
