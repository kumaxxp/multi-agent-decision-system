"""
デモ実行スクリプト（モデルなしでも動作確認可能）
"""

import os
import sys
from datetime import datetime
import json

def demo_conversation(user_input: str):
    """モデルを使わないデモ対話"""
    
    print(f"\n=== 多エージェント対話システム（デモモード） ===")
    print(f"セッションID: {datetime.now().strftime('%Y%m%d_%H%M%S')}")
    print(f"ユーザー入力: {user_input}\n")
    
    # デモ用の対話シミュレーション
    conversations = [
        {
            "agent": "語り手",
            "content": f"「{user_input}」について、私は壮大な物語を語りましょう！これは人類の歴史を変える可能性を秘めた深遠なテーマです。想像してみてください、このトピックが世界中で議論され、新しい文明の礎となる日を...！"
        },
        {
            "agent": "相槌役",
            "content": "なるほど、確かに興味深い視点ですね。ただ、少し大げさかもしれません。実際のところ、このトピックにはもっと現実的な側面もあります。具体的なデータや事例を見てみると..."
        },
        {
            "agent": "判定役",
            "content": f"両者の意見を踏まえて結論を述べます。「{user_input}」については、理想と現実のバランスを考慮することが重要です。\n\n【結論】\n状況に応じた柔軟な対応が必要\n\n【代替案】\n1. 段階的なアプローチを採用\n2. 定期的な見直しと改善\n\n以上で議論を終了します。"
        }
    ]
    
    # 対話を表示
    for conv in conversations:
        print(f"\n[{conv['agent']}]")
        print(conv['content'])
        print("-" * 50)
    
    # ログ保存
    log_dir = "conversation_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"demo_session_{session_id}.json")
    
    log_data = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "mode": "demo",
        "user_input": user_input,
        "conversations": conversations
    }
    
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nデモ対話ログを保存しました: {log_file}")


if __name__ == "__main__":
    print("=== 多エージェント対話システム - デモ版 ===")
    print("注意: これはモデルを使用しないデモ版です。")
    print("実際のモデルを使用するには：")
    print("1. LM Studioで openai/gpt-oss-20b をダウンロード")
    print("2. .envファイルでMODEL_PATHを設定")
    print("3. python main_local.py を実行\n")
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("議論したいトピックを入力してください: ")
    
    demo_conversation(user_input)