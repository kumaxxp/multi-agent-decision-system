# Multi-Agent Decision System

複数のLLMエージェントが協調して議論を行い、結論を導くシステムです。

## 概要

このプロジェクトは`design_spec.md`に基づいて実装された多エージェント対話システムです。AutoGenフレームワークを使用して3つのエージェントが順番に対話を行い、ユーザーの入力に対して多角的な議論を展開します。

### エージェント構成

1. **語り手エージェント** - 創造的で大胆な発想を行う（ハルシネーション許容）
2. **相槌役エージェント** - 慎重に内容を確認し、必要に応じて指摘を行う
3. **判定役エージェント** - 議論を整理し、結論と代替案を提示する

## セットアップ

### 1. 環境準備

```bash
# リポジトリのクローン
git clone <repository-url>
cd multi-agent-decision-system

# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt
```

### 2. LLM設定

#### ローカルモデルを直接使用する場合（推奨）

LM Studioでダウンロードしたモデルファイル（GGUF形式）を直接使用します：

```bash
# ローカルモデル用の設定ファイルをコピー
cp .env.local .env

# ローカルモデル版を実行
python main_local.py
```

詳細な設定方法は[local_model_setup.md](local_model_setup.md)を参照してください。

#### LM Studio APIを使用する場合

```bash
# LM Studio API用の設定ファイルをコピー
cp .env.lmstudio .env

# 通常版を実行
python main.py
```

詳細は[lmstudio_setup.md](lmstudio_setup.md)を参照してください。

#### その他のLLMを使用する場合

```bash
cp .env.example .env
```

設定例：
- **OpenAI API**: `OPENAI_API_KEY`を設定
- **Ollama**: `API_BASE_URL=http://localhost:11434/v1`

## 使用方法

### 基本的な実行

```bash
python main.py "議論したいトピック"
```

例：
```bash
python main.py "AIが人間の仕事を奪うことについてどう思いますか？"
```

### インタラクティブモード

引数なしで実行すると、トピックの入力を求められます：

```bash
python main.py
```

## ログ機能

対話ログは`conversation_logs/`ディレクトリにJSON形式で保存されます。各セッションにはタイムスタンプベースのIDが付与されます。

## プロジェクト構造

```
multi-agent-decision-system/
├── main.py              # メインエントリーポイント
├── agents.py            # エージェント定義
├── requirements.txt     # 依存関係
├── .env.example         # 環境変数の例
├── design_spec.md       # 詳細設計書
├── README.md            # このファイル
└── conversation_logs/   # 対話ログ保存ディレクトリ
```

## 今後の拡張予定

- ReDelによる対話の可視化UI
- 相槌役エージェントへのWeb検索ツール追加
- より高度な対話制御（並列処理、再帰的委譲）
- 複数のローカルLLMモデルの同時利用

詳細な設計については`design_spec.md`を参照してください。
