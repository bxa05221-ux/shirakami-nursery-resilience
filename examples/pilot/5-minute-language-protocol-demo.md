# 5-Minute Language Protocol Demo

## Purpose
園長・保育者が構造化データを覚えなくても、自然言語だけで白神のLandscape循環を試せる最小デモ。

## Environment
- Windows PC
- Python 3.11+
- Local Pilot Runtime
- Synthetic data only
- No real child personal information

## Step 1: Speak naturally

例:

> 4歳児クラス。最近Aちゃんは朝の切り替えに時間がかかるけれど、戸外では虫探しに夢中です。明日は午前中に外遊びを予定しています。午後は雨の予報です。担任は1名休みです。

## Step 2: Ask for Landscape

> この情報から、明日の保育Landscapeを整理してください。判断はせず、観測された事実、関係しそうな情報、確認が必要な点を分けてください。

## Step 3: Review

確認する項目:
- 現場感覚と合っているか
- 抜けている情報はないか
- AIが事実と推測を混同していないか
- 保育者が判断すべき点が残っているか

## Step 4: Optional proposal

> このLandscapeを前提に、明日の保育計画の「案」を作ってください。必ず根拠となる観測と不確実性を併記し、最終判断は保育者に残してください。

## Step 5: Evidence

実際に行った保育と振り返りを、観測・人間の判断・実践結果として記録する。

## Why language protocol works here

自然言語を入口にすると、園長・保育者はDB項目やJSONを覚えずに現場の言葉で入力できる。Runtime側で必要な構造へ整理するため、試作段階の利用者体験を先に検証できる。

これは本番の個人情報処理を意味しない。実証段階では認証、権限、同意、監査、保存場所、個人情報保護を別途実装・確認する。
