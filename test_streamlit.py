#!/usr/bin/env python3
"""
Streamlitアプリケーションのテストスクリプト
"""

import sys
import os
import importlib.util

def test_imports():
    """必要なモジュールのインポートテスト"""
    print("🔍 モジュールインポートテスト")
    
    required_modules = [
        'streamlit',
        'plotly',
        'pandas',
        'main_intelligent_collaboration',
        'result_analyzer',
        'html_viewer'
    ]
    
    all_good = True
    for module_name in required_modules:
        try:
            if module_name in ['main_intelligent_collaboration', 'result_analyzer', 'html_viewer']:
                # ローカルモジュールの場合
                spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
                if spec is None:
                    print(f"❌ {module_name}: ファイルが見つかりません")
                    all_good = False
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✅ {module_name}: OK")
            else:
                # 外部パッケージの場合
                __import__(module_name)
                print(f"✅ {module_name}: OK")
        except ImportError as e:
            print(f"❌ {module_name}: インポートエラー - {e}")
            all_good = False
        except Exception as e:
            print(f"⚠️ {module_name}: 警告 - {e}")
    
    return all_good

def test_environment():
    """環境変数テスト"""
    print("\n🔧 環境変数テスト")
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY: 設定済み")
        return True
    else:
        # .envファイルをチェック
        if os.path.exists(".env"):
            print("📄 .envファイルが見つかりました")
            try:
                from dotenv import load_dotenv
                load_dotenv()
                api_key = os.environ.get("OPENAI_API_KEY")
                if api_key:
                    print("✅ OPENAI_API_KEY: .envから読み込み成功")
                    return True
                else:
                    print("⚠️ .envファイルにOPENAI_API_KEYが設定されていません")
                    return False
            except ImportError:
                print("⚠️ python-dotenvがインストールされていません")
                return False
        else:
            print("⚠️ OPENAI_API_KEYが設定されていません")
            print("💡 .envファイルまたは環境変数で設定してください")
            return False

def test_files():
    """必要なファイルの存在確認"""
    print("\n📁 ファイル存在テスト")
    
    required_files = [
        'streamlit_app.py',
        'main_intelligent_collaboration.py',
        'result_analyzer.py',
        'html_viewer.py',
        'agent_factory.py',
        'collaboration_system.py',
        'web_search_agent.py',
        'mcp_integration.py'
    ]
    
    all_files_exist = True
    for file_name in required_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name}: 存在 ({size} bytes)")
        else:
            print(f"❌ {file_name}: ファイルが見つかりません")
            all_files_exist = False
    
    return all_files_exist

def test_streamlit_config():
    """Streamlit設定テスト"""
    print("\n⚙️ Streamlit設定テスト")
    
    try:
        import streamlit as st
        print("✅ Streamlit: インポートOK")
        
        # 設定ファイルの確認
        config_file = ".streamlit/config.toml"
        if os.path.exists(config_file):
            print(f"✅ 設定ファイル: {config_file} 存在")
        else:
            print(f"⚠️ 設定ファイル: {config_file} なし（デフォルト設定を使用）")
        
        return True
    except Exception as e:
        print(f"❌ Streamlit設定エラー: {e}")
        return False

def main():
    """メインテスト実行"""
    print("🧪 Streamlitアプリケーション テストスイート")
    print("=" * 50)
    
    tests = [
        ("モジュールインポート", test_imports),
        ("環境変数", test_environment),
        ("必要ファイル", test_files),
        ("Streamlit設定", test_streamlit_config)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name}テストでエラー: {e}")
            results[test_name] = False
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("📊 テスト結果サマリー")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 総合結果: {passed}/{total} テスト通過")
    
    if passed == total:
        print("🎉 全てのテストが成功！Streamlitアプリは正常に動作する準備ができています。")
        print("\n🚀 起動方法:")
        print("  ./start_gui.sh")
        print("  または")
        print("  streamlit run streamlit_app.py")
        return True
    else:
        print("⚠️ いくつかのテストが失敗しました。修正が必要です。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)