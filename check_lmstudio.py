"""
LM Studio接続チェックスクリプト
LM Studioが正しく設定されているか確認します
"""

import requests
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def check_lmstudio_connection():
    """LM Studioへの接続を確認"""
    base_url = os.environ.get("API_BASE_URL", "http://localhost:1234/v1")
    model_name = os.environ.get("MODEL_NAME", "test-model")
    
    print(f"=== LM Studio 接続チェック ===")
    print(f"URL: {base_url}")
    print(f"モデル: {model_name}")
    print()
    
    # 1. サーバーの稼働確認
    try:
        response = requests.get(f"{base_url}/models", timeout=5)
        if response.status_code == 200:
            print("✓ LM Studioサーバーが稼働しています")
            models = response.json().get("data", [])
            if models:
                print("\n利用可能なモデル:")
                for model in models:
                    print(f"  - {model.get('id', 'unknown')}")
            else:
                print("⚠ モデルがロードされていません")
                print("  LM Studioでモデルをロードしてください")
        else:
            print(f"✗ サーバーエラー: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ LM Studioに接続できません")
        print("  1. LM Studioが起動しているか確認してください")
        print("  2. Local Serverが開始されているか確認してください")
        print("  3. ポート1234が正しいか確認してください")
        return False
    except Exception as e:
        print(f"✗ エラー: {e}")
        return False
    
    # 2. チャット機能のテスト
    print("\n=== チャット機能テスト ===")
    try:
        test_message = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "こんにちは"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            json=test_message,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✓ チャット機能が正常に動作しています")
            result = response.json()
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"\nテスト応答: {reply[:100]}...")
            return True
        else:
            print(f"✗ チャットエラー: {response.status_code}")
            print(f"  詳細: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ チャットテストエラー: {e}")
        return False


if __name__ == "__main__":
    if check_lmstudio_connection():
        print("\n✓ LM Studioは正しく設定されています！")
        print("  main.pyを実行できます")
    else:
        print("\n✗ LM Studioの設定を確認してください")
        print("  詳細はlmstudio_setup.mdを参照してください")