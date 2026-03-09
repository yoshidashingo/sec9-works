# 技術的正確性レビュー: 第1章〜第5章

**レビュー日**: 2026-02-22
**対象**: chapter-01.md, chapter-02.md, chapter-03.md, chapter-04.md, chapter-05.md
**参照文献**: references.md (101件)

---

## 総合評価

第1章〜第5章は全体として高い技術的正確性を維持している。引用データは参照文献と整合しており、コード例のPython構文も正しい。用語の一貫性も良好である。以下、4つのレビュー観点ごとに詳細な所見を報告する。

---

## 1. 引用データ・数値の正確性

### 合格（正確と確認できた主要数値）

| 数値 | 出典 | 章・行 | 判定 |
|------|------|--------|------|
| Terminal Bench 2.0: 52.8→66.5、+13.7pt、Top 30→Top 5 | LC-08 | 第1章 1.1節 | 正確。references.mdのLC-08概要と完全一致 |
| 7人のエンジニア、5ヶ月、約100万行、1,500 PR | OAI-01 | 第1章 1.1節 | 正確。references.mdのOAI-01概要と一致 |
| 推論サンドイッチ: 全フェーズextra-high=53.9%、バランス型=63.6% | LC-08 | 第1章 1.1節、第3章 3.2節、第5章 5.3節 | 正確。LC-08概要の「推論サンドイッチ」パターン記述と一致 |
| LangChain調査: 1,340名回答、57.3%本番運用、89%オブザーバビリティ実装 | LC-05 | 第1章 1.3節 | 正確。references.mdのLC-05概要と一致 |
| 68%のエージェントが最大10ステップで人間介入必要 | ACD-06 | 第1章 1.3節 | 正確。references.mdのACD-06概要と一致 |
| 16並列Claudeインスタンス、10万行Cコンパイラ、約2,000セッション、$20,000 | ANT-12 | 第3章 3.3節 | 正確。references.mdのANT-12概要と一致 |
| MCP: トークン85%削減（約134kから約5k） | ANT-08 | 第3章 3.4節、第5章 5.3節 | 正確。references.mdのANT-08概要と一致 |
| 許可プロンプト84%削減（Claude Codeサンドボックス） | ANT-07 | 第4章 4.4節 | 正確。references.mdのANT-07概要と一致 |
| ジェイルブレイク成功率4.4%（Constitutional Classifiers） | ANT-18 | 第4章 4.4節 | 正確。references.mdのANT-18概要と一致 |
| AGENTS.md: 60,000以上のOSSプロジェクトに採用 | STD-02 | 第4章 4.1節、第5章 5.2節 | 正確。references.mdのSTD-02概要と一致 |
| DeepAgents CLI: Claude Sonnet 4.5使用時にTerminal Bench 2.0で平均42.65% | LC-16 | 第1章 1.3節 | 正確。references.mdのLC-16概要と一致 |
| thinkツール: 航空会社カスタマーサービスで54%の相対的改善 | ANT-05 | 第3章 3.4節 | 正確。references.mdのANT-05概要と一致 |
| Pan et al.: 26ドメイン、306名、20件のケーススタディ | ACD-06 | 第1章 1.3節 | 正確。references.mdのACD-06概要と整合 |
| 70%がプロンプティングベースのアプローチに依存 | ACD-06 | 第1章 1.3節 | 正確。出典ACD-06に帰属されており妥当 |
| Terminal Bench 2.0: 89タスク、4領域 | LC-16 | 第1章 1.1節 | 正確。LC-16概要と一致 |

### 要確認事項

