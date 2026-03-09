# システム論理構成図_20251229

> 出典: https://docs.google.com/presentation/d/1dTldD1Ovb8qj3tjfxJzKvuPiCWSCzafx/edit?slide=id.p3#slide=id.p3

## スライド1: 現システムの論理構成 - KFM/MDware

### 東京リージョン
- **H2O AWS**
  - Web (取引先): ALB, WAF, ACM (取引先のみ), Cognito テナント管理
  - Web (内部): ALB
  - 帳票: EFS
  - DB (MS-SQL) x2
  - S3, bat, JP1
  - 基幹補助: NFS
  - IICS, S3
  - HULFT (AWS)
  - EDI基盤
  - Network Firewall (内部NWからのインターネット接続)
  - S3 (ログ管理)
  - Internet GW, NAT GW
  - NLB (江坂経由接続はNLBを経由)
  - Cloud Proxy (CBO経由)

### 大阪リージョン
- 記載なし（東京のみ）

### 接続先
- **Toshiba TEC AWS**: POS PrimeStore
- **FJJ DC**: TradeFront 統合, TM-1
- **社内ネットワーク（閉域網）**: 江坂NC, 新NC, 神戸DC
- **Equinix**: DXGW経由
- **NEC AWS**, **NRI AWS**
- **OCVS**: 補充金
- **SS会計**

### ネットワーク構成
- 次世代ネットワーク経由: 拠点、百貨店、店舗
- 社内ネットワーク（閉域網）: 江坂NC, 新NC, 神戸DC
- DXGW: Equinix経由

### 運用基盤
- WorkSpaces
- Step Functions
- Inspector
- Patch Manager
- Backup

## スライド2: 現システムの論理構成 - KFM/MDware（IF全体図）

- MDwareが止まることで、直接影響を受けるサーバは確認済み
- 細かな被害状況はKFMで整理してもらう

## スライド3: 現システムの論理構成 - 百貨店/POS

### H2O AWS
- **POS-AP**: ALB
- **FSx**
- **DB (MS-SQL)**: ALB
- **Managed AD**
- **PC-AP**: ALB
- **BAT-AP** x2
- **Pay-AP**: 決済基盤
- **外付け-AP**: 外付け
- **DWH**
- **HULFT**
- **MAN-AP**: 運用管理
- **S3 (ログ管理)**
- **S3 (POSdata)**
- **Internet GW**

### 接続先
- 富士通京橋: 基幹、免税中継、集配信
- Link Express: S3 (POSdata)

### 運用基盤
- WorkSpaces, Step Functions, Inspector, Patch Manager, Backup, ACM

## スライド4: 大阪Rで稼働させる際の構成 - KFM/MDware

- 東京リージョンから大阪リージョンへの構成移行
- 基本的に同一構成を大阪リージョンに再現
- ネットワーク接続は次世代ネットワーク経由で拠点・百貨店・店舗にアクセス

## スライド5: 大阪Rで稼働させる際の構成 - 百貨店/POS

- 百貨店/POSシステムの大阪リージョン構成
