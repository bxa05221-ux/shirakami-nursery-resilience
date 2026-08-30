# 白神保育レジリエンス α1.0 Pilot

## まずインストールする

このリポジトリのAlpha 1.0 reference runtimeは、現時点ではローカルPCで動かすためのプロトタイプです。`server.py` は外部フレームワークを使わず、Python標準ライブラリで起動できます。PyYAMLはSynthetic Pilot実行・テストで使用します。

### 必要なもの

- Windows / macOS / Linux
- Python 3.11系を推奨（CIも3.11で実行）
- Git

### 1. リポジトリを取得

```bash
git clone https://github.com/bxa05221-ux/shirakami-nursery-resilience.git
cd shirakami-nursery-resilience
```

### 2. 仮想環境を作る

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. 依存関係を入れる

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Synthetic Pilotを確認

実在する園児・職員データはまだ入力しません。

```bash
python -m pytest -q tests/test_pilot_pipeline.py
```

成功すれば、Synthetic Dataによる基礎パイプラインの確認が完了です。

### 5. ローカルAPIを起動

別のPowerShell / Terminalで、リポジトリのルートから:

```bash
python runtime/reference/server.py
```

ブラウザで次を開きます:

`http://127.0.0.1:8000/api/v1/landscape/daily`

JSONが表示されれば起動成功です。

## 最初の試し方

最初は実データを使わず、`examples/pilot/sample-facility.yaml` を使います。

Synthetic Pilotの流れは:

```text
Synthetic Data
  ↓
出席・在園時間Landscape
  ↓
時間帯予測Landscape
  ↓
明日の保育Landscape
  ↓
人間レビュー
```

この段階ではAIによる自動決定は行いません。予測・提案は判断材料として扱い、保育者が判断します。

## 実証園へ移る前に

次の確認が必要です。

- 園内の権限設計
- 個人情報の取り扱い
- 保護者への説明・同意
- 仮名化／匿名化境界
- 保存場所とバックアップ
- 園の規程・法令・制度上の要件
- 発達・医療・虐待・事故等の高リスク領域における専門職判断

**現在のreference runtimeは本番運用用ではありません。** 認証、認可、暗号化、永続DB、監査基盤、バックアップ、Safeguarding workflow等が未実装です。

## 困ったら

まず、

1. Pythonのバージョン
2. `python -m pytest -q tests/test_pilot_pipeline.py` の結果
3. 起動時のエラーメッセージ

を確認してください。

個人情報や実在園児の記録をIssueや公開リポジトリへ貼り付けないでください。
