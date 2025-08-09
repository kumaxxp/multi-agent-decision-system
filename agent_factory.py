"""
動的エージェント生成システム
トピックや文脈に応じて専門エージェントを自動生成する
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ExpertiseArea(Enum):
    """専門分野の定義"""
    TECHNOLOGY = "technology"
    BUSINESS = "business"
    ACADEMIC = "academic"
    CREATIVE = "creative"
    LEGAL = "legal"
    MEDICAL = "medical"
    FINANCE = "finance"
    ENVIRONMENT = "environment"
    EDUCATION = "education"
    SOCIAL = "social"


@dataclass
class AgentProfile:
    """エージェントプロファイル"""
    name: str
    role: str
    expertise_area: ExpertiseArea
    personality: str
    system_message: str
    debate_style: str
    knowledge_focus: List[str]
    interaction_patterns: List[str]


class AgentFactory:
    """動的エージェント生成ファクトリー"""
    
    def __init__(self):
        self.agent_templates = self._load_agent_templates()
        self.topic_analyzer = TopicAnalyzer()
        
    def _load_agent_templates(self) -> Dict[ExpertiseArea, Dict[str, Any]]:
        """エージェントテンプレートを定義"""
        return {
            ExpertiseArea.TECHNOLOGY: {
                "profiles": [
                    {
                        "name": "テックエバンジェリスト",
                        "personality": "革新的で楽観的、技術の可能性を追求",
                        "debate_style": "データ駆動、実例重視、未来志向",
                        "knowledge_focus": ["最新技術動向", "プログラミング", "AI/ML", "クラウド"],
                        "system_template": "あなたは最新技術に精通したテックエバンジェリストです。{topic}について、技術的観点から革新的で実践的な意見を述べてください。データや実例を交えて、将来の可能性も含めて議論してください。"
                    },
                    {
                        "name": "システムアーキテクト",
                        "personality": "論理的で慎重、システム全体を俯瞰",
                        "debate_style": "構造的思考、リスク分析、スケーラビリティ重視",
                        "knowledge_focus": ["システム設計", "アーキテクチャ", "セキュリティ", "パフォーマンス"],
                        "system_template": "あなたは経験豊富なシステムアーキテクトです。{topic}について、システム全体の構造や設計の観点から、スケーラビリティやリスクを考慮した専門的な分析を行ってください。"
                    }
                ]
            },
            
            ExpertiseArea.BUSINESS: {
                "profiles": [
                    {
                        "name": "戦略コンサルタント",
                        "personality": "分析的で結果重視、ビジネス価値を追求",
                        "debate_style": "SWOT分析、ROI重視、市場データ活用",
                        "knowledge_focus": ["経営戦略", "市場分析", "競合分析", "収益モデル"],
                        "system_template": "あなたは経営戦略に精通した戦略コンサルタントです。{topic}について、ビジネス価値や市場機会、競合優位性の観点から分析し、実践的な戦略を提案してください。"
                    },
                    {
                        "name": "プロダクトマネージャー",
                        "personality": "ユーザー中心、イノベーション志向",
                        "debate_style": "ユーザー体験重視、データ分析、MVP思考",
                        "knowledge_focus": ["プロダクト戦略", "UX/UI", "市場調査", "データ分析"],
                        "system_template": "あなたは製品開発に精通したプロダクトマネージャーです。{topic}について、ユーザーのニーズや市場の要求を踏まえて、実用的な製品・サービスの観点から議論してください。"
                    }
                ]
            },
            
            ExpertiseArea.ACADEMIC: {
                "profiles": [
                    {
                        "name": "学術研究者",
                        "personality": "厳密で客観的、エビデンス重視",
                        "debate_style": "文献引用、統計分析、仮説検証",
                        "knowledge_focus": ["学術論文", "研究手法", "統計分析", "理論構築"],
                        "system_template": "あなたは学術研究に精通した研究者です。{topic}について、既存の研究や理論を踏まえ、客観的なエビデンスに基づいて厳密な分析を行ってください。"
                    },
                    {
                        "name": "教育専門家",
                        "personality": "育成重視、長期的視点",
                        "debate_style": "教育理論、実践事例、成長プロセス重視",
                        "knowledge_focus": ["教育理論", "学習心理学", "カリキュラム設計", "教育技術"],
                        "system_template": "あなたは教育に精通した専門家です。{topic}について、学習効果や人材育成の観点から、理論と実践を組み合わせた教育的な視点で議論してください。"
                    }
                ]
            },
            
            ExpertiseArea.CREATIVE: {
                "profiles": [
                    {
                        "name": "クリエイティブディレクター",
                        "personality": "創造的で直感的、美的センス重視",
                        "debate_style": "アイデア発想、デザイン思考、感性重視",
                        "knowledge_focus": ["デザイン", "ブランディング", "コミュニケーション", "トレンド"],
                        "system_template": "あなたは創造性に富んだクリエイティブディレクターです。{topic}について、デザインや美的価値、ブランド価値の観点から、創造的で革新的なアイデアを提案してください。"
                    },
                    {
                        "name": "イノベーター",
                        "personality": "挑戦的で破壊的、常識を疑う",
                        "debate_style": "アウトオブボックス、逆説的思考、実験精神",
                        "knowledge_focus": ["イノベーション理論", "創造的思考", "ブルーオーシャン", "ディスラプション"],
                        "system_template": "あなたは革新的思考を得意とするイノベーターです。{topic}について、既存の枠組みを超えた斬新なアプローチや、業界を変革する可能性のあるアイデアを提案してください。"
                    }
                ]
            },
            
            ExpertiseArea.SOCIAL: {
                "profiles": [
                    {
                        "name": "社会学者",
                        "personality": "社会的影響重視、多様性尊重",
                        "debate_style": "社会構造分析、文化的背景考慮、包括性重視",
                        "knowledge_focus": ["社会構造", "文化人類学", "社会心理学", "社会問題"],
                        "system_template": "あなたは社会の仕組みに精通した社会学者です。{topic}について、社会への影響や文化的背景、多様性や包括性の観点から分析し、社会全体の利益を考慮した議論を行ってください。"
                    }
                ]
            }
        }
    
    def analyze_topic_and_generate_agents(self, topic: str, num_agents: int = 4) -> List[AgentProfile]:
        """トピック分析に基づいて適切なエージェントを生成"""
        
        # トピック分析
        relevant_areas = self.topic_analyzer.identify_relevant_expertise(topic)
        
        # 関連する専門分野から適切な数のエージェントを選択
        selected_agents = []
        
        for area in relevant_areas[:num_agents]:
            if area in self.agent_templates:
                profiles = self.agent_templates[area]["profiles"]
                # 最適なプロファイルを選択（簡易実装では最初の1つ）
                profile_data = profiles[0]
                
                agent_profile = self._create_agent_profile(
                    area, profile_data, topic
                )
                selected_agents.append(agent_profile)
        
        # 不足分を補完（多様性確保）
        while len(selected_agents) < num_agents:
            remaining_areas = [area for area in ExpertiseArea if area not in [agent.expertise_area for agent in selected_agents]]
            if remaining_areas and remaining_areas[0] in self.agent_templates:
                area = remaining_areas[0]
                profile_data = self.agent_templates[area]["profiles"][0]
                agent_profile = self._create_agent_profile(area, profile_data, topic)
                selected_agents.append(agent_profile)
            else:
                break
        
        return selected_agents
    
    def _create_agent_profile(self, area: ExpertiseArea, profile_data: Dict[str, Any], topic: str) -> AgentProfile:
        """エージェントプロファイルを作成"""
        
        system_message = profile_data["system_template"].format(topic=topic)
        
        return AgentProfile(
            name=profile_data["name"],
            role=f"{area.value}_expert",
            expertise_area=area,
            personality=profile_data["personality"],
            system_message=system_message,
            debate_style=profile_data["debate_style"],
            knowledge_focus=profile_data["knowledge_focus"],
            interaction_patterns=self._generate_interaction_patterns(profile_data["debate_style"])
        )
    
    def _generate_interaction_patterns(self, debate_style: str) -> List[str]:
        """議論スタイルに基づいて相互作用パターンを生成"""
        patterns = []
        
        if "データ駆動" in debate_style:
            patterns.append("具体的な数値や統計を要求する")
            patterns.append("エビデンスの出典を確認する")
        
        if "ユーザー体験重視" in debate_style:
            patterns.append("ユーザーの視点で問題を再定義する")
            patterns.append("実際の使用例を求める")
        
        if "創造的" in debate_style or "革新的" in debate_style:
            patterns.append("従来とは異なる視点を提示する")
            patterns.append("アナロジーや比喩を活用する")
        
        if "リスク分析" in debate_style:
            patterns.append("潜在的な問題点を指摘する")
            patterns.append("代替案を提案する")
        
        return patterns


class TopicAnalyzer:
    """トピック分析クラス"""
    
    def __init__(self):
        self.expertise_keywords = {
            ExpertiseArea.TECHNOLOGY: [
                "AI", "機械学習", "プログラミング", "システム", "アプリ", "ソフトウェア",
                "クラウド", "データベース", "セキュリティ", "アルゴリズム", "コード",
                "技術", "開発", "エンジニアリング", "デジタル", "IT"
            ],
            ExpertiseArea.BUSINESS: [
                "ビジネス", "経営", "戦略", "マーケティング", "売上", "収益", "投資",
                "企業", "競合", "市場", "顧客", "ブランド", "商品", "サービス",
                "ROI", "KPI", "マネジメント", "組織"
            ],
            ExpertiseArea.ACADEMIC: [
                "研究", "学術", "論文", "理論", "分析", "調査", "実験", "仮説",
                "統計", "データ", "エビデンス", "科学", "学問", "教育", "大学"
            ],
            ExpertiseArea.CREATIVE: [
                "デザイン", "創造", "アート", "クリエイティブ", "イノベーション",
                "発想", "アイデア", "表現", "美的", "感性", "インスピレーション",
                "ブランディング", "コミュニケーション"
            ],
            ExpertiseArea.SOCIAL: [
                "社会", "文化", "人々", "コミュニティ", "多様性", "包括性",
                "社会問題", "社会的影響", "倫理", "価値観", "人権", "平等"
            ],
            ExpertiseArea.LEGAL: [
                "法律", "法的", "規制", "コンプライアンス", "契約", "権利",
                "法務", "裁判", "判例", "条文"
            ],
            ExpertiseArea.MEDICAL: [
                "医療", "健康", "病気", "治療", "薬", "医学", "患者",
                "診断", "医師", "看護", "ヘルスケア"
            ],
            ExpertiseArea.FINANCE: [
                "金融", "投資", "資金", "財務", "会計", "税務", "保険",
                "銀行", "資産", "リスク", "収支", "予算"
            ],
            ExpertiseArea.ENVIRONMENT: [
                "環境", "持続可能", "エコ", "気候", "自然", "リサイクル",
                "省エネ", "温暖化", "生態系", "環境問題"
            ],
            ExpertiseArea.EDUCATION: [
                "教育", "学習", "授業", "カリキュラム", "学校", "大学",
                "教師", "学生", "スキル", "能力開発", "人材育成"
            ]
        }
    
    def identify_relevant_expertise(self, topic: str) -> List[ExpertiseArea]:
        """トピックから関連する専門分野を特定"""
        topic_lower = topic.lower()
        relevance_scores = {}
        
        for area, keywords in self.expertise_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in topic_lower:
                    score += 1
            relevance_scores[area] = score
        
        # スコアの高い順にソート
        sorted_areas = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        
        # スコアが0より大きい分野を返す、最低2つは返す
        relevant_areas = [area for area, score in sorted_areas if score > 0]
        
        if len(relevant_areas) < 2:
            # 関連性が低い場合でも、多様性確保のため最低限の分野を追加
            all_areas = list(ExpertiseArea)
            for area in all_areas:
                if area not in relevant_areas:
                    relevant_areas.append(area)
                if len(relevant_areas) >= 4:
                    break
        
        return relevant_areas[:6]  # 最大6つの専門分野