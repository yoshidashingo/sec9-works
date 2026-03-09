# H2O BCP プロジェクト調査結果サマリー

**参照元リポジトリ:** `/Users/shingo/Documents/GitHub/h2o-bcp/`
**調査日:** 2026-02-27

---

## プロジェクト基本情報

| 項目 | 内容 |
|------|------|
| 企業 | エイチ・ツー・オー リテイリング株式会社 |
| プロジェクト | IT BCP（事業継続計画）環境構築 |
| 開始日 | 2026-02-05 |
| 担当 | sec9 (Michael Oshita, Shinichi Takahashi, 乙部美咲, Shingo Yoshida) |
| コンペ競合 | Server Works（1,500〜1,800万円） |
| sec9前回見積 | 2,000万円超 |

---

## 対象システム

### MDware（商品・サプライチェーン管理）

| リソース | 内訳 |
|---------|------|
| EC2 | 18台 |
| RDS | 4個（SQL Server + PostgreSQL、合計約20.3TB） |
| 実使用量 | 約14TB |
| 用途 | 仕入・在庫・販売企画 |

### Department Store POS（POSシステム）

| リソース | 内訳 |
|---------|------|
| EC2 | 45台 |
| RDS | 2個（SQL Server、合計約13TB） |
| FSx | 20.8TB（Windows File Server、AD統合） |
| 用途 | 店舗売上・顧客データ・在庫管理 |

**スコープ変遷:**
- Phase 1: MDware + POS（初期）
- Phase 2: MDwareのみ（2026-02-16〜）
- Phase 3: MDware + POS（2026-02-26〜、**現在**）

---

## アーキテクチャ概要

- **DRサイト:** 大阪リージョン（ap-northeast-3）
- **本番サイト:** 東京リージョン（ap-northeast-1）
- **接続:** AWS Direct Connect Gateway（DXGW）、Transit Gateway（3月5日切り替え予定）
- **DR方式:** Peacetime Provisioning（事前にDRリソースを用意）
- **バックアップ:** 日次スナップショット + 大阪へのCross-Region Copy

---

## コスト試算（月次ランニングコスト）

### スナップショット保持コスト（変動率別、90日保持）

| 変動率 | 月次増分 | MDware RDS月額 | POS RDS月額 | FSx月額 | 合計目安 |
|--------|---------|--------------|------------|---------|---------|
| 0.5%/日 | - | 未試算 | 未試算 | 未試算 | - |
| 1%/日 | - | 未試算 | 未試算 | 未試算 | - |
| 2%/日 | - | 未試算 | 未試算 | 未試算 | - |

> ※ 再見積もりの主要論点：変動率3パターン × 90日保持での試算

**ストレージ単価参考:**
- RDSスナップショット: $0.095/GB/月
- FSxスナップショット: 約$0.05/GB/月

**前回試算ベースライン（60日保持時）:**
- MDware RDS（20.3TB × 60日 × 0.095）: 約$3,000〜$4,500/月
- リージョン間転送: $1,100〜$3,300/月
- 全体合計: $5,000〜$17,000/月（前回見積）

### RTO制約

- 要件: **12時間以内**
- 現状評価: 日次レプリケーション済みの場合はギリギリ達成可能
- 東京スナップショットのみの場合: 20TBを50MB/秒で転送すると112時間 → **達成不可能**
- **結論: 大阪への事前レプリケーションが必須**

---

## 工数・費用見積もり（参考：前回設計）

- 10ユニット構成（6 peacetime + 4 recovery）
- Terraform IaC化
- 前回提案額: 2,000万円超

---

## 参照ファイル（h2o-bcpリポジトリ）

| ファイル | 内容 |
|---------|------|
| `aidlc-docs/aidlc-state.md` | プロジェクト状態管理 |
| `aidlc-docs/inception/requirements/requirements.md` | 要件定義v3.0 |
| `aidlc-docs/inception/application-design/` | アーキテクチャ設計 |
| `aidlc-docs/construction/functional-design/` | 10ユニット詳細設計 |
| `aws-infrastructure-audit.md` | AWS環境監査レポート（1月29日） |
| `step-functions-analysis.md` | Step Functions分析 |
