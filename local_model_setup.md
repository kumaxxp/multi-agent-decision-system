# ローカルモデル セットアップガイド

LM Studioでダウンロードしたモデルファイル（GGUF形式）を直接使用する方法です。

## 前提条件

- LM Studioでモデルをダウンロード済み
- Python環境にllama-cpp-pythonがインストール済み
- GPU使用の場合はCUDAドライバがインストール済み

## セットアップ手順

### 1. 依存関係のインストール

```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt
```

GPU使用の場合（CUDA 11.8の例）：
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### 2. 環境設定

`.env.local`を`.env`にコピー：

```bash
cp .env.local .env
```

### 3. モデルの選択

プログラムを実行すると、LM Studioでダウンロードしたモデルの一覧が表示されます：

```bash
python main_local.py
```

表示例：
```
利用可能なモデル:
  1. mistral-7b-instruct-v0.2.Q4_K_M.gguf (TheBloke/Mistral-7B-Instruct-v0.2-GGUF)
  2. llama-2-13b-chat.Q4_K_M.gguf (TheBloke/Llama-2-13B-chat-GGUF)
  3. elyza-7b-instruct.Q5_K_M.gguf (elyza/ELYZA-japanese-Llama-2-7b)
```

`.env`ファイルの`MODEL_INDEX`を編集して、使用したいモデルの番号を指定：

```env
MODEL_INDEX=1  # 1番目のモデルを使用
```

または、フルパスで指定：

```env
MODEL_PATH=/Users/username/.cache/lm-studio/models/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

### 4. 実行

```bash
python main_local.py "議論したいトピック"
```

## モデル選択の指針

### 日本語対応モデル（推奨）

- **ELYZA-japanese-Llama-2-7b**: 日本語特化、高品質
- **rinna-japanese-gpt**: 日本語専用、軽量
- **Swallow-7b**: 日本語対応、バランス型

### 汎用モデル

- **Mistral-7B-Instruct**: 高速、英語中心
- **Llama-2-13B-chat**: 大容量、高品質
- **Vicuna-13B**: 対話特化

### 量子化レベル

- **Q4_K_M**: バランス型（推奨）
- **Q5_K_M**: 高品質
- **Q3_K_S**: 高速・省メモリ
- **Q8_0**: 最高品質（要大容量メモリ）

## パフォーマンスチューニング

### GPU設定

`.env`ファイルで調整：

```env
# GPUに載せるレイヤー数
N_GPU_LAYERS=-1  # 全て（推奨）
N_GPU_LAYERS=20  # 部分的（VRAMが少ない場合）
N_GPU_LAYERS=0   # CPU only
```

### コンテキストサイズ

```env
N_CTX=2048  # デフォルト
N_CTX=4096  # 長い対話用（要メモリ）
N_CTX=1024  # 省メモリ
```

## トラブルシューティング

### モデルが見つからない場合

1. LM Studioのモデル保存場所を確認：
   - Mac: `~/.cache/lm-studio/models/`
   - Windows: `C:\Users\username\.cache\lm-studio\models\`
   - Linux: `~/.cache/lm-studio/models/`

2. `MODEL_PATH`で直接パスを指定

### メモリ不足エラー

1. より小さいモデルを使用（7B以下）
2. 量子化レベルを下げる（Q3_K_S など）
3. `N_CTX`を小さくする
4. `N_GPU_LAYERS`を調整

### 日本語が文字化けする

1. 日本語対応モデルを使用
2. ターミナルの文字コードをUTF-8に設定

## メモリ使用量の目安

| モデルサイズ | 量子化 | 必要メモリ |
|------------|--------|-----------|
| 7B | Q4_K_M | 約4-6GB |
| 7B | Q5_K_M | 約5-7GB |
| 13B | Q4_K_M | 約8-10GB |
| 13B | Q5_K_M | 約10-12GB |