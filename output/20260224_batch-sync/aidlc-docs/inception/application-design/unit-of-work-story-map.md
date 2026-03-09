# Unit of Work - Requirements Mapping

User Stories ステージはスキップしたため、要件（requirements.md）からユニットへのマッピングを示す。

## Requirements → Unit Mapping

| Requirement | Unit 1: Agent SDK Core | Unit 2: Orchestration |
|-------------|:-----:|:-----:|
| **FR-2.1**: GA議事録同期 (tldv) | o | - |
| **FR-2.2**: Sec9議事録同期 (circleback) | o | - |
| **FR-2.3**: Paulo記事同期 (Gmail) | o | - |
| **FR-2.4**: Market Hack記事同期 (Gmail) | o | - |
| **FR-2.5**: MCPサーバー接続 | o | - |
| **FR-2.6**: 同期状態管理 | o | - |
| **FR-2.7**: ファイル出力 | o | - |
| **FR-2.8**: git操作 | o (--no-git mode) | o (git-sync-helper.sh) |
| **FR-3.1**: 毎晩25時実行 | - | o |
| **FR-3.2**: sync-all-cron.sh統合 | - | o |
| **FR-3.3**: 方式切替機構 | - | o |
| **FR-4.1**: ロギング | o | o |
| **FR-4.2**: 重複実行防止 | - | o |
| **FR-4.3**: sync-stateバリデーション | o | - |
| **FR-4.4**: git操作安全性 | - | o |
| **NFR-1**: 実行環境 (macOS) | o | o |
| **NFR-2**: 信頼性 | o | o |
| **NFR-3**: コスト制御 | o | - |
| **NFR-4**: 保守性 | o | o |
| **NFR-5**: セキュリティ | o | - |

## Coverage Summary

- **Unit 1**: FR-2全般, FR-4.1/4.3, NFR-1〜5 → Agent SDKの中核機能
- **Unit 2**: FR-3全般, FR-4.1/4.2/4.4, NFR-1/2/4 → cron統合・運用基盤
- **全要件がいずれかのユニットにマッピング済み**
