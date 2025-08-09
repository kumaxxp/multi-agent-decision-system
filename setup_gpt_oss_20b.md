# OpenAI GPT-OSS-20B セットアップガイド

## 1. LM Studioでモデルをダウンロード

1. LM Studioを起動
2. 「Discover」タブを選択
3. 検索バーに「gpt-oss-20b」または「openai」と入力
4. モデルを見つけたら「Download」ボタンをクリック
5. ダウンロード完了まで待機（20Bモデルなので時間がかかります）

## 2. モデルの保存場所を確認

LM Studioのモデルは通常以下の場所に保存されます：

- **Mac/Linux**: `~/.cache/lm-studio/models/`
- **Windows**: `C:\Users\[ユーザー名]\.cache\lm-studio\models\`

## 3. 環境設定

`.env`ファイルを編集して、モデルのパスを設定：

```bash
# .envファイルの例
MODEL_PATH=/home/[ユーザー名]/.cache/lm-studio/models/openai/gpt-oss-20b/gpt-oss-20b-q4_k_m.gguf
TEMPERATURE=0.7
MAX_TOKENS=512
N_CTX=2048
N_GPU_LAYERS=40  # 20Bモデルは大きいので、GPUメモリに応じて調整
```

## 4. メモリ要件

GPT-OSS-20Bモデルの推奨スペック：

- **RAM**: 16GB以上（推奨: 32GB）
- **GPU VRAM**: 16GB以上（推奨: 24GB）
- **ストレージ**: 15-20GB（モデルファイル用）

メモリが不足する場合の対策：

```bash
# GPU レイヤー数を減らす
N_GPU_LAYERS=20  # または 0（CPU only）

# コンテキストサイズを減らす
N_CTX=1024

# より小さい量子化版を使用
# q3_k_s版やq2_k版など
```

## 5. 実行

```bash
# 環境設定の確認
python test_local_model.py

# 本番実行
python main_local.py "議論したいトピック"
```

## 6. トラブルシューティング

### モデルが見つからない場合

```bash
# モデルファイルを検索
find ~ -name "*gpt-oss-20b*.gguf" 2>/dev/null
```

### メモリ不足エラー

1. より小さい量子化版を使用（q3_k_s、q2_k）
2. N_GPU_LAYERSを減らす
3. N_CTXを減らす（512や256）

### 実行が遅い場合

1. GPUが正しく認識されているか確認
2. llama-cpp-pythonをGPU対応で再インストール：

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

## 代替オプション

20Bモデルが大きすぎる場合は、以下の代替モデルを検討：

- **Mistral-7B-Instruct**: 高速で高品質
- **Llama-2-13B-chat**: バランス型
- **ELYZA-japanese-7B**: 日本語特化（7B）

これらのモデルも同じ手順で使用できます。