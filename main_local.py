"""
Main entry point for the Multi-Agent Decision System with local model support.
LM Studioでダウンロードしたモデルファイルを直接使用します。
"""

import os
import sys
from typing import Dict, Any
from autogen import ConversableAgent, GroupChat, GroupChatManager
from agents import create_speaker_agent, create_verifier_agent, create_judge_agent
import json
from datetime import datetime
from local_llm import get_local_llm_config, local_llm_wrapper


def setup_agents_with_local_llm(llm_config: Dict[str, Any]):
    """ローカルLLMを使用してエージェントをセットアップ"""
    
    # カスタムLLMラッパーを使用する設定
    custom_config = {
        "config_list": [{
            "model": "local-model",
            "api_type": "custom",
            "base_url": "custom",
            "api_key": "not-needed",
        }],
        "functions": None,
        "timeout": 600,
        "temperature": llm_config.get("temperature", 0.7),
        "max_tokens": llm_config.get("max_tokens", 512),
    }
    
    # カスタムLLMクライアントを設定
    wrapper = local_llm_wrapper(llm_config)
    
    # 各エージェントにカスタムクライアントを設定
    speaker = create_speaker_agent(custom_config)
    speaker.client = wrapper
    
    verifier = create_verifier_agent(custom_config)
    verifier.client = wrapper
    
    judge = create_judge_agent(custom_config)
    judge.client = wrapper
    
    return speaker, verifier, judge


def create_sequential_chat(agents, max_round: int = 5):
    """Sequential Workflowを実現するグループチャット"""
    speaker, verifier, judge = agents
    
    def speaker_selector(last_speaker, group_chat):
        """発言順序を制御: user -> speaker -> verifier -> judge"""
        messages = group_chat.messages
        
        if len(messages) <= 1:
            return speaker
        
        last_name = last_speaker.name if last_speaker else None
        
        if last_name == "語り手":
            return verifier
        elif last_name == "相槌役":
            return judge
        elif last_name == "判定役":
            return None
        else:
            return speaker
    
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=max_round,
        speaker_selection_method=speaker_selector,
        allow_repeat_speaker=False,
    )
    
    # GroupChatManagerにもカスタムLLM設定を適用
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=False,  # マネージャー自体はLLMを使わない
    )
    
    return group_chat, manager


def save_conversation_log(messages, session_id: str):
    """対話ログをJSON形式で保存"""
    log_dir = "conversation_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"session_{session_id}.json")
    
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "messages": messages,
    }
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n対話ログを保存しました: {log_file}")


def run_conversation(user_input: str, llm_config: Dict[str, Any]):
    """エージェント間の対話を実行"""
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n=== 多エージェント対話システム（ローカルモデル版） ===")
    print(f"セッションID: {session_id}")
    print(f"ユーザー入力: {user_input}\n")
    
    # エージェントのセットアップ
    try:
        speaker, verifier, judge = setup_agents_with_local_llm(llm_config)
        agents = [speaker, verifier, judge]
    except Exception as e:
        print(f"エージェントのセットアップに失敗しました: {e}")
        return
    
    # Sequential Workflowの作成
    group_chat, manager = create_sequential_chat(agents, max_round=6)
    
    # ユーザープロキシ
    user_proxy = ConversableAgent(
        name="ユーザー",
        llm_config=False,
        human_input_mode="NEVER",
    )
    
    # 対話の開始
    try:
        user_proxy.initiate_chat(
            manager,
            message=user_input,
            clear_history=True,
        )
    except Exception as e:
        print(f"対話中にエラーが発生しました: {e}")
    
    # 対話ログの保存
    messages = [
        {
            "role": msg.get("role", "assistant"),
            "name": msg.get("name", "unknown"),
            "content": msg.get("content", ""),
        }
        for msg in group_chat.messages
    ]
    save_conversation_log(messages, session_id)
    
    print("\n=== 対話終了 ===")


if __name__ == "__main__":
    # 環境変数の読み込み
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # ローカルLLM設定の取得
    try:
        llm_config = get_local_llm_config()
    except FileNotFoundError as e:
        print(f"エラー: {e}")
        sys.exit(1)
    
    # コマンドライン引数またはデフォルトの入力
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("議論したいトピックを入力してください: ")
    
    # 対話の実行
    run_conversation(user_input, llm_config)