| 項目 | 章・行 | 指摘内容 | 重要度 |
|------|--------|----------|--------|
| **「1日あたり平均3.5件のPR」** | 第1章 1.1節（行25付近） | OAI-01の参照文献概要には「約100万行・1,500 PRのソフトウェア製品を構築した」とあるが、「1人のエンジニアが1日あたり平均3.5件のプルリクエストをマージする」という具体的数値は、references.mdの概要には明記されていない。概算（1,500 PR / 7人 / 約60営業日 ≒ 約3.6件/人日）で整合はするが、OAI-01原文に明記されている数値かどうかの確認を推奨する。 | 中 |
| **「コンテキストウィンドウの使用率が95%に達した時点でauto-compact」** | 第2章 2.2節（行165付近） | 出典がLC-11に帰属されているが、この95%という閾値はClaude Codeの実装詳細であり、LC-11（LangChainの記事）が情報元として正確かどうか確認を推奨する。第5章比較表ではAnthropic Claude側の仕様として「auto-compact（95%閾値）」と記述されており整合はしている。 | 低 |
| **「Manusの開発チームが6ヶ月間でハーネスを5回書き直した」** | 第1章 1.1節（行33付近） | BLG-02に帰属されており、BLG-02とBLG-06の概要にも「Manusが5回書き直し」「6ヶ月で5回」と記載があるため整合する。ただしManusの公式情報としての裏取り可否は不明。 | 低 |
| **「74%が主に人間による評価に依存」** | 第1章 1.3節（行159付近） | ACD-06からの引用として扱われている。references.mdのACD-06概要には「68%が最大10ステップで人間介入を必要」は明記されているが、74%の数値は概要に明示されていない。ACD-06原文での確認を推奨する。 | 中 |
| **「GPT-5.2-Codex」をTerminal Bench 2.0実験で使用** | 第1章 1.1節（行41付近） | LC-08の概要に「モデル（GPT-5.2-Codex）を一切変更せず」と記載されており本文と一致する。ただしGPT-5.2-Codexというモデル名は一般に広く知られたものではなく、2026年Q1時点の最新情報として正確かどうかは原文依存。 | 低 |

---

## 2. コード例のPython構文エラー

### 第3章: モデルフォールバックの概念例（行131-144）

```python
reasoning_engine_config = {
    "primary": "claude-opus-4-6",
    "fallback": [
        "gpt-5.2-codex",
        "gemini-3-pro"
    ],
    "selection_criteria": {
        "timeout_ms": 30000,
        "max_retries": 2,
        "fallback_on": ["rate_limit", "server_error", "timeout"]
    }
}
```

**判定**: 構文上問題なし。辞書リテラルとして有効なPythonコード。概念例として適切。

### 第3章: 従来のアプローチ vs 新しいアプローチ（行260-277）

```python
# 従来のアプローチ
agent = create_react_agent(
    model="claude-opus-4-6",
    tools=[search, calculator, file_reader]
)

# 新しいアプローチ
agent = create_agent(
    model="claude-opus-4-6",
    tools=[search, calculator, file_reader],
    middlewares=[
        SummarizationMiddleware(max_context_tokens=100000),
        PlanningMiddleware(update_frequency="every_5_steps"),
        HumanInTheLoopMiddleware(require_approval=["delete_file"]),
        LocalContextMiddleware(project_root="./"),
    ]
)
```

**判定**: 構文上問題なし。`search`, `calculator`, `file_reader` 等の変数が定義されていないがこれは概念例なので適切。

### 第3章: Hands-on コード全体（行763-854）

```python
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
# (省略)
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
```

**判定**: 構文上問題なし。ただし以下の軽微な注意点がある。

- **注意**: `create_react_agent` の `max_iterations` パラメータは、LangGraph のバージョンによっては `recursion_limit` や他のパラメータ名で実装されている可能性がある。本書の記述時点（2026年Q1）のAPIに依存するため、Web補足でのバージョン確認を促す注記があると親切。ただし本文中で「概念例」として位置づけられているため、致命的ではない。
- **注意**: `prompt` パラメータが `create_react_agent` で直接受け取れるかはバージョン依存。`state_modifier` や `messages_modifier` として渡す必要がある可能性がある。

### 第4章: PolicyGuardrailクラス（行431-455）

```python
class PolicyGuardrail:
    def __init__(self, policy_document: str):
        self.policy_prompt = self._generate_guardrail_prompt(policy_document)

    def _generate_guardrail_prompt(self, policy: str) -> str:
        return f"""
        以下の組織ポリシーに基づいて、
        ユーザーのリクエストが許可されるか判定してください。
        ...
        """

    def check(self, user_request: str) -> dict:
        result = llm.invoke(
            system=self.policy_prompt,
            user=user_request
        )
        return parse_decision(result)
```

