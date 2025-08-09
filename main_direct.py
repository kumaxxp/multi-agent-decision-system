"""
直接OpenAI APIを使用した多エージェント対話システム
AutoGenを使わずにシンプルに実装
"""

import os
import sys
from datetime import datetime
import json

def call_openai_api(messages, system_message="", model="gpt-3.5-turbo"):
    """OpenAI APIを直接呼び出し"""
    try:
        import openai
        
        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # システムメッセージを追加
        full_messages = []
        if system_message:
            full_messages.append({"role": "system", "content": system_message})
        full_messages.extend(messages)
        
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"APIエラー: {e}"


def run_multi_agent_conversation(user_input: str):
    """3つのエージェントによる順次対話を実行"""
    
    print(f"\n=== 多エージェント対話システム（直接API版） ===")
    print(f"ユーザー入力: {user_input}\n")
    
    # エージェントのシステムメッセージ
    agents = {
        "語り手": "あなたは創造的な語り手です。大胆で自由な発想で意見を述べ、時には想像力豊かで大げさな表現も使ってください。ハルシネーションも恐れずに、議論の方向性を示してください。",
        
        "相槌役": "あなたは慎重な相槌役です。語り手の発言を注意深く聞き、内容を確認してください。良い点は積極的に同意し、問題がある点は建設的に指摘してください。必要に応じて「それは面白い視点ですが、実際には...」のような形で修正を提案してください。",
        
        "判定役": "あなたは公平な判定役です。これまでの議論を整理し、バランスの取れた結論を導いてください。語り手と相槌役の意見を両方考慮し、最終的な結論と代替案を1-2個提示してください。最後に必ず「以上で議論を終了します」と明記してください。"
    }
    
    # 対話履歴
    conversation_history = [{"role": "user", "content": user_input}]
    responses = {}
    
    # 各エージェントが順番に発言
    for agent_name, system_msg in agents.items():
        print(f"\n[{agent_name}の発言]")
        
        # APIを呼び出し
        response = call_openai_api(conversation_history, system_msg)
        responses[agent_name] = response
        
        print(response)
        print("-" * 50)
        
        # 履歴に追加
        conversation_history.append({
            "role": "assistant", 
            "content": f"{agent_name}: {response}"
        })
        
        # 判定役が終了を宣言したら終了
        if agent_name == "判定役" and "以上で議論を終了します" in response:
            break
    
    # ログ保存
    save_conversation_log(user_input, responses)
    
    print("\n=== 対話完了 ===")


def save_conversation_log(user_input: str, responses: dict):
    """対話ログをJSON形式で保存"""
    log_dir = "conversation_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"direct_session_{session_id}.json")
    
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "mode": "direct_openai_api",
        "user_input": user_input,
        "responses": responses
    }
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n対話ログを保存しました: {log_file}")


def main():
    """メイン実行関数"""
    # 環境変数読み込み
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # OpenAI APIキーの確認
    if not os.environ.get("OPENAI_API_KEY"):
        print("警告: OPENAI_API_KEY が設定されていません。")
        print(".envファイルでAPIキーを設定してください。")
        print("例: OPENAI_API_KEY=sk-...")
        return
    
    # 入力取得
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("議論したいトピックを入力してください: ")
    
    # 対話実行
    run_multi_agent_conversation(user_input)


if __name__ == "__main__":
    main()