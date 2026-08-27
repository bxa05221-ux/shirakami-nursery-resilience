# 保育レジリエンス α1.0 — System Map

## Core flow

```text
職員スマホ
  ↓
Web UI
  ↓
OpenAPI Contract
  ↓
Reference Runtime
  ├─ Observation
  ├─ Landscape
  ├─ Staffing
  ├─ Safety Signal
  ├─ External Landscape
  └─ Tomorrow Plan Draft
        ↓
  保育者による修正・承認
        ↓
  Evidence / 継続的改善
```

## Landscape layers

- Child: 個別の発達・姿・選択・声
- Class: 集団、環境、活動、担当配置
- Facility: 施設全体、複数クラス、職員配置
- External: 天候、防災、害獣、地域情報等

## Phase rotation

同じ事象を以下の軸で再観測する。

1. 個別 → 集団 → 園 → 外部
2. 過去 → 現在 → 明日
3. 観察 → 計画 → 実践 → 評価 → 改善

## Output chain

Observation → Landscape → Safety/Checkpoints → Tomorrow Plan → Teacher Revision → Approval → Evidence

将来的には日誌、ヒヤリハット、事故報告、対応マニュアル更新、会議録、第三者評価用Evidence Summaryへ派生させる。

## Capacity assumptions for alpha1.0

- 最大6クラス
- 1クラス最大20人（システム上のデモ上限）
- 定員区分、年齢構成、施設種別、制度年度、職員配置Policyは別管理し、固定値として法的基準扱いしない。

## Safety boundary

虐待・不適切保育・重大事故等は、AIが判定主体にならない。事実記録、緊急性確認、所定の人間による初動、報告、関係機関との連携を優先する。

匿名内部通報では、通報者情報と通報内容を分離し、アクセス制御・監査・通報者保護を前提とする。

## Regulatory knowledge layer

施設類型に応じて、少なくとも以下を参照可能にする。

- 幼保連携型認定こども園教育・保育要領
- 幼稚園教育要領
- 保育所保育指針
- 各解説・関連する最新の制度・自治体Policy

根拠文書はAIへの単純な学習データではなく、計画案・実践・Evidenceの根拠として参照する。

## Next stage

1. Reference Runtimeを永続DBへ移行
2. 認証・役割別権限を追加
3. Web UIとAPIの本接続を標準化
4. 施設ごとのPolicy登録
5. Evidenceの不変記録・監査ログ
6. 3施設で実証
7. 実証結果をプロトコルへ逆流
