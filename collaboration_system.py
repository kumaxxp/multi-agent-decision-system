"""
エージェント間競合・協調システム
意見の対立、合意形成、投票システムを管理
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from collections import defaultdict, Counter


class OpinionType(Enum):
    """意見のタイプ"""
    STRONGLY_AGREE = "strongly_agree"
    AGREE = "agree"
    NEUTRAL = "neutral"
    DISAGREE = "disagree"
    STRONGLY_DISAGREE = "strongly_disagree"


class ConflictLevel(Enum):
    """対立レベル"""
    HARMONY = "harmony"          # 調和
    MILD_DISAGREEMENT = "mild"   # 軽微な不一致
    MODERATE_CONFLICT = "moderate"  # 中程度の対立
    STRONG_CONFLICT = "strong"   # 強い対立
    DEADLOCK = "deadlock"        # 膠着状態


@dataclass
class Opinion:
    """意見データ構造"""
    agent_name: str
    content: str
    opinion_type: OpinionType
    confidence: float  # 0.0-1.0
    evidence: List[str]
    related_topics: List[str]
    timestamp: str


@dataclass
class Consensus:
    """合意データ構造"""
    topic: str
    agreed_points: List[str]
    disagreed_points: List[str]
    consensus_level: float  # 0.0-1.0
    participating_agents: List[str]
    resolution_method: str


class OpinionConflictResolver:
    """意見対立解決システム"""
    
    def __init__(self):
        self.conflict_history = []
        self.resolution_strategies = {
            ConflictLevel.MILD_DISAGREEMENT: self._mild_disagreement_strategy,
            ConflictLevel.MODERATE_CONFLICT: self._moderate_conflict_strategy,
            ConflictLevel.STRONG_CONFLICT: self._strong_conflict_strategy,
            ConflictLevel.DEADLOCK: self._deadlock_strategy
        }
    
    def analyze_conflict_level(self, opinions: List[Opinion]) -> ConflictLevel:
        """意見から対立レベルを分析"""
        if len(opinions) < 2:
            return ConflictLevel.HARMONY
        
        opinion_types = [op.opinion_type for op in opinions]
        type_counts = Counter(opinion_types)
        
        # 強い対立意見の数をカウント
        strong_negative = type_counts.get(OpinionType.STRONGLY_DISAGREE, 0)
        negative = type_counts.get(OpinionType.DISAGREE, 0)
        positive = type_counts.get(OpinionType.AGREE, 0)
        strong_positive = type_counts.get(OpinionType.STRONGLY_AGREE, 0)
        
        total_strong_opinions = strong_negative + strong_positive
        total_conflicting = strong_negative + negative + positive + strong_positive
        
        if total_strong_opinions >= len(opinions) * 0.5 and strong_negative > 0 and strong_positive > 0:
            return ConflictLevel.STRONG_CONFLICT
        elif total_conflicting >= len(opinions) * 0.6:
            return ConflictLevel.MODERATE_CONFLICT
        elif negative > 0 or strong_negative > 0:
            return ConflictLevel.MILD_DISAGREEMENT
        else:
            return ConflictLevel.HARMONY
    
    def resolve_conflict(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """対立を解決する"""
        conflict_level = self.analyze_conflict_level(opinions)
        
        if conflict_level in self.resolution_strategies:
            resolution = self.resolution_strategies[conflict_level](opinions, topic)
        else:
            resolution = self._default_resolution(opinions, topic)
        
        self.conflict_history.append({
            "topic": topic,
            "conflict_level": conflict_level.value,
            "resolution": resolution,
            "num_opinions": len(opinions)
        })
        
        return resolution
    
    def _mild_disagreement_strategy(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """軽微な不一致の解決戦略"""
        return {
            "strategy": "clarification_and_evidence",
            "action": "各エージェントに具体的な根拠の提示を求める",
            "next_steps": [
                "反対意見のエージェントに詳細な説明を求める",
                "共通点を見つけて議論の焦点を絞る",
                "追加の情報収集を提案する"
            ],
            "resolution_probability": 0.8
        }
    
    def _moderate_conflict_strategy(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """中程度の対立の解決戦略"""
        return {
            "strategy": "structured_debate",
            "action": "構造化された議論を実施する",
            "next_steps": [
                "各立場の代表者を選出する",
                "論点を明確に整理する",
                "段階的な合意形成を行う",
                "第三者の意見を求める"
            ],
            "resolution_probability": 0.6
        }
    
    def _strong_conflict_strategy(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """強い対立の解決戦略"""
        return {
            "strategy": "mediation_and_compromise",
            "action": "仲裁と妥協案の模索",
            "next_steps": [
                "中立的な仲裁者を設置する",
                "各立場の核心的価値を特定する",
                "妥協可能な点を見つける",
                "段階的実施案を検討する"
            ],
            "resolution_probability": 0.4
        }
    
    def _deadlock_strategy(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """膠着状態の解決戦略"""
        return {
            "strategy": "alternative_approach",
            "action": "根本的にアプローチを変更する",
            "next_steps": [
                "問題の再定義を行う",
                "新しい視点や専門家を投入する",
                "部分的な解決策を模索する",
                "将来的な再検討を計画する"
            ],
            "resolution_probability": 0.2
        }
    
    def _default_resolution(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """デフォルト解決策"""
        return {
            "strategy": "consensus_building",
            "action": "合意形成を促進する",
            "next_steps": [
                "共通の理解を確認する",
                "次のステップを計画する"
            ],
            "resolution_probability": 0.9
        }


class ConsensusBuilder:
    """合意形成システム"""
    
    def __init__(self):
        self.consensus_history = []
        
    def build_consensus(self, opinions: List[Opinion], topic: str) -> Consensus:
        """意見から合意を構築"""
        
        # 合意点と不一致点を抽出
        agreed_points = self._extract_agreed_points(opinions)
        disagreed_points = self._extract_disagreed_points(opinions)
        
        # 合意レベルを計算
        consensus_level = self._calculate_consensus_level(opinions)
        
        consensus = Consensus(
            topic=topic,
            agreed_points=agreed_points,
            disagreed_points=disagreed_points,
            consensus_level=consensus_level,
            participating_agents=[op.agent_name for op in opinions],
            resolution_method=self._determine_resolution_method(consensus_level)
        )
        
        self.consensus_history.append(consensus)
        return consensus
    
    def _extract_agreed_points(self, opinions: List[Opinion]) -> List[str]:
        """合意点を抽出"""
        # 簡易実装：肯定的意見の共通点を探す
        agreed_points = []
        positive_opinions = [
            op for op in opinions 
            if op.opinion_type in [OpinionType.AGREE, OpinionType.STRONGLY_AGREE]
        ]
        
        if len(positive_opinions) >= len(opinions) * 0.6:
            # 過半数が同意している点を抽出
            common_themes = self._extract_common_themes([op.content for op in positive_opinions])
            agreed_points.extend(common_themes)
        
        return agreed_points[:5]  # 最大5つまで
    
    def _extract_disagreed_points(self, opinions: List[Opinion]) -> List[str]:
        """不一致点を抽出"""
        disagreed_points = []
        negative_opinions = [
            op for op in opinions 
            if op.opinion_type in [OpinionType.DISAGREE, OpinionType.STRONGLY_DISAGREE]
        ]
        
        if negative_opinions:
            contentious_themes = self._extract_common_themes([op.content for op in negative_opinions])
            disagreed_points.extend(contentious_themes)
        
        return disagreed_points[:5]  # 最大5つまで
    
    def _extract_common_themes(self, contents: List[str]) -> List[str]:
        """共通テーマを抽出（簡易実装）"""
        # キーワードベースの簡易実装
        common_words = []
        word_counts = defaultdict(int)
        
        for content in contents:
            words = content.split()
            for word in words:
                if len(word) > 3:  # 短い単語を除外
                    word_counts[word] += 1
        
        # 複数のコンテンツに出現する単語を抽出
        for word, count in word_counts.items():
            if count >= 2:
                common_words.append(word)
        
        return common_words[:3]  # 最大3つまで
    
    def _calculate_consensus_level(self, opinions: List[Opinion]) -> float:
        """合意レベルを計算"""
        if not opinions:
            return 0.0
        
        positive_count = sum(1 for op in opinions if op.opinion_type in [OpinionType.AGREE, OpinionType.STRONGLY_AGREE])
        neutral_count = sum(1 for op in opinions if op.opinion_type == OpinionType.NEUTRAL)
        negative_count = len(opinions) - positive_count - neutral_count
        
        # 加重平均で計算
        consensus_score = (positive_count * 1.0 + neutral_count * 0.5 + negative_count * 0.0) / len(opinions)
        
        return round(consensus_score, 2)
    
    def _determine_resolution_method(self, consensus_level: float) -> str:
        """解決方法を決定"""
        if consensus_level >= 0.8:
            return "strong_consensus"
        elif consensus_level >= 0.6:
            return "majority_agreement"
        elif consensus_level >= 0.4:
            return "compromise_needed"
        else:
            return "fundamental_disagreement"


class VotingSystem:
    """投票システム"""
    
    def __init__(self):
        self.voting_history = []
    
    def conduct_vote(self, agents: List[str], question: str, options: List[str]) -> Dict[str, Any]:
        """投票を実施（シミュレーション）"""
        
        # 簡易投票シミュレーション
        import random
        votes = {}
        
        for agent in agents:
            # エージェントの特性に基づいた投票傾向をシミュレート
            vote = random.choice(options)
            votes[agent] = vote
        
        # 結果集計
        vote_counts = Counter(votes.values())
        total_votes = len(votes)
        
        results = {
            "question": question,
            "options": options,
            "votes": votes,
            "results": dict(vote_counts),
            "winner": vote_counts.most_common(1)[0][0] if vote_counts else None,
            "participation_rate": total_votes / len(agents) if agents else 0,
            "margin": self._calculate_margin(vote_counts, total_votes)
        }
        
        self.voting_history.append(results)
        return results
    
    def _calculate_margin(self, vote_counts: Counter, total_votes: int) -> float:
        """勝利マージンを計算"""
        if not vote_counts or len(vote_counts) < 2:
            return 1.0
        
        sorted_counts = vote_counts.most_common()
        if len(sorted_counts) >= 2:
            winner_count = sorted_counts[0][1]
            runner_up_count = sorted_counts[1][1]
            margin = (winner_count - runner_up_count) / total_votes
        else:
            margin = sorted_counts[0][1] / total_votes
        
        return round(margin, 2)
    
    def analyze_voting_patterns(self) -> Dict[str, Any]:
        """投票パターンを分析"""
        if not self.voting_history:
            return {"message": "投票履歴がありません"}
        
        total_votes = len(self.voting_history)
        close_votes = sum(1 for vote in self.voting_history if vote["margin"] < 0.2)
        unanimous_votes = sum(1 for vote in self.voting_history if vote["margin"] == 1.0)
        
        return {
            "total_votes_conducted": total_votes,
            "close_votes": close_votes,
            "close_vote_rate": close_votes / total_votes,
            "unanimous_votes": unanimous_votes,
            "unanimous_rate": unanimous_votes / total_votes,
            "average_participation": sum(vote["participation_rate"] for vote in self.voting_history) / total_votes
        }


class CollaborationOrchestrator:
    """協調システム統合オーケストレーター"""
    
    def __init__(self):
        self.conflict_resolver = OpinionConflictResolver()
        self.consensus_builder = ConsensusBuilder()
        self.voting_system = VotingSystem()
        
    def process_agent_interactions(self, opinions: List[Opinion], topic: str) -> Dict[str, Any]:
        """エージェント間の相互作用を処理"""
        
        # 1. 対立レベルを分析
        conflict_level = self.conflict_resolver.analyze_conflict_level(opinions)
        
        # 2. 対立解決策を提案
        resolution = self.conflict_resolver.resolve_conflict(opinions, topic)
        
        # 3. 合意形成を試行
        consensus = self.consensus_builder.build_consensus(opinions, topic)
        
        # 4. 必要に応じて投票を実施
        voting_result = None
        if conflict_level in [ConflictLevel.MODERATE_CONFLICT, ConflictLevel.STRONG_CONFLICT]:
            agent_names = [op.agent_name for op in opinions]
            voting_options = ["提案A", "提案B", "再議論"]
            voting_result = self.voting_system.conduct_vote(agent_names, topic, voting_options)
        
        return {
            "topic": topic,
            "conflict_level": conflict_level.value,
            "resolution_strategy": resolution,
            "consensus": consensus,
            "voting_result": voting_result,
            "next_actions": self._determine_next_actions(conflict_level, consensus, voting_result)
        }
    
    def _determine_next_actions(self, conflict_level: ConflictLevel, consensus: Consensus, voting_result: Optional[Dict]) -> List[str]:
        """次のアクションを決定"""
        actions = []
        
        if consensus.consensus_level >= 0.8:
            actions.append("合意に基づく結論の確定")
        elif conflict_level == ConflictLevel.STRONG_CONFLICT:
            actions.append("専門家の追加投入")
            actions.append("問題の分割検討")
        elif voting_result and voting_result["margin"] < 0.3:
            actions.append("再議論の実施")
        else:
            actions.append("部分的合意の確認")
            actions.append("次ラウンドでの継続議論")
        
        return actions