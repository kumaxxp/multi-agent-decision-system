# LM Studio セットアップガイド

## LM Studioでの設定手順

### 1. LM Studioの起動と設定

1. LM Studioを起動します
2. 左側のメニューから「Local Server」タブを選択します
3. 以下の設定を確認・変更します：
   - **Server Port**: `1234`（デフォルト）
   - **CORS**: 有効にする（チェックを入れる）
   - **Request Queuing**: 有効にする（推奨）

### 2. モデルの読み込み

1. 使用したいモデルを選択して「Load」をクリック
2. 推奨モデル（日本語対応）：
   - `TheBloke/Mistral-7B-Instruct-v0.2-GGUF`
   - `TheBloke/Llama-2-13B-chat-GGUF`
   - `elyza/ELYZA-japanese-Llama-2-7b-instruct-GGUF`（日本語特化）
   - `rinna/japanese-gpt-neox-3.6b-instruction-sft-v2`（日本語特化）

### 3. サーバーの起動

1. モデルロード後、「Start Server」ボタンをクリック
2. コンソールに「Server started on http://localhost:1234」と表示されることを確認

### 4. 環境設定

`.env.lmstudio`ファイルを`.env`にコピー：

```bash
cp .env.lmstudio .env
```

必要に応じて`.env`ファイルを編集：

```bash
# モデル名をLM Studioで読み込んだものに変更
MODEL_NAME=your-loaded-model-name

# 温度パラメータを調整（0.0-1.0）
TEMPERATURE=0.7
```

### 5. プログラムの実行

```bash
python main.py "議論したいトピック"
```

## トラブルシューティング

### 接続エラーが発生する場合

1. LM Studioのサーバーが起動しているか確認
2. ポート1234が他のアプリケーションで使用されていないか確認
3. ファイアウォールがlocalhost:1234への接続をブロックしていないか確認

### レスポンスが遅い場合

1. より小さいモデル（7B以下）を使用する
2. GPUアクセラレーションが有効になっているか確認
3. LM Studioの設定で「GPU Layers」を調整

### 日本語が文字化けする場合

1. 日本語対応モデルを使用しているか確認
2. ターミナルの文字エンコーディングがUTF-8になっているか確認

## パフォーマンスチューニング

### モデル選択の指針

- **高速レスポンス重視**: 3B-7Bクラスのモデル
- **品質重視**: 13B以上のモデル
- **日本語重視**: ELYZA、rinna等の日本語特化モデル

### メモリ使用量の目安

- 7Bモデル: 約6-8GB RAM
- 13Bモデル: 約10-16GB RAM
- 30Bモデル: 約20-32GB RAM

### GPU使用時の設定

LM Studioの「Model Configuration」で：
- **GPU Layers**: 可能な限り大きく設定（GPU VRAMに応じて）
- **Context Length**: 2048-4096（長い対話には大きく設定）