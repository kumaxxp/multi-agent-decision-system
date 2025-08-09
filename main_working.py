"""
動作する多エージェント対話システム - 新AutoGen API対応版
"""

import os
import sys
import asyncio
from typing import Dict, Any
from datetime import datetime
import json

async def run_multi_agent_chat(user_input: str):
    """新しいAutoGen APIを使用した対話"""
    
    print(f"\n=== 多エージェント対話システム ===")
    print(f"ユーザー入力: {user_input}\n")
    
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.conditions import MaxMessageTermination
        from autogen_agentchat.teams import RoundRobinGroupChat
        from autogen_agentchat.ui import Console
        from autogen_core.models import OpenAIChatCompletionClient
        
        # LLM クライアント設定
        model_client = OpenAIChatCompletionClient(
            model="gpt-3.5-turbo",
            api_key=os.environ.get("OPENAI_API_KEY", "test-key"),
        )
        
        # エージェント作成
        speaker_agent = AssistantAgent(
            name="語り手",
            description="創造的で大胆な発想を行うエージェント",
            system_message="あなたは創造的な語り手です。大胆で自由な発想で意見を述べ、時には想像力豊かな表現も使ってください。",
            model_client=model_client,
        )
        
        verifier_agent = AssistantAgent(
            name="相槌役",
            description="慎重に内容を確認し、建設的な意見を述べるエージェント", 
            system_message="あなたは慎重な相槌役です。語り手の発言を注意深く聞き、良い点は同意し、問題がある点は建設的に指摘してください。",
            model_client=model_client,
        )
        
        judge_agent = AssistantAgent(
            name="判定役",
            description="議論を整理し、結論を導くエージェント",
            system_message="あなたは公平な判定役です。これまでの議論を整理し、バランスの取れた結論と代替案を提示してください。最後に「以上で議論を終了します」と明記してください。",
            model_client=model_client,
        )
        
        # チーム作成（順次発言）
        team = RoundRobinGroupChat([speaker_agent, verifier_agent, judge_agent])
        
        # 対話実行
        result = await team.run(
            task=user_input,
            termination_condition=MaxMessageTermination(max_messages=6)
        )
        
        # 結果表示
        print("\n=== 対話結果 ===")
        for message in result.messages:
            print(f"\n[{message.source}]")
            print(message.content)
            print("-" * 50)
        
        # ログ保存
        save_conversation_log(user_input, result.messages)
        
    except ImportError as e:
        print(f"Import エラー: {e}")
        print("必要なパッケージがインストールされていません。")
        
    except Exception as e:
        print(f"実行エラー: {e}")
        print("OpenAI APIキーが正しく設定されているか確認してください。")


def save_conversation_log(user_input: str, messages):
    """対話ログをJSON形式で保存"""
    log_dir = "conversation_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"working_session_{session_id}.json")
    
    # メッセージをシリアライズ可能な形式に変換
    serialized_messages = []
    for msg in messages:
        serialized_messages.append({
            "source": getattr(msg, 'source', 'unknown'),
            "content": getattr(msg, 'content', str(msg)),
            "type": str(type(msg).__name__)
        })
    
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "messages": serialized_messages
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
    
    # 入力取得
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("議論したいトピックを入力してください: ")
    
    # 非同期実行
    asyncio.run(run_multi_agent_chat(user_input))


if __name__ == "__main__":
    main()