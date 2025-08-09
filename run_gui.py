#!/usr/bin/env python3
"""
Streamlit GUIアプリケーション起動スクリプト
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """必要な依存関係をチェック"""
    try:
        import streamlit
        import plotly
        print("✅ 必要なパッケージがインストール済みです")
        return True
    except ImportError as e:
        print(f"❌ 必要なパッケージがインストールされていません: {e}")
        print("📦 以下のコマンドでインストールしてください:")
        print("   pip install streamlit plotly")
        return False

def check_environment():
    """環境変数をチェック"""
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️ OPENAI_API_KEYが設定されていません")
        print("💡 .envファイルまたは環境変数でAPIキーを設定してください")
        return False
    return True

def run_streamlit_app():
    """Streamlitアプリを起動"""
    script_path = Path(__file__).parent / "streamlit_app.py"
    
    print("🚀 Streamlitアプリを起動中...")
    print("📱 ブラウザで http://localhost:8501 が開きます")
    print("⏹️ 終了するには Ctrl+C を押してください")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(script_path),
            "--theme.base", "light",
            "--theme.primaryColor", "#1f77b4",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 アプリケーションを終了しました")
    except subprocess.CalledProcessError as e:
        print(f"❌ アプリケーションの起動に失敗しました: {e}")

def main():
    """メイン実行関数"""
    print("🤖 インテリジェント協調多エージェントシステム - GUI版")
    print("=" * 60)
    
    # 依存関係チェック
    if not check_dependencies():
        return
    
    # 環境変数チェック（警告のみ、起動は継続）
    check_environment()
    
    # Streamlitアプリ起動
    run_streamlit_app()

if __name__ == "__main__":
    main()