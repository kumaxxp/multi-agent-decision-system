# Multi-Agent Decision System

OpenAI APIを使用した3つのエージェントによる対話システムです。

## 概要

このシステムでは、3つの異なる役割を持つAIエージェントが順番に議論を行い、ユーザーの入力に対して多角的な結論を導きます。

### エージェント構成

1. **語り手エージェント** - 創造的で大胆な発想を行う（ハルシネーション許容）
2. **相槌役エージェント** - 慎重に内容を確認し、建設的な指摘を行う
3. **判定役エージェント** - 議論を整理し、結論と代替案を提示する

## セットアップ

### 1. 環境準備

```bash
# 依存関係のインストール
pip install -r requirements.txt
```

### 2. OpenAI API設定

`.env`ファイルを作成してAPIキーを設定：

```bash
# .env
OPENAI_API_KEY=sk-your-actual-api-key-here
MODEL_NAME=gpt-3.5-turbo
```

## 使用方法

### 基本的な実行

```bash
python main_direct.py "議論したいトピック"
```

### 実行例

```bash
python main_direct.py "AIは人間の創造性を高めるか？"
python main_direct.py "リモートワークのメリット・デメリット"
python main_direct.py "持続可能な社会を作るために必要なこと"
```

### インタラクティブモード

```bash
python main_direct.py
# → 議論したいトピックを入力してください: [ここに入力]
```

## 出力例

```
=== 多エージェント対話システム（直接API版） ===
ユーザー入力: AIは人間の創造性を高めるか？

[語り手の発言]
AIは間違いなく人間の創造性を革命的に高めます！
想像してみてください、AIが創作のパートナーとなり...
--------------------------------------------------

[相槌役の発言]
確かに興味深い視点ですね。ただし、AIに頼りすぎると
人間本来の創造力が衰退する可能性も...
--------------------------------------------------

[判定役の発言]
両者の意見を踏まえると、AIは適切に活用すれば
創造性を高める強力なツールになります...

以上で議論を終了します。
--------------------------------------------------

対話ログを保存しました: conversation_logs/direct_session_20250809_123456.json
```

## ログ機能

- 全ての対話は`conversation_logs/`にJSON形式で自動保存
- ファイル名: `direct_session_YYYYMMDD_HHMMSS.json`
- 後から分析や参照が可能

## プロジェクト構造

```
multi-agent-decision-system/
├── main_direct.py       # メインプログラム
├── requirements.txt     # 依存関係（openai, python-dotenv）
├── .env                 # OpenAI API設定
├── design_spec.md       # 詳細設計書
├── README.md            # このファイル
└── conversation_logs/   # 対話ログ保存ディレクトリ
```

## コスト目安

- **gpt-3.5-turbo**: 約$0.01-0.03/回
- **gpt-4**: 約$0.10-0.30/回

## トラブルシューティング

### APIキーエラー
```
警告: OPENAI_API_KEY が設定されていません
```
→ `.env`ファイルでAPIキーを正しく設定してください

### レート制限エラー
```
APIエラー: Rate limit exceeded
```
→ しばらく待ってから再実行してください

詳細な設計については`design_spec.md`を参照してください。