**判定**: 構文上問題なし。`llm` と `parse_decision` が未定義だが概念例として適切。

### 第4章: GuardrailMiddlewareクラス（行472-489）

```python
class GuardrailMiddleware:
    def __init__(self, rules: list[str]):
        self.rules = rules
        self.violation_counter = Counter()

    async def modify_model_request(self, request: ModelRequest) -> ModelRequest:
        for rule in self.rules:
            if self._violates_rule(request.messages, rule):
                ...
```

**判定**: 構文上問題なし。`Counter` のインポート（`from collections import Counter`）が省略されているが概念例として適切。`list[str]` はPython 3.9+のネイティブジェネリクス構文であり妥当。

### 第5章: アブストラクション層によるモデル切り替え（行447-454）

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="anthropic:claude-sonnet-4",
)
```

**判定**: 構文上問題なし。`init_chat_model` はLangChainのユーティリティ関数で妥当。

### 第5章: Subagent定義の例（行213-219）

```python
research_subagent = {
    "name": "research-agent",
    "description": "深い質問をより詳しく調査するために使用",
    "system_prompt": "優れた研究者です",
    "tools": [internet_search],
    "model": "openai:gpt-4o"
}
```

**判定**: 構文上問題なし。`internet_search` が未定義だが概念例として適切。ただし `gpt-4o` は2024年時点のモデル名であり、本書の2026年Q1の文脈では `gpt-5.x` 系が主流のはず。LC-09原文のコード例をそのまま引用しているのであれば問題ないが、読者に混乱を与えない程度の注記があるとよい。

### 総括

**全コード例で致命的なPython構文エラーは検出されなかった。** すべて概念例として適切に機能しており、実行可能性よりも設計パターンの伝達を主目的としている旨が本文中でも明示されている。

---

## 3. 用語の正確性と一貫性

### 良好な一貫性が維持されている用語

| 用語 | 使用パターン | 判定 |
|------|-------------|------|
| ハーネスエンジニアリング（Harness Engineering） | 全章で統一 | 一貫 |
| エージェントハーネス（Agent Harness） | 全章で統一 | 一貫 |
| コンテキストエンジニアリング（Context Engineering） | 全章で統一 | 一貫 |
| コンテキストロット（Context Rot） | 第2章、第5章で統一 | 一貫 |
| コンパクション（Compaction） | 全章で「コンテキスト圧縮」の意味で統一 | 一貫 |
| プログレッシブ・ディスクロージャー（Progressive Disclosure） | 第4章、第5章で統一、初出時に定義あり | 一貫 |
| OSメタファー（OS Metaphor） | 第2章で導入、第3章で再利用 | 一貫 |
| ミドルウェア（Middleware） | 第3章で導入、第4章・第5章で再利用 | 一貫 |
| MCPサーバー / MCPクライアント | 全章で技術的に正確な使い分け | 一貫 |
| 6つのコンポーネント名称 | 全章で英語名・日本語名ともに統一 | 一貫 |

### 指摘事項

| 項目 | 章 | 指摘内容 | 重要度 |
|------|-----|----------|--------|
| **Deep Agents vs DeepAgents** | 第1章・第2章・第5章 | 「Deep Agents」（スペース付き）と「DeepAgents」（スペースなし）の両方の表記が混在している。第1章行17では「Deep Agents」、第2章行347では「DeepAgents」、第5章の比較表では「DeepAgents」が多い。Harrison Chase氏の引用中は「deep agents」（小文字スペースあり）。製品名としてどちらが正式かを統一すべき。references.mdでは「DeepAgents」（LC-03, LC-04等）と「Deep Agents」（LC-02, LC-09等）が混在。LangChainの公式表記に合わせることを推奨する。 | 中 |
| **「推論サンドイッチ」の英語表記** | 第1章、第3章、第5章 | 日本語「推論サンドイッチ」は全章で統一されているが、英語表記がない箇所がある。第3章 3.2節で「推論サンドイッチ」パターンとして言及されるが初出ではない。全体として概念の理解には問題ないが、索引等を想定すると英語の「Reasoning Sandwich」を少なくとも1回は併記すると国際的な参照性が高まる。 | 低 |
| **「コンテキスト失敗モード」の帰属** | 第2章 2.2節（行209付近） | 「Drew Breunig氏が体系化した4つのコンテキスト失敗モード」と記述されているが、出典はLC-11（LangChainの記事）に帰属されている。Drew Breunig氏がこの分類を最初に提唱し、LangChainがLC-11記事で紹介・引用した、という関係が正確かどうか確認を推奨する。本文では「（LC-11）」としか書かれていないため、読者が混乱する可能性がある。 | 低 |
| **「claude-sonnet-4-5」vs「Claude Sonnet 4.5」** | 第3章 Hands-on（行800付近） | コード中のモデル名が `"claude-sonnet-4-5"` だが、本文中では `Claude Sonnet 4.5` と表記。API文字列としてはハイフン区切りが一般的だが、正式なAPI名としては `claude-sonnet-4-5` が正しいか確認を推奨する。Anthropicの命名規則では `claude-sonnet-4-5-20250514` のようなバージョン付き文字列が使用される場合もある。 | 低 |

---

## 4. 技術的主張の根拠の有無

### 十分な根拠がある主張

| 主張 | 根拠 | 判定 |
|------|------|------|
| 「モデルはコモディティ、ハーネスこそが競争優位」 | BLG-02（Aakash Gupta氏の記事）、LC-08（Terminal Bench 2.0実証） | 複数ソースで裏付け |
| 「ハーネスの最適化のみでスコアが52.8→66.5に向上」 | LC-08（LangChainの実験報告） | 一次ソースに基づく |
| エージェントスタックの3層分類（Framework / Runtime / Harness） | LC-01（Harrison Chase氏の記事）、TLDV-01（VIPコミュニティコールでの直接発言） | 提唱者本人の一次ソースに基づく |
| コンテキストエンジニアリングの4操作戦略 | LC-11（LangChain記事） | 一次ソースに基づく |
| Constitutional Classifiersがジェイルブレイク成功率を4.4%に低減 | ANT-18（Anthropic Research論文） | 査読前論文だが一次ソース |
| MCPがツール標準化の事実上の標準 | STD-01（AAIF設立）、STD-03（MCP仕様）、OAI-06（AAIFへの寄贈） | 複数の公的ソースで裏付け |
| 12 Factor Agentsの位置づけ | BLG-11（Dex Horthy氏の原著） | 一次ソース |
| Claude Codeのサンドボックス設計 | ANT-07（Anthropic Engineering記事） | 一次ソース |
| OSメタファー | LC-11（LangChain記事） | 一次ソース |

### 根拠の補強を推奨する主張

| 主張 | 章・行 | 指摘内容 | 重要度 |
|------|--------|----------|--------|
| **「主要なLLMの性能差は急速に縮小しており」** | 第1章 1.1節（行31付近） | BLG-02への帰属があるが、「性能差の縮小」自体を定量的に示すデータは本文中に提示されていない。ベンチマークスコアの推移データ等を補足するか、「Gupta氏はこう主張している」という帰属を明確にすることを推奨する。 | 中 |
| **「エージェントが途中で方向性を見失う。長時間のタスクでコンテキストが劣化し、品質が急激に低下する。」** | 第1章 1.1節（行19付近） | 一般的な業界認識として述べられているが、具体的なソースへの帰属がない。ANT-03（コンテキストロット）やACD-06を参照先として追加するとより堅牢になる。 | 低 |
| **「適切なハーネスなしにエージェントを動かしていることが、信頼性低下の主要因である可能性が高い」** | 第1章 1.3節（行164付近） | 著者の解釈・推論として述べられているが、「可能性が高い」という表現は根拠の強さに比してやや断定的。LC-08の実験結果（ハーネス最適化による改善）が間接的な根拠となりうるが、「信頼性低下の主要因」という因果関係は別途の論証が必要。「ハーネスが信頼性向上に寄与するという仮説を支持するデータがある」程度の表現が正確。 | 低 |
| **「フレームワークの世代交代は約1年周期で起きている」** | 第5章 Column（行314付近） | LC-14への帰属はあるが、3データポイント（2023, 2024, 2025）からの帰納であり、「約1年周期」という法則を導出するにはサンプルが少ない。「過去3年間では約1年周期であった」という限定的な表現がより正確。 | 低 |
| **SQLiteベースMCPの「500トークン程度に抑え」** | 第3章 3.5節（行554付近） | TLDV-03（AIコーディング道場の議論）からの引用であるが、「500トークン」という数値は参加者の報告に基づくものであり、検証されたデータとしての信頼性は限定的。議事録ベースの情報であることを明記しているため問題は小さいが、読者に注意を促す文言があるとよい。 | 低 |

---

## 5. その他の所見

### 表記・構成に関する軽微な指摘

| 項目 | 章 | 指摘内容 | 重要度 |
|------|-----|----------|--------|
| **表1.1と表2.1の内容重複** | 第1章・第2章 | 「ハーネスエンジニアリング用語の系譜」を示す表が第1章（表1.1）と第2章（表2.1）で内容がほぼ重複している。第2章の表には12 Factor Agentsの行が追加されている点が異なるが、読者に冗長に感じられる可能性がある。第2章の表を「拡張版」として位置づけるか、第1章では簡略化するか、整理を推奨する。 | 低 |
| **「Humans Steer, Agents Execute」の帰属** | 第1章 1.1節（行25付近） | 「Lopopolo氏はこの新しい働き方をHumans Steer, Agents Executeと表現した」とあるが、この正確なフレーズがOAI-01原文に登場するかの確認を推奨する。 | 低 |
| **第5章の比較表の情報密度** | 第5章 5.3節 | 8プラットフォーム x 5軸の比較表は情報量が非常に多く、印刷物として読みにくくなる可能性がある。電子版での閲覧を前提とした補足（ソート機能付き表のWeb版など）の案内があると親切。本文でも「Web補足（GitHub）で最新版を提供する」との記述があり対処されている。 | 低 |

### 参照整合性

全章を通じて、本文中の出典表記（OAI-01, LC-08, ANT-07等）はすべてreferences.mdに対応するエントリが存在することを確認した。参照切れは検出されなかった。

各章末の参照文献リストについても、本文中で引用されている文献が漏れなく掲載されていることを確認した。

---

## レビューサマリ

| カテゴリ | 件数 | 内訳 |
|---------|------|------|
| **引用データ・数値** | 主要数値15件すべて正確、要確認5件 | 致命的誤りなし |
| **コード構文** | 7箇所のコード例すべて構文正常 | 致命的エラーなし |
| **用語の正確性・一貫性** | 主要用語10種すべて一貫、指摘4件 | 「Deep Agents / DeepAgents」の表記揺れのみ中程度 |
| **技術的主張の根拠** | 主要主張9件すべて十分な根拠あり、補強推奨5件 | 致命的な根拠不在なし |
| **その他** | 軽微な指摘3件 | 表の重複、帰属確認 |

### 重要度別集計

- **致命的**: 0件
- **中**: 3件（「1日平均3.5件PR」の原文確認、「74%」の原文確認、「Deep Agents/DeepAgents」表記統一）
- **低**: 14件

---

## 推奨アクション（優先度順）

1. **「Deep Agents」と「DeepAgents」の表記を統一する**（中程度） -- LangChain公式表記を確認のうえ全章で統一
2. **「1日あたり平均3.5件のPR」がOAI-01原文に明記されているか確認する**（中程度） -- 概算値であれば「概算で」と注記を追加
3. **「74%が主に人間による評価に依存」がACD-06原文に明記されているか確認する**（中程度） -- 概要には未記載のため原文照合が必要
4. **「主要なLLMの性能差は急速に縮小」の根拠を補強する**（低〜中） -- ベンチマークデータの引用、または「Gupta氏の主張によれば」と帰属を明確化
5. **表1.1と表2.1の重複を整理する**（低） -- 第1章は簡略版、第2章は拡張版とする等
