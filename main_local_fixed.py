"""
完全ローカル多エージェント対話システム
OpenAI APIキー不要、LM Studioのモデルを直接使用
"""

import os
import sys
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any


def find_local_llm_server():
    """ローカルLLMサーバーを検出"""
    
    # 一般的なローカルLLMサーバーのポート
    servers = [
        ("LM Studio", "http://localhost:1234/v1"),
        ("Ollama", "http://localhost:11434/v1"), 
        ("Text Generation WebUI", "http://localhost:5000/v1"),
        ("LocalAI", "http://localhost:8080/v1"),
    ]
    
    for name, url in servers:
        try:
            response = requests.get(f"{url}/models", timeout=3)
            if response.status_code == 200:
                models = response.json().get("data", [])
                if models:
                    print(f"✓ {name}サーバーを検出: {url}")
                    print(f"  利用可能モデル: {len(models)}個")
                    return url, models[0].get("id", "local-model")
        except:
            continue
    
    return None, None


def call_local_llm(messages, system_message="", base_url="http://localhost:1234/v1", model="local-model"):
    """ローカルLLMを呼び出し"""
    
    try:
        # システムメッセージを追加
        full_messages = []
        if system_message:
            full_messages.append({"role": "system", "content": system_message})
        full_messages.extend(messages)
        
        # ローカルサーバーにリクエスト
        response = requests.post(
            f"{base_url}/chat/completions",
            json={
                "model": model,
                "messages": full_messages,
                "temperature": 0.7,
                "max_tokens": 500,
                "stream": False
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"サーバーエラー: {response.status_code} - {response.text}"
            
    except requests.exceptions.ConnectionError:
        return "接続エラー: ローカルLLMサーバーに接続できません。LM Studioが起動しているか確認してください。"
    except requests.exceptions.Timeout:
        return "タイムアウト: モデルの応答に時間がかかりすぎています。"
    except Exception as e:
        return f"エラー: {str(e)}"


def run_local_multi_agent_conversation(user_input: str, base_url: str, model: str):
    """ローカルLLMを使用した3エージェント対話"""
    
    print(f"\n=== 多エージェント対話システム（完全ローカル版） ===")
    print(f"LLMサーバー: {base_url}")
    print(f"使用モデル: {model}")
    print(f"ユーザー入力: {user_input}\n")
    
    # エージェントのシステムメッセージ
    agents = {
        "語り手": """あなたは創造的な語り手です。以下の特徴で応答してください：
- 大胆で自由な発想で意見を述べる
- 想像力豊かで時には大げさな表現を使う
- ハルシネーション（創造的な推測）も恐れない
- 議論の方向性を示す火付け役となる
- 日本語で200-300文字程度で応答する""",

        "相槌役": """あなたは慎重な相槌役です。以下の特徴で応答してください：
- 語り手の発言を注意深く分析する
- 良い点は積極的に同意する
- 問題がある点は建設的に指摘する
- 「それは面白い視点ですが...」のような形で修正提案する
- 事実確認や裏付けを重視する
- 日本語で200-300文字程度で応答する""",

        "判定役": """あなたは公平な判定役です。以下の特徴で応答してください：
- これまでの議論を整理する
- 語り手と相槌役の意見を両方考慮する  
- バランスの取れた結論を導く
- 1-2個の代替案を提示する
- 最後に必ず「以上で議論を終了します」と明記する
- 日本語で300-400文字程度で応答する"""
    }
    
    # 対話履歴
    conversation_history = [{"role": "user", "content": user_input}]
    responses = {}
    
    # 各エージェントが順番に発言
    for agent_name, system_msg in agents.items():
        print(f"\n[{agent_name}の発言]")
        print("応答生成中...")
        
        # ローカルLLMを呼び出し
        response = call_local_llm(conversation_history, system_msg, base_url, model)
        responses[agent_name] = response
        
        print(response)
        print("-" * 50)
        
        # 履歴に追加
        conversation_history.append({
            "role": "assistant",
            "content": f"{agent_name}: {response}"
        })
        
        # エラーチェック
        if "エラー" in response or "接続エラー" in response:
            print(f"\n⚠️ {agent_name}の応答でエラーが発生しました。")
            break
            
        # 判定役が終了を宣言したら終了
        if agent_name == "判定役" and "以上で議論を終了します" in response:
            break
    
    # ログ保存
    save_local_conversation_log(user_input, responses, base_url, model)
    
    print("\n=== 対話完了 ===")


def save_local_conversation_log(user_input: str, responses: dict, base_url: str, model: str):
    """ローカル対話ログを保存"""
    log_dir = "conversation_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"local_session_{session_id}.json")
    
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "mode": "local_llm",
        "llm_server": base_url,
        "model": model,
        "user_input": user_input,
        "responses": responses
    }
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 対話ログを保存しました: {log_file}")


def main():
    """メイン実行関数"""
    
    print("=== 完全ローカル多エージェント対話システム ===")
    print("OpenAI APIキー不要 - LM Studioやその他のローカルLLMサーバーを使用\n")
    
    # ローカルLLMサーバーを検出
    print("ローカルLLMサーバーを検索中...")
    base_url, model = find_local_llm_server()
    
    if not base_url:
        print("❌ ローカルLLMサーバーが見つかりません。\n")
        print("以下のいずれかを起動してください：")
        print("1. LM Studio - Local Server (ポート1234)")
        print("2. Ollama (ポート11434)")  
        print("3. Text Generation WebUI (ポート5000)")
        print("4. LocalAI (ポート8080)")
        print("\nLM Studioの場合:")
        print("- LM Studioを起動")
        print("- モデル(openai/gpt-oss-20b等)をロード")
        print("- 'Local Server'タブで'Start Server'をクリック")
        return
    
    # 入力取得
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("\n議論したいトピックを入力してください: ")
    
    # ローカル対話実行
    run_local_multi_agent_conversation(user_input, base_url, model)


if __name__ == "__main__":
    main()