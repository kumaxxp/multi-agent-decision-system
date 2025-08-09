"""
拡張多エージェント対話システムのテスト版
インタラクティブ入力なしで動作確認
"""

import os
import sys
from main_extended import ExtendedMultiAgentSystem

def test_extended_system():
    """拡張システムのテスト実行"""
    
    # 環境変数読み込み
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    if not os.environ.get("OPENAI_API_KEY"):
        print("エラー: OPENAI_API_KEY が設定されていません。")
        return
    
    # システム初期化
    system = ExtendedMultiAgentSystem()
    
    print(f"\n=== 拡張多エージェント対話システム テスト ===")
    print(f"セッションID: {system.conversation_manager.session_id}")
    
    # 利用可能なツールを表示
    available_tools = [f"{name}: {'✅' if status else '❌'}" 
                     for name, status in system.mcp_tools.available_tools.items()]
    if available_tools:
        print(f"\n利用可能なMCPツール:")
        for tool in available_tools:
            print(f"  - {tool}")
    
    # テストトピック
    test_topics = [
        "FastAPIとDjangoフレームワークの詳細比較分析",
        "最新のPythonライブラリについて調べてください"
    ]
    
    for i, topic in enumerate(test_topics, 1):
        print(f"\n{'='*60}")
        print(f"テストラウンド {i}")
        print(f"トピック: {topic}")
        print(f"{'='*60}")
        
        # 1ラウンドだけ実行してテスト
        should_continue = system.run_conversation_round(topic)
        
        if should_continue:
            print(f"\n✓ ラウンド{i}完了 - システムは継続を提案")
        else:
            print(f"\n✓ ラウンド{i}完了 - システムは終了を提案")
        
        print(f"\n対話履歴数: {len(system.conversation_manager.conversation_history)}")
    
    # ログ保存
    log_file = system.conversation_manager.save_log()
    print(f"\n=== テスト完了 ===")
    print(f"ログファイル: {log_file}")


if __name__ == "__main__":
    test_extended_system()