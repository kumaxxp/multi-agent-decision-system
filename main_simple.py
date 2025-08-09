"""
シンプルなテスト版 - AutoGenの新しいAPIに対応
"""

import os
import sys
from typing import Dict, Any
from datetime import datetime
import json

def simple_conversation(user_input: str):
    """シンプルなAutoGenテスト（OpenAI API使用）"""
    
    print(f"\n=== 多エージェント対話システム（テスト版） ===")
    print(f"ユーザー入力: {user_input}\n")
    
    try:
        # 新しいAutogen APIを使用
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.conditions import MaxMessageTermination
        from autogen_agentchat.teams import RoundRobinGroupChat
        
        # LLM設定
        llm_config = {
            "model": "gpt-3.5-turbo",
            "api_key": os.environ.get("OPENAI_API_KEY", "test-key"),
            "temperature": 0.7,
        }
        
        # エージェント作成
        speaker = ConversableAgent(
            name="語り手",
            system_message="あなたは創造的な語り手です。大胆で自由な発想で意見を述べてください。",
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
        
        verifier = ConversableAgent(
            name="相槌役", 
            system_message="あなたは慎重な相槌役です。語り手の発言を注意深く聞き、内容を確認してください。",
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
        
        judge = ConversableAgent(
            name="判定役",
            system_message="あなたは公平な判定役です。議論を整理し、バランスの取れた結論を導いてください。",
            llm_config=llm_config,
            human_input_mode="NEVER",
        )
        
        print("エージェントを作成しました。対話を開始します...\n")
        
        # 順次対話
        print("[語り手の発言]")
        speaker_response = speaker.generate_reply(messages=[{"role": "user", "content": user_input}])
        print(speaker_response)
        print("-" * 50)
        
        print("\n[相槌役の発言]")  
        verifier_response = verifier.generate_reply(messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": speaker_response}
        ])
        print(verifier_response)
        print("-" * 50)
        
        print("\n[判定役の発言]")
        judge_response = judge.generate_reply(messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": f"語り手: {speaker_response}"},
            {"role": "assistant", "content": f"相槌役: {verifier_response}"}
        ])
        print(judge_response)
        print("-" * 50)
        
        # ログ保存
        save_log(user_input, speaker_response, verifier_response, judge_response)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("\nOpenAI APIキーが設定されていない可能性があります。")
        print("環境変数 OPENAI_API_KEY を設定してください。")


def save_log(user_input, speaker_response, verifier_response, judge_response):
    """対話ログを保存"""
    log_dir = "conversation_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"simple_session_{session_id}.json")
    
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "mode": "simple_test",
        "user_input": user_input,
        "responses": {
            "speaker": speaker_response,
            "verifier": verifier_response, 
            "judge": judge_response
        }
    }
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n対話ログを保存しました: {log_file}")


if __name__ == "__main__":
    # 環境変数読み込み
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # 入力取得
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("議論したいトピックを入力してください: ")
    
    # 対話実行
    simple_conversation(user_input)