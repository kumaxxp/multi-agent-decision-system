"""
議論結果分析・表示ツール
JSONログを分析して見やすい形式で表示
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse
from pathlib import Path


class ResultAnalyzer:
    """結果分析クラス"""
    
    def __init__(self):
        self.log_dir = "intelligent_collaboration_logs"
        
    def list_available_sessions(self) -> List[Dict[str, str]]:
        """利用可能なセッション一覧を取得"""
        if not os.path.exists(self.log_dir):
            return []
        
        sessions = []
        for file_name in os.listdir(self.log_dir):
            if file_name.endswith('.json') and file_name.startswith('intelligent_session_'):
                session_id = file_name.replace('intelligent_session_', '').replace('.json', '')
                file_path = os.path.join(self.log_dir, file_name)
                
                # ファイル情報を取得
                stat = os.stat(file_path)
                created_time = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M')
                file_size = f"{stat.st_size / 1024:.1f} KB"
                
                sessions.append({
                    "session_id": session_id,
                    "file_name": file_name,
                    "created_time": created_time,
                    "file_size": file_size
                })
        
        return sorted(sessions, key=lambda x: x['session_id'], reverse=True)
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """セッション結果を読み込み"""
        file_path = os.path.join(self.log_dir, f"intelligent_session_{session_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ セッション読み込みエラー: {e}")
            return None
    
    def analyze_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """セッション結果を分析"""
        
        session_info = session_data["session_info"]
        agents = session_data["agents"]
        discussion_rounds = session_data["discussion_rounds"]
        final_conclusion = session_data["final_conclusion"]
        metrics = session_data["overall_collaboration_metrics"]
        
        # 基本統計
        basic_stats = {
            "topic": session_info["topic"],
            "duration_rounds": session_info["actual_rounds"],
            "total_agents": len(agents),
            "total_opinions": metrics["total_opinions"],
            "consensus_achieved": final_conclusion["consensus_level"] >= 0.7
        }
        
        # エージェント分析
        agent_analysis = self._analyze_agents(agents, discussion_rounds)
        
        # ラウンド別分析
        round_analysis = self._analyze_rounds(discussion_rounds)
        
        # 協調パターン分析
        collaboration_patterns = self._analyze_collaboration_patterns(discussion_rounds)
        
        # 意見進化分析
        opinion_evolution = self._analyze_opinion_evolution(discussion_rounds)
        
        return {
            "basic_stats": basic_stats,
            "agent_analysis": agent_analysis,
            "round_analysis": round_analysis,
            "collaboration_patterns": collaboration_patterns,
            "opinion_evolution": opinion_evolution,
            "final_conclusion": final_conclusion,
            "metrics": metrics
        }
    
    def _analyze_agents(self, agents: List[Dict[str, Any]], discussion_rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """エージェント分析"""
        
        agent_stats = {}
        
        for agent in agents:
            name = agent["name"]
            expertise = agent["expertise_area"]
            
            # 各ラウンドでの発言を分析
            responses = []
            opinion_types = []
            confidences = []
            
            for round_data in discussion_rounds:
                for response in round_data["agent_responses"]:
                    if response["agent_name"] == name:
                        responses.append(response)
                        opinion_types.append(response["opinion"]["type"])
                        confidences.append(response["opinion"]["confidence"])
            
            # 統計計算
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            most_common_opinion = max(set(opinion_types), key=opinion_types.count) if opinion_types else "neutral"
            
            agent_stats[name] = {
                "expertise_area": expertise,
                "personality": agent["personality"],
                "total_responses": len(responses),
                "average_confidence": round(avg_confidence, 2),
                "dominant_opinion_type": most_common_opinion,
                "opinion_consistency": self._calculate_opinion_consistency(opinion_types),
                "influence_score": self._calculate_influence_score(responses)
            }
        
        return agent_stats
    
    def _analyze_rounds(self, discussion_rounds: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ラウンド別分析"""
        
        round_analysis = []
        
        for round_data in discussion_rounds:
            round_num = round_data["round_number"]
            responses = round_data["agent_responses"]
            
            # 意見分布
            opinion_distribution = {}
            confidence_scores = []
            evidence_usage = 0
            
            for response in responses:
                opinion_type = response["opinion"]["type"]
                confidence = response["opinion"]["confidence"]
                evidence = response["opinion"]["evidence"]
                
                opinion_distribution[opinion_type] = opinion_distribution.get(opinion_type, 0) + 1
                confidence_scores.append(confidence)
                
                if evidence:
                    evidence_usage += 1
            
            # 協調分析があればそれも含める
            collaboration_info = {}
            if "collaboration_analysis" in round_data:
                collab = round_data["collaboration_analysis"]
                collaboration_info = {
                    "conflict_level": collab["conflict_level"],
                    "consensus_level": collab["consensus"]["consensus_level"],
                    "agreed_points": len(collab["consensus"]["agreed_points"]),
                    "disagreed_points": len(collab["consensus"]["disagreed_points"])
                }
            
            round_analysis.append({
                "round_number": round_num,
                "opinion_distribution": opinion_distribution,
                "average_confidence": round(sum(confidence_scores) / len(confidence_scores), 2) if confidence_scores else 0,
                "evidence_usage_rate": round(evidence_usage / len(responses), 2) if responses else 0,
                "collaboration_metrics": collaboration_info,
                "key_themes": self._extract_key_themes(responses)
            })
        
        return round_analysis
    
    def _analyze_collaboration_patterns(self, discussion_rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """協調パターン分析"""
        
        conflict_levels = []
        consensus_levels = []
        
        for round_data in discussion_rounds:
            if "collaboration_analysis" in round_data:
                collab = round_data["collaboration_analysis"]
                conflict_levels.append(collab["conflict_level"])
                consensus_levels.append(collab["consensus"]["consensus_level"])
        
        # パターンの識別
        if len(consensus_levels) >= 2:
            consensus_trend = "increasing" if consensus_levels[-1] > consensus_levels[0] else ("decreasing" if consensus_levels[-1] < consensus_levels[0] else "stable")
        else:
            consensus_trend = "insufficient_data"
        
        return {
            "conflict_progression": conflict_levels,
            "consensus_progression": consensus_levels,
            "consensus_trend": consensus_trend,
            "peak_conflict": max(conflict_levels) if conflict_levels else "none",
            "final_consensus": consensus_levels[-1] if consensus_levels else 0,
            "collaboration_effectiveness": self._assess_collaboration_effectiveness(conflict_levels, consensus_levels)
        }
    
    def _analyze_opinion_evolution(self, discussion_rounds: List[Dict[str, Any]]) -> Dict[str, Any]:
        """意見進化分析"""
        
        agent_opinion_evolution = {}
        
        for round_data in discussion_rounds:
            round_num = round_data["round_number"]
            
            for response in round_data["agent_responses"]:
                agent_name = response["agent_name"]
                opinion_type = response["opinion"]["type"]
                confidence = response["opinion"]["confidence"]
                
                if agent_name not in agent_opinion_evolution:
                    agent_opinion_evolution[agent_name] = []
                
                agent_opinion_evolution[agent_name].append({
                    "round": round_num,
                    "opinion": opinion_type,
                    "confidence": confidence
                })
        
        # 進化パターンの分析
        evolution_patterns = {}
        for agent_name, evolution in agent_opinion_evolution.items():
            if len(evolution) >= 2:
                initial_opinion = evolution[0]["opinion"]
                final_opinion = evolution[-1]["opinion"]
                
                if initial_opinion == final_opinion:
                    pattern = "consistent"
                elif self._opinion_distance(initial_opinion, final_opinion) <= 1:
                    pattern = "slight_shift"
                else:
                    pattern = "major_shift"
                
                evolution_patterns[agent_name] = {
                    "pattern": pattern,
                    "initial_opinion": initial_opinion,
                    "final_opinion": final_opinion,
                    "confidence_change": evolution[-1]["confidence"] - evolution[0]["confidence"]
                }
        
        return {
            "agent_evolutions": agent_opinion_evolution,
            "evolution_patterns": evolution_patterns,
            "stability_score": self._calculate_stability_score(evolution_patterns)
        }
    
    def _calculate_opinion_consistency(self, opinion_types: List[str]) -> float:
        """意見一貫性を計算"""
        if not opinion_types:
            return 0.0
        
        most_common = max(set(opinion_types), key=opinion_types.count)
        consistency = opinion_types.count(most_common) / len(opinion_types)
        return round(consistency, 2)
    
    def _calculate_influence_score(self, responses: List[Dict[str, Any]]) -> float:
        """影響力スコアを計算（簡易版）"""
        # 発言数、信頼度、証拠使用頻度を基に計算
        if not responses:
            return 0.0
        
        total_confidence = sum(r["opinion"]["confidence"] for r in responses)
        evidence_count = sum(1 for r in responses if r["opinion"]["evidence"])
        
        influence = (total_confidence + evidence_count) / len(responses)
        return round(min(influence, 1.0), 2)
    
    def _extract_key_themes(self, responses: List[Dict[str, Any]]) -> List[str]:
        """主要テーマを抽出（簡易版）"""
        # キーワード頻度分析（実際はより高度なNLP処理が必要）
        all_text = " ".join([r["response"] for r in responses])
        
        # よく出現する単語を抽出（簡易実装）
        words = all_text.split()
        word_counts = {}
        
        for word in words:
            if len(word) > 3:  # 短い単語を除外
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # 頻出単語上位3つを返す
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:3] if count >= 2]
    
    def _assess_collaboration_effectiveness(self, conflict_levels: List[str], consensus_levels: List[float]) -> str:
        """協調効果を評価"""
        if not conflict_levels or not consensus_levels:
            return "insufficient_data"
        
        final_consensus = consensus_levels[-1]
        
        if final_consensus >= 0.8:
            return "highly_effective"
        elif final_consensus >= 0.6:
            return "moderately_effective"
        elif final_consensus >= 0.4:
            return "partially_effective"
        else:
            return "low_effectiveness"
    
    def _opinion_distance(self, opinion1: str, opinion2: str) -> int:
        """意見間の距離を計算"""
        opinion_scale = {
            "strongly_disagree": 0,
            "disagree": 1,
            "neutral": 2,
            "agree": 3,
            "strongly_agree": 4
        }
        
        return abs(opinion_scale.get(opinion1, 2) - opinion_scale.get(opinion2, 2))
    
    def _calculate_stability_score(self, evolution_patterns: Dict[str, Dict[str, Any]]) -> float:
        """安定性スコアを計算"""
        if not evolution_patterns:
            return 0.0
        
        consistent_agents = sum(1 for pattern in evolution_patterns.values() if pattern["pattern"] == "consistent")
        stability = consistent_agents / len(evolution_patterns)
        return round(stability, 2)
    
    def display_analysis(self, analysis: Dict[str, Any]):
        """分析結果をコンソール表示"""
        print("\n🔍 === 議論分析レポート ===\n")
        
        # 基本統計
        stats = analysis["basic_stats"]
        print("📊 基本統計:")
        print(f"  議論トピック: {stats['topic']}")
        print(f"  実施ラウンド: {stats['duration_rounds']}")
        print(f"  参加エージェント: {stats['total_agents']}人")
        print(f"  総発言数: {stats['total_opinions']}")
        print(f"  合意達成: {'✅' if stats['consensus_achieved'] else '❌'}")
        
        # エージェント分析
        print(f"\n👥 エージェント分析:")
        agent_analysis = analysis["agent_analysis"]
        for name, data in agent_analysis.items():
            print(f"  {name} ({data['expertise_area']}):")
            print(f"    平均信頼度: {data['average_confidence']:.2f}")
            print(f"    主要意見: {data['dominant_opinion_type']}")
            print(f"    一貫性: {data['opinion_consistency']:.2f}")
            print(f"    影響力: {data['influence_score']:.2f}")
        
        # ラウンド進展
        print(f"\n🔄 ラウンド別進展:")
        for round_data in analysis["round_analysis"]:
            round_num = round_data["round_number"]
            print(f"  ラウンド{round_num}:")
            print(f"    平均信頼度: {round_data['average_confidence']:.2f}")
            print(f"    証拠使用率: {round_data['evidence_usage_rate']:.2f}")
            
            if round_data["collaboration_metrics"]:
                collab = round_data["collaboration_metrics"]
                print(f"    対立レベル: {collab['conflict_level']}")
                print(f"    合意度: {collab['consensus_level']:.2f}")
        
        # 協調パターン
        print(f"\n🤝 協調パターン:")
        collab_patterns = analysis["collaboration_patterns"]
        print(f"  合意の傾向: {collab_patterns['consensus_trend']}")
        print(f"  最終合意度: {collab_patterns['final_consensus']:.2f}")
        print(f"  協調効果: {collab_patterns['collaboration_effectiveness']}")
        
        # 最終結論
        print(f"\n🎯 最終結論:")
        conclusion = analysis["final_conclusion"]
        print(f"  {conclusion['conclusion_text']}")
        print(f"  推奨事項: {conclusion['recommendation']}")


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="議論結果分析ツール")
    parser.add_argument("--list", action="store_true", help="利用可能なセッション一覧を表示")
    parser.add_argument("--session", type=str, help="分析するセッションID")
    parser.add_argument("--html", action="store_true", help="HTML形式で出力")
    
    args = parser.parse_args()
    
    analyzer = ResultAnalyzer()
    
    if args.list:
        # セッション一覧表示
        sessions = analyzer.list_available_sessions()
        if not sessions:
            print("📂 保存されたセッションがありません。")
            return
        
        print("📋 利用可能なセッション:\n")
        for session in sessions:
            print(f"  {session['session_id']}")
            print(f"    作成日時: {session['created_time']}")
            print(f"    サイズ: {session['file_size']}")
            print()
        
        return
    
    if args.session:
        # 特定セッションの分析
        session_data = analyzer.load_session(args.session)
        if not session_data:
            print(f"❌ セッション {args.session} が見つかりません。")
            return
        
        analysis = analyzer.analyze_session(session_data)
        
        if args.html:
            # HTML出力（後で実装）
            print("📄 HTML出力は準備中です。")
        else:
            # コンソール出力
            analyzer.display_analysis(analysis)
        
        return
    
    # インタラクティブモード
    sessions = analyzer.list_available_sessions()
    if not sessions:
        print("📂 保存されたセッションがありません。")
        print("まず main_intelligent_collaboration.py を実行してセッションを作成してください。")
        return
    
    print("📋 利用可能なセッション:")
    for i, session in enumerate(sessions, 1):
        print(f"  {i}. {session['session_id']} ({session['created_time']})")
    
    try:
        choice = int(input("\n分析したいセッション番号を選択してください: ")) - 1
        if 0 <= choice < len(sessions):
            session_id = sessions[choice]["session_id"]
            session_data = analyzer.load_session(session_id)
            
            if session_data:
                analysis = analyzer.analyze_session(session_data)
                analyzer.display_analysis(analysis)
            else:
                print("❌ セッションの読み込みに失敗しました。")
        else:
            print("❌ 無効な選択です。")
            
    except ValueError:
        print("❌ 無効な入力です。")


if __name__ == "__main__":
    main()