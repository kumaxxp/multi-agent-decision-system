"""
インテリジェント協調多エージェントシステム
動的エージェント生成 + 高度な協調機能を統合
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import openai

# 新機能モジュールのインポート
from agent_factory import AgentFactory, AgentProfile, ExpertiseArea
from collaboration_system import (
    CollaborationOrchestrator, Opinion, OpinionType, 
    ConflictLevel, Consensus
)
from web_search_agent import WebSearchAgent, FactChecker, TrendAnalyzer
from mcp_integration import RealMCPIntegration


class IntelligentCollaborationSystem:
    """インテリジェント協調システム"""
    
    def __init__(self):
        # 基本コンポーネント
        self.openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # 新機能コンポーネント
        self.agent_factory = AgentFactory()
        self.collaboration_orchestrator = CollaborationOrchestrator()
        self.web_searcher = WebSearchAgent()
        self.fact_checker = FactChecker(self.web_searcher)
        self.trend_analyzer = TrendAnalyzer(self.web_searcher)
        self.mcp_tools = RealMCPIntegration()
        
        # セッション管理
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_log = []
        self.analysis_results = []
        
    def run_intelligent_discussion(self, topic: str, num_agents: int = 4, max_rounds: int = 3) -> Dict[str, Any]:
        """インテリジェントな議論を実行"""
        
        print(f"\n🚀 === インテリジェント協調多エージェントシステム ===")
        print(f"📅 セッションID: {self.session_id}")
        print(f"💭 議論トピック: {topic}")
        print(f"👥 エージェント数: {num_agents}")
        print(f"🔄 最大ラウンド数: {max_rounds}")
        
        # Phase 1: 動的エージェント生成
        print(f"\n🎭 Phase 1: 専門エージェント生成")
        agents = self._generate_specialized_agents(topic, num_agents)
        
        # Phase 2: 背景情報収集
        print(f"\n🔍 Phase 2: 背景情報収集・分析")
        background_info = self._gather_background_information(topic)
        
        # Phase 3: 多ラウンド議論
        print(f"\n💬 Phase 3: インテリジェント議論開始")
        discussion_results = []
        
        for round_num in range(1, max_rounds + 1):
            print(f"\n{'='*60}")
            print(f"🔄 ラウンド {round_num}")
            print(f"{'='*60}")
            
            round_result = self._execute_discussion_round(
                agents, topic, round_num, background_info, discussion_results
            )
            
            # 協調分析（Opinionオブジェクトのまま実行）
            collaboration_analysis = self._analyze_collaboration(round_result["opinions"])
            round_result["collaboration_analysis"] = collaboration_analysis
            
            # 辞書形式に変換してから結果に追加
            round_result["opinions"] = [self._opinion_to_dict(opinion) for opinion in round_result["opinions"]]
            discussion_results.append(round_result)
            
            print(f"\n📊 ラウンド{round_num}協調分析:")
            self._display_collaboration_summary(collaboration_analysis)
            
            # 終了条件チェック
            if self._should_end_discussion(collaboration_analysis):
                print(f"\n✅ 十分な合意が形成されました。議論を終了します。")
                break
        
        # Phase 4: 最終統合・結論
        print(f"\n🎯 Phase 4: 最終統合・結論生成")
        final_conclusion = self._generate_final_conclusion(discussion_results, topic)
        
        # 結果構造の生成
        session_result = {
            "session_info": {
                "session_id": self.session_id,
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "num_agents": num_agents,
                "max_rounds": max_rounds,
                "actual_rounds": len(discussion_results)
            },
            "agents": [self._agent_profile_to_dict(agent) for agent in agents],
            "background_info": background_info,
            "discussion_rounds": discussion_results,
            "final_conclusion": final_conclusion,
            "overall_collaboration_metrics": self._calculate_overall_metrics(discussion_results)
        }
        
        # ログ保存
        self._save_session_log(session_result)
        
        print(f"\n🎉 === 議論完了 ===")
        print(f"📁 詳細結果は {self.session_id} で保存されました")
        
        return session_result
    
    def _generate_specialized_agents(self, topic: str, num_agents: int) -> List[AgentProfile]:
        """専門エージェントを生成"""
        agents = self.agent_factory.analyze_topic_and_generate_agents(topic, num_agents)
        
        print(f"✨ {len(agents)}人の専門エージェントを生成:")
        for i, agent in enumerate(agents, 1):
            print(f"  {i}. {agent.name} ({agent.expertise_area.value})")
            print(f"     特性: {agent.personality}")
        
        return agents
    
    def _gather_background_information(self, topic: str) -> Dict[str, Any]:
        """背景情報を収集"""
        print("🔍 Web検索による情報収集...")
        search_results = self.web_searcher.search_for_topic(topic, "web", 3)
        search_summary = self.web_searcher.get_search_summary(search_results)
        
        print("📈 トレンド分析...")
        trend_analysis = self.trend_analyzer.analyze_trend(topic)
        
        background = {
            "search_results": [
                {
                    "title": r.title,
                    "source": r.source,
                    "snippet": r.snippet,
                    "relevance_score": r.relevance_score
                } for r in search_results
            ],
            "search_summary": search_summary,
            "trend_analysis": trend_analysis
        }
        
        print(f"✅ 背景情報収集完了:")
        print(f"  📄 関連記事: {len(search_results)}件")
        print(f"  📊 トレンドスコア: {trend_analysis['trend_score']}")
        print(f"  💭 感情分析: {trend_analysis['sentiment']['overall']}")
        
        return background
    
    def _execute_discussion_round(self, agents: List[AgentProfile], topic: str, 
                                round_num: int, background_info: Dict[str, Any], 
                                previous_rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """1ラウンドの議論を実行"""
        
        # コンテキスト準備
        context = self._prepare_discussion_context(topic, round_num, background_info, previous_rounds)
        
        # 各エージェントの発言生成
        agent_responses = []
        opinions = []
        
        for i, agent in enumerate(agents, 1):
            print(f"\n👤 [{agent.name}] の発言:")
            
            # エージェント固有のコンテキスト
            agent_context = context + f"\n\n{agent.system_message}"
            
            # 発言生成
            response = self._generate_agent_response(agent, agent_context)
            print(response)
            
            # 意見分析
            opinion = self._extract_opinion_from_response(agent.name, response)
            opinions.append(opinion)
            
            agent_responses.append({
                "agent_name": agent.name,
                "expertise_area": agent.expertise_area.value,
                "response": response,
                "opinion": {
                    "type": opinion.opinion_type.value,
                    "confidence": opinion.confidence,
                    "evidence": opinion.evidence
                }
            })
            
            print("-" * 50)
        
        return {
            "round_number": round_num,
            "agent_responses": agent_responses,
            "opinions": opinions,  # Opinionオブジェクトのまま返す
            "timestamp": datetime.now().isoformat()
        }
    
    def _prepare_discussion_context(self, topic: str, round_num: int, 
                                  background_info: Dict[str, Any], 
                                  previous_rounds: List[Dict[str, Any]]) -> str:
        """議論コンテキストを準備"""
        
        context = f"議論トピック: {topic}\n\n"
        
        # 背景情報
        if background_info.get("search_summary"):
            context += f"背景情報:\n"
            context += f"- 関連情報: {background_info['search_summary']['total_results']}件\n"
            context += f"- トレンド: {background_info['trend_analysis']['sentiment']['overall']}\n\n"
        
        # 前ラウンドの要約
        if previous_rounds:
            context += f"これまでの議論（ラウンド{len(previous_rounds)}まで）:\n"
            for prev_round in previous_rounds[-2:]:  # 最新2ラウンドのみ
                round_num = prev_round["round_number"]
                context += f"\nラウンド{round_num}の要点:\n"
                for response in prev_round["agent_responses"]:
                    agent_name = response["agent_name"]
                    opinion_type = response["opinion"]["type"]
                    context += f"- {agent_name}: {opinion_type}\n"
        
        context += f"\nラウンド{round_num}の目標: "
        if round_num == 1:
            context += "初期意見の表明と論点の整理"
        elif round_num == 2:
            context += "異なる視点の提示と議論の深化"
        else:
            context += "合意形成または最終的な立場の明確化"
        
        return context
    
    def _generate_agent_response(self, agent: AgentProfile, context: str) -> str:
        """エージェントの応答を生成"""
        try:
            messages = [
                {"role": "system", "content": agent.system_message},
                {"role": "user", "content": context}
            ]
            
            response = self.openai_client.chat.completions.create(
                model=os.environ.get("MODEL_NAME", "gpt-3.5-turbo"),
                messages=messages,
                temperature=0.7,
                max_tokens=400
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"[{agent.name}] エラーが発生しました: {e}"
    
    def _extract_opinion_from_response(self, agent_name: str, response: str) -> Opinion:
        """応答から意見を抽出"""
        
        # 簡易的な意見分析（実際はもっと高度なNLP処理が必要）
        response_lower = response.lower()
        
        # 意見タイプの判定
        if any(word in response_lower for word in ["強く賛成", "完全に同意", "絶対に"]):
            opinion_type = OpinionType.STRONGLY_AGREE
        elif any(word in response_lower for word in ["賛成", "同意", "良い", "正しい"]):
            opinion_type = OpinionType.AGREE
        elif any(word in response_lower for word in ["反対", "異議", "問題", "懸念"]):
            opinion_type = OpinionType.DISAGREE
        elif any(word in response_lower for word in ["強く反対", "完全に反対", "絶対に反対"]):
            opinion_type = OpinionType.STRONGLY_DISAGREE
        else:
            opinion_type = OpinionType.NEUTRAL
        
        # 信頼度の計算（簡易実装）
        confidence_indicators = ["確信", "明確", "間違いなく", "確実", "データ"]
        confidence = min(0.5 + 0.1 * sum(1 for word in confidence_indicators if word in response_lower), 1.0)
        
        # エビデンスの抽出
        evidence = []
        if "研究" in response_lower or "データ" in response_lower:
            evidence.append("研究・データ")
        if "経験" in response_lower or "実例" in response_lower:
            evidence.append("経験・実例")
        if "理論" in response_lower:
            evidence.append("理論")
        
        return Opinion(
            agent_name=agent_name,
            content=response,
            opinion_type=opinion_type,
            confidence=confidence,
            evidence=evidence,
            related_topics=[],
            timestamp=datetime.now().isoformat()
        )
    
    def _analyze_collaboration(self, opinions: List[Opinion]) -> Dict[str, Any]:
        """協調分析を実行"""
        return self.collaboration_orchestrator.process_agent_interactions(opinions, "current_topic")
    
    def _display_collaboration_summary(self, collaboration_analysis: Dict[str, Any]):
        """協調分析結果の表示"""
        conflict_level = collaboration_analysis["conflict_level"]
        consensus = collaboration_analysis["consensus"]
        
        print(f"  🎯 対立レベル: {conflict_level}")
        print(f"  🤝 合意度: {consensus.consensus_level:.2f}")
        print(f"  ✅ 合意点: {len(consensus.agreed_points)}個")
        print(f"  ❗ 不一致点: {len(consensus.disagreed_points)}個")
        
        if collaboration_analysis.get("voting_result"):
            voting = collaboration_analysis["voting_result"]
            print(f"  🗳️ 投票結果: {voting['winner']} (マージン: {voting['margin']:.2f})")
        
        # 次のアクション
        next_actions = collaboration_analysis.get("next_actions", [])
        if next_actions:
            print(f"  📋 推奨アクション:")
            for action in next_actions[:2]:
                print(f"    • {action}")
    
    def _should_end_discussion(self, collaboration_analysis: Dict[str, Any]) -> bool:
        """議論終了条件をチェック"""
        consensus = collaboration_analysis["consensus"]
        conflict_level = collaboration_analysis["conflict_level"]
        
        # 高い合意が得られた場合
        if consensus.consensus_level >= 0.8:
            return True
        
        # 調和状態の場合
        if conflict_level == "harmony":
            return True
        
        return False
    
    def _generate_final_conclusion(self, discussion_results: List[Dict[str, Any]], topic: str) -> Dict[str, Any]:
        """最終結論を生成"""
        
        all_opinions = []
        for round_result in discussion_results:
            # 辞書形式のopinionをOpinionオブジェクトに変換
            for opinion_dict in round_result["opinions"]:
                opinion = Opinion(
                    agent_name=opinion_dict["agent_name"],
                    content=opinion_dict["content"],
                    opinion_type=OpinionType(opinion_dict["opinion_type"]),
                    confidence=opinion_dict["confidence"],
                    evidence=opinion_dict["evidence"],
                    related_topics=opinion_dict["related_topics"],
                    timestamp=opinion_dict["timestamp"]
                )
                all_opinions.append(opinion)
        
        # 最終的な協調分析
        final_collaboration = self.collaboration_orchestrator.process_agent_interactions(all_opinions, topic)
        
        # 主要な論点を抽出
        key_points = []
        consensus_points = final_collaboration["consensus"].agreed_points
        disagreement_points = final_collaboration["consensus"].disagreed_points
        
        # 結論テキストを生成
        conclusion_text = f"「{topic}」についての{len(discussion_results)}ラウンドの議論を通じて、"
        
        if final_collaboration["consensus"].consensus_level >= 0.7:
            conclusion_text += "参加者間で高い合意が形成されました。"
        elif final_collaboration["consensus"].consensus_level >= 0.5:
            conclusion_text += "部分的な合意が得られました。"
        else:
            conclusion_text += "多様な意見が表明され、さらなる議論が必要です。"
        
        return {
            "conclusion_text": conclusion_text,
            "consensus_level": final_collaboration["consensus"].consensus_level,
            "agreed_points": consensus_points,
            "disagreed_points": disagreement_points,
            "conflict_level": final_collaboration["conflict_level"],
            "resolution_strategy": final_collaboration["resolution_strategy"],
            "recommendation": self._generate_recommendation(final_collaboration)
        }
    
    def _generate_recommendation(self, collaboration_analysis: Dict[str, Any]) -> str:
        """推奨事項を生成"""
        consensus_level = collaboration_analysis["consensus"].consensus_level
        conflict_level = collaboration_analysis["conflict_level"]
        
        if consensus_level >= 0.8:
            return "合意に基づく実行計画の策定を推奨します。"
        elif conflict_level == "strong_conflict":
            return "外部専門家の意見や追加調査を実施することを推奨します。"
        elif conflict_level == "moderate_conflict":
            return "論点を絞り込んでの継続議論を推奨します。"
        else:
            return "現在の方向性での段階的進行を推奨します。"
    
    def _calculate_overall_metrics(self, discussion_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """全体メトリクスを計算"""
        all_opinions = []
        for round_result in discussion_results:
            # 辞書形式のopinionをOpinionオブジェクトに変換
            for opinion_dict in round_result["opinions"]:
                opinion = Opinion(
                    agent_name=opinion_dict["agent_name"],
                    content=opinion_dict["content"],
                    opinion_type=OpinionType(opinion_dict["opinion_type"]),
                    confidence=opinion_dict["confidence"],
                    evidence=opinion_dict["evidence"],
                    related_topics=opinion_dict["related_topics"],
                    timestamp=opinion_dict["timestamp"]
                )
                all_opinions.append(opinion)
        
        # 参加度分析
        agent_participation = {}
        for opinion in all_opinions:
            agent_name = opinion.agent_name
            agent_participation[agent_name] = agent_participation.get(agent_name, 0) + 1
        
        # 意見の多様性
        opinion_types = [opinion.opinion_type.value for opinion in all_opinions]
        opinion_diversity = len(set(opinion_types)) / len(OpinionType)
        
        # 平均信頼度
        avg_confidence = sum(opinion.confidence for opinion in all_opinions) / len(all_opinions)
        
        return {
            "total_rounds": len(discussion_results),
            "total_opinions": len(all_opinions),
            "agent_participation": agent_participation,
            "opinion_diversity": round(opinion_diversity, 2),
            "average_confidence": round(avg_confidence, 2),
            "evidence_usage_rate": len([op for op in all_opinions if op.evidence]) / len(all_opinions)
        }
    
    def _agent_profile_to_dict(self, agent: AgentProfile) -> Dict[str, Any]:
        """エージェントプロファイルを辞書に変換"""
        return {
            "name": agent.name,
            "role": agent.role,
            "expertise_area": agent.expertise_area.value,
            "personality": agent.personality,
            "debate_style": agent.debate_style,
            "knowledge_focus": agent.knowledge_focus,
            "interaction_patterns": agent.interaction_patterns
        }
    
    def _opinion_to_dict(self, opinion: Opinion) -> Dict[str, Any]:
        """Opinionオブジェクトを辞書に変換"""
        return {
            "agent_name": opinion.agent_name,
            "content": opinion.content,
            "opinion_type": opinion.opinion_type.value,
            "confidence": opinion.confidence,
            "evidence": opinion.evidence,
            "related_topics": opinion.related_topics,
            "timestamp": opinion.timestamp
        }
    
    def _save_session_log(self, session_result: Dict[str, Any]):
        """セッションログを保存"""
        log_dir = "intelligent_collaboration_logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"intelligent_session_{self.session_id}.json")
        
        # Opinionオブジェクトを辞書に変換するための前処理
        serializable_result = self._make_json_serializable(session_result)
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(serializable_result, f, ensure_ascii=False, indent=2)
        
        print(f"📁 詳細ログ保存: {log_file}")
    
    def _make_json_serializable(self, obj):
        """オブジェクトをJSONシリアライズ可能な形式に変換"""
        if hasattr(obj, '__dict__'):
            # データクラスやオブジェクトを辞書に変換
            result = {}
            for key, value in obj.__dict__.items():
                if hasattr(value, 'value'):  # Enumの場合
                    result[key] = value.value
                else:
                    result[key] = self._make_json_serializable(value)
            return result
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        else:
            return obj


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
        print("❌ エラー: OPENAI_API_KEY が設定されていません。")
        print("📝 .envファイルでAPIキーを設定してください。")
        return
    
    # 引数処理
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("🤔 議論したいトピックを入力してください: ")
    
    # システム実行
    system = IntelligentCollaborationSystem()
    
    try:
        result = system.run_intelligent_discussion(topic)
        
        # 簡易サマリー表示
        print(f"\n📊 === 最終サマリー ===")
        print(f"🎯 合意度: {result['final_conclusion']['consensus_level']:.2f}")
        print(f"🤝 対立レベル: {result['final_conclusion']['conflict_level']}")
        print(f"💡 推奨: {result['final_conclusion']['recommendation']}")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")


if __name__ == "__main__":
    main()