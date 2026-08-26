# Shirakami Nursery Resilience

## 保育レジリエンス α1.0

保育をAIに決めさせるためのシステムではない。

子ども一人ひとりの観察、発達、関係、環境、保育者の判断、安全、地域情報をLandscapeとして蓄積し、個別の保育を束ねて集団・園全体の保育へ還流させるためのReference Implementationである。

## Core principle

> 個々の子どもを全体に合わせるのではなく、個々の子どもの姿から全体保育を組み立てる。

## α1.0 scope

- 個別Landscape
- 発達観測と個別保育計画
- 集団Landscape / 園Landscape
- 翌日の保育計画への還流
- 日誌・ヒヤリハット・事故報告・会議録等の記録支援
- 人員配置・保育負荷の観測支援
- External Landscape（天候、防災、害獣等）
- 匿名内部通報 / 組織改善Signal
- Evidenceの蓄積
- 第三者評価への逆流・改善ループ

## Design boundary

AIは診断・処遇・配置・安全判断・評価結果を自律決定しない。
AIは観測された情報を整理し、関係を提示し、計画案や問いを生成する。最終判断は園・専門職・管理者が行う。

## Domain-independent direction

本リポジトリは保育を最初のReference Implementationとするが、Core概念は将来の学校、就労支援、高齢者支援、医療等への展開を想定する。

共通概念：Person / Group / Environment / Observation / Evidence / Plan / Event / Signal / Decision / Outcome / Permission / Audit

## Third-party evaluation loop

`個別保育 → 集団Landscape → 園Landscape → Evidence → 評価 → 改善提案 → 園Landscape → 実践`

第三者評価を記録提出の終点ではなく、組織学習と保育改善へ戻る逆流ループとして扱う。

## Status

α1.0 — pilot design / reference implementation

This repository intentionally excludes any identifiable child, family, staff, or facility operational data.
