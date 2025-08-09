#!/bin/bash

echo "🤖 インテリジェント協調多エージェントシステム - GUI起動"
echo "=" * 60

# 環境変数チェック
if [ -z "$OPENAI_API_KEY" ] && [ ! -f ".env" ]; then
    echo "⚠️ 警告: OPENAI_API_KEYが設定されていません"
    echo "💡 .envファイルを作成するか、環境変数を設定してください"
    echo ""
fi

# .envファイルがある場合は読み込み
if [ -f ".env" ]; then
    echo "📄 .envファイルを読み込み中..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# 依存関係チェック
echo "🔍 依存関係をチェック中..."
python -c "import streamlit, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 必要なパッケージがインストールされていません"
    echo "📦 以下のコマンドでインストールしてください:"
    echo "   pip install streamlit plotly"
    exit 1
fi

echo "✅ 依存関係OK"

# ポート確認
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️ ポート8501は既に使用されています"
    echo "🔄 既存のStreamlitプロセスを終了しています..."
    pkill -f "streamlit run"
    sleep 2
fi

# Streamlit起動
echo "🚀 Streamlitアプリを起動中..."
echo "📱 ブラウザで http://localhost:8501 が開きます"
echo "⏹️ 終了するには Ctrl+C を押してください"
echo ""

streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --theme.base light \
    --theme.primaryColor "#1f77b4"