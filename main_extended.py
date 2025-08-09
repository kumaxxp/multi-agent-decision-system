"""
拡張多エージェント対話システム
- 継続対話機能
- MCPツール統合
- 対話履歴管理
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import openai

class ConversationManager:
    """対話履歴を管理するクラス"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_history = []
        self.round_count = 0
        self.log_dir = "conversation_logs"
        os.makedirs(self.log_dir, exist_ok=True)
        
    def add_message(self, agent: str, content: str, tools_used: List[str] = None):
        """メッセージを履歴に追加"""
        message = {
            "round": self.round_count,
            "agent": agent,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "tools_used": tools_used or []
        }
        self.conversation_history.append(message)
        
    def get_context_summary(self, max_rounds: int = 3) -> str:
        """直近の対話履歴をサマリーとして取得"""
        if not self.conversation_history:
            return ""
            
        recent_messages = [msg for msg in self.conversation_history 
                          if msg["round"] >= max(0, self.round_count - max_rounds)]
        
        summary = "\n\n=== これまでの議論の流れ ===\n"
        for msg in recent_messages:
            summary += f"ラウンド{msg['round']} [{msg['agent']}]: {msg['content'][:200]}...\n"
        summary += "=== 議論の流れ終了 ===\n\n"
        
        return summary
        
    def save_log(self):
        """対話ログを保存"""
        log_file = os.path.join(self.log_dir, f"extended_session_{self.session_id}.json")
        
        log_data = {
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat(),
            "total_rounds": self.round_count,
            "conversation_history": self.conversation_history
        }
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        return log_file


from mcp_integration import RealMCPIntegration

# MCPツール統合は別モジュールで実装


