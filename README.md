# 🤖 インテリジェント協調多エージェントシステム

## 📋 概要

OpenAI GPTを使用した高度な多エージェント議論システム。動的エージェント生成、協調分析、Web検索統合、美しいStreamlit GUIを備えた完全なソリューション。

## ✨ 主要機能

### 🎯 コア機能
- **動的エージェント生成**: トピックに応じた専門エージェントの自動生成
- **インテリジェント協調**: 対立解決、合意形成、投票システム
- **Web検索統合**: リアルタイム情報収集、ファクトチェック、トレンド分析
- **美しいGUI**: Streamlitによる直感的なWebインターフェース
- **詳細分析**: 包括的な議論分析と可視化

### 🚀 システム構成

#### 1. メインシステム (`main_intelligent_collaboration.py`)
- 完全統合版のインテリジェント協調システム
- 動的エージェント生成、Web検索、協調分析を統合
- JSONログ出力、詳細な分析機能

#### 2. シンプル版 (`main_direct.py`)
- 基本的な3エージェント議論システム
- 軽量で高速な実行
- プロトタイピングやテストに最適

#### 3. Streamlit GUI (`streamlit_app.py`)
- 美しいWebインターフェース
- リアルタイム議論実行
- 詳細な会話表示とHTML報告書表示
- インタラクティブな分析グラフ

## 🛠️ インストール

### 必要要件
- Python 3.8以上
- OpenAI API Key

### セットアップ
```bash
# リポジトリのクローン
git clone [repository-url]
cd multi-agent-decision-system

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

## 🚀 使用方法

### GUI版（推奨）
```bash
# Streamlitアプリ起動
streamlit run streamlit_app.py

# または専用ランチャー
./start_gui.sh

# またはPythonラッパー
python run_gui.py
```

ブラウザで http://localhost:8501 を開いてアクセス

### コマンドライン版
```bash
# インテリジェント協調システム
python main_intelligent_collaboration.py "議論トピック"

# シンプル版
python main_direct.py "議論トピック"

# 結果分析
python result_analyzer.py --list
python result_analyzer.py --session [session_id]

# HTML報告書生成
python html_viewer.py --all
```

## 📁 ファイル構成

### コアシステム
- `main_intelligent_collaboration.py` - メイン統合システム
- `main_direct.py` - シンプル版システム
- `agent_factory.py` - 動的エージェント生成
- `collaboration_system.py` - 協調・対立解決システム
- `web_search_agent.py` - Web検索・ファクトチェック
- `mcp_integration.py` - MCP統合

### GUI・表示
- `streamlit_app.py` - Streamlit GUIアプリケーション
- `html_viewer.py` - HTML報告書生成
- `result_analyzer.py` - 結果分析ツール

### ユーティリティ
- `run_gui.py` - GUI起動スクリプト
- `start_gui.sh` - シェル起動スクリプト
- `test_integration.py` - 統合テスト
- `test_streamlit.py` - Streamlitテスト

### 設定・ドキュメント
- `requirements.txt` - Python依存関係
- `.streamlit/config.toml` - Streamlit設定
- `.gitignore` - Git除外設定
- `design_spec.md` - 設計仕様書

## 🎨 GUI機能詳細

### モード
1. **🚀 新しい議論を開始**
   - トピック入力
   - エージェント数・ラウンド数設定
   - リアルタイム実行とプログレス表示

2. **📊 過去の議論を分析**
   - セッション選択
   - 詳細分析表示
   - インタラクティブグラフ

3. **📋 セッション一覧**
   - 全セッション管理
   - 個別分析・HTML報告書生成

### 新機能
- **💬 会話詳細表示**: エージェント発言の完全表示
- **📄 GUI内HTML報告書**: Streamlit内で直接表示
- **📊 統合ビューア**: タブ切り替えによる情報整理

## 📊 分析機能

### メトリクス
- 合意度推移
- エージェント性能（信頼度、影響力、一貫性）
- 意見分布と進化
- 協調パターン分析

### 出力形式
- JSON詳細ログ
- HTML美麗報告書
- インタラクティブグラフ
- CSV/DataFrame出力

## 🧪 テスト

```bash
# 統合テスト
python test_integration.py

# Streamlitテスト
python test_streamlit.py

# クイックテスト
python test_integration.py --quick
```

## 🔧 カスタマイズ

### エージェント追加
`agent_factory.py`で新しい専門分野を定義：
```python
ExpertiseArea.NEW_FIELD = "new_field"
```

### テーマ変更
`.streamlit/config.toml`でカラー設定をカスタマイズ

### モデル変更
環境変数で使用モデルを指定：
```bash
export MODEL_NAME="gpt-4"
```

## 📈 パフォーマンス

- **処理速度**: 4エージェント3ラウンドで約30-60秒
- **メモリ使用**: 通常100-200MB
- **並行処理**: 非同期処理対応可能

## 🛡️ セキュリティ

- APIキーは環境変数で管理
- ローカルファイルシステムでのログ保存
- XSS/CSRF保護

## 📝 ライセンス

MIT License

## 🤝 貢献

Pull Requestsを歓迎します！

## 📞 サポート

Issues機能で問題報告・機能要望をお寄せください。

## 🎉 更新履歴

### v2.0 (2025-08-09)
- Streamlit GUI実装
- 会話詳細表示機能追加
- GUI内HTML報告書表示
- エラーハンドリング強化

### v1.5
- インテリジェント協調システム実装
- 動的エージェント生成
- Web検索統合

### v1.0
- 初期リリース
- 基本的な3エージェントシステム