class ExtendedMultiAgentSystem:
    """拡張多エージェント対話システム"""
    
    def __init__(self):
        self.conversation_manager = ConversationManager()
        self.mcp_tools = RealMCPIntegration()
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # エージェントの定義
        self.agents = {
            "語り手": {
                "role": "creative_storyteller",
                "system_message": """あなたは創造的な語り手です。以下の特徴で応答してください：
- 大胆で自由な発想で意見を述べる
- 前回の議論を発展させて新しい視点を提供する
- 必要に応じてツール使用を提案する（「〇〇について詳しく調べてみましょう」など）
- 議論を深める質問や仮説を提示する
- 日本語で300-400文字程度で応答する""",
            },
            
            "相槌役": {
                "role": "careful_verifier", 
                "system_message": """あなたは慎重な相槌役です。以下の特徴で応答してください：
- これまでの議論の流れを整理する
- 語り手の新しい提案を建設的に検討する
- 事実確認が必要な場合はツール使用を提案する
- 議論の矛盾点や改善点を指摘する
- 次のステップを具体的に提案する
- 日本語で300-400文字程度で応答する""",
            },
            
            "判定役": {
                "role": "strategic_coordinator",
                "system_message": """あなたは戦略的な判定役です。以下の特徴で応答してください：
- これまでの全ラウンドの議論を統合する
- 新たに浮上した課題や論点を整理する
- 次のラウンドに向けた方向性を決定する
- 必要なツールや情報源を特定する
- 継続するかどうかの判断を行う
- 「次のラウンドに進みます」または「議論を終了します」を明記する
- 日本語で400-500文字程度で応答する""",
            }
        }
    
    def call_openai_api(self, messages: List[Dict], system_message: str) -> str:
        """OpenAI APIを呼び出し"""
        try:
            full_messages = [{"role": "system", "content": system_message}]
            full_messages.extend(messages)
            
            response = self.client.chat.completions.create(
                model=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
                messages=full_messages,
                temperature=0.7,
                max_tokens=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"APIエラー: {e}"
    
    def process_tool_requests(self, content: str, agent_role: str) -> tuple[str, List[str]]:
        """エージェントの発言からツール使用要求を処理"""
        tool_results = []
        tools_used = []
        
        # より高度なツール使用の検出と実行
        
        # Context7でのライブラリ検索
        if any(keyword in content for keyword in ["ライブラリ", "API", "フレームワーク"]) and "調べ" in content:
            # 簡易的なライブラリ名抽出
            library_names = self._extract_library_names(content)
            for lib_name in library_names[:2]:  # 最大2つまで
                result = self.mcp_tools.search_library_documentation(lib_name)
                tool_results.append(result)
                tools_used.append("context7")
        
        # Geminiでの詳細分析
        if any(keyword in content for keyword in ["分析", "詳細", "評価", "検討"]):
            analysis_result = self.mcp_tools.analyze_with_gemini(content[:500])  # 長すぎる場合は切り取り
            tool_results.append(analysis_result)
            tools_used.append("gemini-cli")
        
        # コード関連の処理
        if any(keyword in content for keyword in ["コード", "プログラム", "実装"]):
            # コードブロックを抽出して実行
            code_blocks = self._extract_code_blocks(content)
            for code in code_blocks[:1]:  # 1つのコードブロックのみ
                result = self.mcp_tools.execute_code_analysis(code)
                tool_results.append(result)
                tools_used.append("ide")
        
        # ツール使用提案を表示
        suggestions = self.mcp_tools.suggest_tools_for_context(content, agent_role)
        if suggestions:
            suggestion_text = "\n\n💡 ツール使用提案:\n"
            for i, suggestion in enumerate(suggestions, 1):
                suggestion_text += f"{i}. {suggestion['tool']}: {suggestion['action']} - {suggestion['reason']}\n"
            tool_results.append(suggestion_text)
        
        # ツール結果を統合
        enhanced_content = content
        if tool_results:
            tools_info = "\n\n=== ツール実行・提案結果 ===\n"
            tools_info += "\n".join(tool_results)
            tools_info += "\n=== ツール結果終了 ===\n"
            enhanced_content = content + tools_info
        
        return enhanced_content, tools_used
    
    def _extract_library_names(self, content: str) -> List[str]:
        """コンテンツからライブラリ名を抽出"""
        # 簡易的な実装（実際はより高度なNLP処理が必要）
        common_libraries = [
            "python", "react", "vue", "django", "flask", "numpy", "pandas", 
            "tensorflow", "pytorch", "scikit-learn", "fastapi", "express",
            "spring", "angular", "bootstrap", "jquery"
        ]
        
        found_libs = []
        content_lower = content.lower()
        for lib in common_libraries:
            if lib in content_lower:
                found_libs.append(lib)
        
        return found_libs or ["python"]  # デフォルトはpython
    
    def _extract_code_blocks(self, content: str) -> List[str]:
        """コンテンツからコードブロックを抽出"""
        # 簡易的な実装
        code_blocks = []
        
        # ```で囲まれたコードブロックを検出
        import re
        pattern = r'```(?:\w+)?\n?(.*?)\n?```'
        matches = re.findall(pattern, content, re.DOTALL)
        code_blocks.extend(matches)
        
        # インラインコードも検出（簡易版）
        if not code_blocks:
            inline_pattern = r'`([^`]+)`'
            inline_matches = re.findall(inline_pattern, content)
            code_blocks.extend(inline_matches[:2])
        
        return [code.strip() for code in code_blocks if code.strip()]
    
    def run_conversation_round(self, user_input: str = None) -> bool:
        """1ラウンドの対話を実行。継続する場合はTrue、終了する場合はFalseを返す"""
        
        self.conversation_manager.round_count += 1
        print(f"\n{'='*60}")
        print(f"ラウンド {self.conversation_manager.round_count}")
        print(f"{'='*60}")
        
        if user_input:
            print(f"新しい入力: {user_input}")
            
        # 対話履歴のコンテキストを準備
        context = self.conversation_manager.get_context_summary()
        
        # 各エージェントが順番に発言
        current_messages = []
        if user_input:
            current_messages.append({"role": "user", "content": user_input})
        
        continue_conversation = False
        
        for agent_name, agent_config in self.agents.items():
            print(f"\n[{agent_name}の発言]")
            
            # システムメッセージにコンテキストを追加
            enhanced_system_message = agent_config["system_message"] + f"\n\n{context}"
            
            # API呼び出し
            response = self.call_openai_api(current_messages, enhanced_system_message)
            
            # ツール処理
            enhanced_response, tools_used = self.process_tool_requests(response, agent_config["role"])
            
            print(enhanced_response)
            print("-" * 50)
            
            # 履歴に追加
            self.conversation_manager.add_message(agent_name, enhanced_response, tools_used)
            
            # 対話履歴を更新
            current_messages.append({
                "role": "assistant",
                "content": f"{agent_name}: {enhanced_response}"
            })
            
            # 判定役が継続を決定したかチェック
            if agent_name == "判定役":
                if "次のラウンドに進みます" in enhanced_response:
                    continue_conversation = True
                elif "議論を終了します" in enhanced_response:
                    continue_conversation = False
        
        return continue_conversation
    
    def run_extended_conversation(self, initial_topic: str):
        """拡張対話システムのメイン実行"""
        print(f"\n=== 拡張多エージェント対話システム ===")
        print(f"セッションID: {self.conversation_manager.session_id}")
        print(f"初期トピック: {initial_topic}")
        
        # 利用可能なツールを表示
        available_tools = [f"{name}: {'✅' if status else '❌'}" 
                         for name, status in self.mcp_tools.available_tools.items()]
        if available_tools:
            print(f"\n利用可能なMCPツール:")
            for tool in available_tools:
                print(f"  - {tool}")
        
        current_input = initial_topic
        max_rounds = 5  # 最大ラウンド数
        
        # 対話ループ
        for round_num in range(max_rounds):
            try:
                should_continue = self.run_conversation_round(current_input if round_num == 0 else None)
                
                if not should_continue:
                    print(f"\n判定役により議論が終了されました（ラウンド{round_num + 1}）")
                    break
                    
                # 2ラウンド目以降はユーザーが追加入力できる
                if round_num < max_rounds - 1:
                    print(f"\n--- ラウンド{round_num + 1}完了 ---")
                    user_continue = input("続行しますか？ (Enter: 続行, 'q': 終了, その他: 追加入力): ").strip()
                    
                    if user_continue.lower() == 'q':
                        print("ユーザーにより対話を終了します。")
                        break
                    elif user_continue and user_continue.lower() != '':
                        current_input = user_continue
                    else:
                        current_input = None
                        
            except KeyboardInterrupt:
                print("\n\n対話が中断されました。")
                break
        
        # セッション終了
        log_file = self.conversation_manager.save_log()
        print(f"\n=== 拡張対話セッション終了 ===")
        print(f"総ラウンド数: {self.conversation_manager.round_count}")
        print(f"対話ログ保存: {log_file}")


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
        print("エラー: OPENAI_API_KEY が設定されていません。")
        print(".envファイルでAPIキーを設定してください。")
        return
    
    # 初期トピック取得
    if len(sys.argv) > 1:
        initial_topic = " ".join(sys.argv[1:])
    else:
        initial_topic = input("議論したいトピックを入力してください: ")
    
    # 拡張対話システム実行
    system = ExtendedMultiAgentSystem()
    system.run_extended_conversation(initial_topic)


if __name__ == "__main__":
    main()