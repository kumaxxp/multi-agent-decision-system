"""
統合システムテスト
全コンポーネントの動作を検証
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any

def test_environment_setup():
    """環境設定のテスト"""
    print("🔧 環境設定テスト")
    
    # 必要なモジュールのインポートテスト
    try:
        from main_intelligent_collaboration import IntelligentCollaborationSystem
        from result_analyzer import ResultAnalyzer
        from html_viewer import HTMLViewer
        from agent_factory import AgentFactory
        from collaboration_system import CollaborationOrchestrator
        from web_search_agent import WebSearchAgent
        print("✅ 全モジュールのインポートが成功")
    except ImportError as e:
        print(f"❌ モジュールインポートエラー: {e}")
        return False
    
    # 環境変数チェック（デモ用）
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        print("✅ OPENAI_API_KEY が設定されています")
    else:
        print("⚠️ OPENAI_API_KEY が設定されていません（デモモードで実行）")
    
    return True


def test_agent_factory():
    """エージェント生成システムのテスト"""
    print("\n🎭 エージェント生成システムテスト")
    
    try:
        from agent_factory import AgentFactory, ExpertiseArea
        
        factory = AgentFactory()
        
        # テストトピック
        test_topics = [
            "AIの倫理的な開発について",
            "持続可能なビジネスモデル",
            "教育におけるデジタル化"
        ]
        
        for topic in test_topics:
            agents = factory.analyze_topic_and_generate_agents(topic, 3)
            print(f"📋 トピック: '{topic}'")
            print(f"   生成エージェント数: {len(agents)}")
            
            for i, agent in enumerate(agents, 1):
                print(f"   {i}. {agent.name} ({agent.expertise_area.value})")
        
        print("✅ エージェント生成テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ エージェント生成テストエラー: {e}")
        return False


def test_collaboration_system():
    """協調システムのテスト"""
    print("\n🤝 協調システムテスト")
    
    try:
        from collaboration_system import CollaborationOrchestrator, Opinion, OpinionType
        
        orchestrator = CollaborationOrchestrator()
        
        # テスト用意見データ
        test_opinions = [
            Opinion(
                agent_name="テストエージェント1",
                content="この提案に賛成します。データに基づいて有効だと考えます。",
                opinion_type=OpinionType.AGREE,
                confidence=0.8,
                evidence=["研究データ"],
                related_topics=["効率性"],
                timestamp=datetime.now().isoformat()
            ),
            Opinion(
                agent_name="テストエージェント2",
                content="いくつか懸念点があります。慎重に検討すべきです。",
                opinion_type=OpinionType.DISAGREE,
                confidence=0.6,
                evidence=["過去の事例"],
                related_topics=["リスク"],
                timestamp=datetime.now().isoformat()
            )
        ]
        
        result = orchestrator.process_agent_interactions(test_opinions, "テストトピック")
        
        print(f"📊 対立レベル: {result['conflict_level']}")
        print(f"📈 合意度: {result['consensus'].consensus_level}")
        print(f"🎯 解決戦略: {result['resolution_strategy']['strategy']}")
        
        print("✅ 協調システムテスト完了")
        return True
        
    except Exception as e:
        print(f"❌ 協調システムテストエラー: {e}")
        return False


def test_web_search_agent():
    """Web検索エージェントのテスト"""
    print("\n🔍 Web検索エージェントテスト")
    
    try:
        from web_search_agent import WebSearchAgent, FactChecker, TrendAnalyzer
        
        searcher = WebSearchAgent()
        fact_checker = FactChecker(searcher)
        trend_analyzer = TrendAnalyzer(searcher)
        
        # 検索テスト
        results = searcher.search_for_topic("AI technology", "web", 2)
        print(f"🔎 検索結果数: {len(results)}")
        
        for result in results:
            print(f"   📄 {result.title} (関連性: {result.relevance_score:.2f})")
        
        # ファクトチェックテスト
        fact_result = fact_checker.verify_claim("AIは人間の仕事を奪う")
        print(f"✅ ファクトチェック結果: {fact_result.verdict} (信頼度: {fact_result.confidence})")
        
        # トレンド分析テスト
        trend_result = trend_analyzer.analyze_trend("人工知能")
        print(f"📈 トレンドスコア: {trend_result['trend_score']:.2f}")
        print(f"😊 感情分析: {trend_result['sentiment']['overall']}")
        
        print("✅ Web検索エージェントテスト完了")
        return True
        
    except Exception as e:
        print(f"❌ Web検索エージェントテストエラー: {e}")
        return False


def test_result_analyzer():
    """結果分析システムのテスト"""
    print("\n📊 結果分析システムテスト")
    
    try:
        from result_analyzer import ResultAnalyzer
        
        analyzer = ResultAnalyzer()
        
        # セッション一覧取得テスト
        sessions = analyzer.list_available_sessions()
        print(f"📂 利用可能セッション数: {len(sessions)}")
        
        if sessions:
            # 最新セッションの分析テスト
            latest_session = sessions[0]
            print(f"🔍 分析対象: {latest_session['session_id']}")
            
            session_data = analyzer.load_session(latest_session['session_id'])
            if session_data:
                analysis = analyzer.analyze_session(session_data)
                print(f"📈 基本統計: {analysis['basic_stats']}")
                print("✅ セッション分析テスト完了")
            else:
                print("⚠️ セッションデータの読み込みに失敗")
        else:
            print("ℹ️ 分析対象のセッションがありません")
        
        return True
        
    except Exception as e:
        print(f"❌ 結果分析システムテストエラー: {e}")
        return False


def test_html_viewer():
    """HTMLビューアーのテスト"""
    print("\n📄 HTMLビューアーテスト")
    
    try:
        from html_viewer import HTMLViewer
        
        viewer = HTMLViewer()
        
        # インデックスページ生成テスト
        index_file = viewer.generate_index_page()
        
        if os.path.exists(index_file):
            file_size = os.path.getsize(index_file)
            print(f"✅ インデックスページ生成: {index_file} ({file_size} bytes)")
        else:
            print("❌ インデックスページの生成に失敗")
            return False
        
        # セッション報告書生成テスト（セッションが存在する場合）
        from result_analyzer import ResultAnalyzer
        analyzer = ResultAnalyzer()
        sessions = analyzer.list_available_sessions()
        
        if sessions:
            try:
                session_id = sessions[0]['session_id']
                report_file = viewer.generate_session_report(session_id)
                
                if os.path.exists(report_file):
                    file_size = os.path.getsize(report_file)
                    print(f"✅ セッション報告書生成: {report_file} ({file_size} bytes)")
                else:
                    print("❌ セッション報告書の生成に失敗")
                    return False
            except Exception as e:
                print(f"⚠️ セッション報告書生成でエラー: {e}")
        
        print("✅ HTMLビューアーテスト完了")
        return True
        
    except Exception as e:
        print(f"❌ HTMLビューアーテストエラー: {e}")
        return False


def test_mcp_integration():
    """MCP統合のテスト"""
    print("\n🔌 MCP統合テスト")
    
    try:
        from mcp_integration import RealMCPIntegration
        
        mcp = RealMCPIntegration()
        
        # 利用可能ツールの確認
        tools = mcp.get_available_tools()
        print(f"🛠️ 利用可能ツール数: {len(tools)}")
        
        for tool_name in list(tools.keys())[:3]:  # 最初の3つを表示
            print(f"   🔧 {tool_name}")
        
        print("✅ MCP統合テスト完了")
        return True
        
    except Exception as e:
        print(f"❌ MCP統合テストエラー: {e}")
        return False


def create_demo_session():
    """デモセッションの作成"""
    print("\n🚀 デモセッション作成")
    
    # デモ用のセッションデータを作成
    demo_session = {
        "session_info": {
            "session_id": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic": "AIの社会実装における課題と機会",
            "timestamp": datetime.now().isoformat(),
            "num_agents": 3,
            "max_rounds": 2,
            "actual_rounds": 2
        },
        "agents": [
            {
                "name": "テックエバンジェリスト",
                "role": "technology_expert",
                "expertise_area": "technology",
                "personality": "革新的で楽観的、技術の可能性を追求",
                "debate_style": "データ駆動、実例重視、未来志向",
                "knowledge_focus": ["AI/ML", "最新技術動向"],
                "interaction_patterns": ["具体的な数値を要求", "実例重視"]
            },
            {
                "name": "社会学者", 
                "role": "social_expert",
                "expertise_area": "social",
                "personality": "社会的影響重視、多様性尊重",
                "debate_style": "社会構造分析、包括性重視",
                "knowledge_focus": ["社会問題", "文化人類学"],
                "interaction_patterns": ["社会への影響を考慮", "多様性重視"]
            },
            {
                "name": "戦略コンサルタント",
                "role": "business_expert", 
                "expertise_area": "business",
                "personality": "分析的で結果重視、ビジネス価値を追求",
                "debate_style": "ROI重視、市場データ活用",
                "knowledge_focus": ["経営戦略", "市場分析"],
                "interaction_patterns": ["ROI分析", "市場データ重視"]
            }
        ],
        "background_info": {
            "search_results": [
                {
                    "title": "AI技術の社会実装：現状と課題",
                    "source": "Tech Review",
                    "snippet": "AI技術の急速な発展により、様々な分野での実装が進む一方、倫理的課題や雇用への影響が懸念されている。",
                    "relevance_score": 0.95
                }
            ],
            "search_summary": {
                "total_results": 5,
                "average_relevance": 0.85
            },
            "trend_analysis": {
                "trend_score": 0.8,
                "sentiment": {
                    "overall": "mixed"
                }
            }
        },
        "discussion_rounds": [
            {
                "round_number": 1,
                "agent_responses": [
                    {
                        "agent_name": "テックエバンジェリスト",
                        "expertise_area": "technology",
                        "response": "AIの社会実装は確実に進んでいます。機械学習技術の進歩により、医療診断の精度が向上し、自動運転技術も実用化段階です。データによると、AI市場は年率30%で成長しており、これは大きな機会です。",
                        "opinion": {
                            "type": "strongly_agree",
                            "confidence": 0.9,
                            "evidence": ["市場データ", "実用事例"]
                        }
                    },
                    {
                        "agent_name": "社会学者",
                        "expertise_area": "social", 
                        "response": "技術的な進歩は素晴らしいですが、社会への影響を慎重に考慮する必要があります。AIの導入により雇用が失われる可能性や、アルゴリズムバイアスによる社会格差の拡大が懸念されます。包括的な議論が必要です。",
                        "opinion": {
                            "type": "neutral",
                            "confidence": 0.7,
                            "evidence": ["社会研究", "雇用統計"]
                        }
                    },
                    {
                        "agent_name": "戦略コンサルタント",
                        "expertise_area": "business",
                        "response": "ビジネス観点では、AI実装のROIは明確です。効率性向上により平均20%のコスト削減が可能で、新しいビジネスモデルも創出されています。しかし、投資対効果を慎重に評価し、段階的な導入戦略が重要です。",
                        "opinion": {
                            "type": "agree",
                            "confidence": 0.8,
                            "evidence": ["ROI分析", "市場調査"]
                        }
                    }
                ],
                "opinions": [],
                "timestamp": datetime.now().isoformat(),
                "collaboration_analysis": {
                    "conflict_level": "mild",
                    "consensus": {
                        "consensus_level": 0.6,
                        "agreed_points": ["AI技術の進歩", "経済的機会"],
                        "disagreed_points": ["社会への影響", "導入スピード"]
                    }
                }
            },
            {
                "round_number": 2,
                "agent_responses": [
                    {
                        "agent_name": "テックエバンジェリスト",
                        "expertise_area": "technology",
                        "response": "社会的懸念は理解できますが、適切な規制とガイドラインの策定により解決可能です。透明性のあるAIアルゴリズムの開発や、再教育プログラムの整備により、負の影響を最小化できると確信しています。",
                        "opinion": {
                            "type": "agree",
                            "confidence": 0.8,
                            "evidence": ["技術ガイドライン", "教育プログラム"]
                        }
                    },
                    {
                        "agent_name": "社会学者",
                        "expertise_area": "social",
                        "response": "規制とガイドラインの重要性に同意します。多様なステークホルダーを巻き込んだ包括的なアプローチが必要です。技術の恩恵を社会全体で共有し、デジタル格差を解消する施策が重要だと考えます。",
                        "opinion": {
                            "type": "agree",
                            "confidence": 0.75,
                            "evidence": ["社会包摂研究", "政策分析"]
                        }
                    },
                    {
                        "agent_name": "戦略コンサルタント",
                        "expertise_area": "business",
                        "response": "包括的アプローチに賛成です。企業としては、持続可能な成長のために社会的責任を果たしながらAI技術を活用すべきです。長期的な視点でのステークホルダー価値の最大化が重要な戦略となります。",
                        "opinion": {
                            "type": "strongly_agree",
                            "confidence": 0.85,
                            "evidence": ["ESG戦略", "長期成長モデル"]
                        }
                    }
                ],
                "opinions": [],
                "timestamp": datetime.now().isoformat(),
                "collaboration_analysis": {
                    "conflict_level": "harmony",
                    "consensus": {
                        "consensus_level": 0.8,
                        "agreed_points": ["規制の重要性", "包括的アプローチ", "社会的責任"],
                        "disagreed_points": []
                    }
                }
            }
        ],
        "final_conclusion": {
            "conclusion_text": "「AIの社会実装における課題と機会」についての2ラウンドの議論を通じて、参加者間で高い合意が形成されました。",
            "consensus_level": 0.8,
            "agreed_points": ["AI技術の経済的機会", "適切な規制の必要性", "包括的な社会実装アプローチ"],
            "disagreed_points": [],
            "conflict_level": "harmony",
            "resolution_strategy": "consensus_building",
            "recommendation": "合意に基づく実行計画の策定を推奨します。"
        },
        "overall_collaboration_metrics": {
            "total_rounds": 2,
            "total_opinions": 6,
            "agent_participation": {
                "テックエバンジェリスト": 2,
                "社会学者": 2, 
                "戦略コンサルタント": 2
            },
            "opinion_diversity": 0.6,
            "average_confidence": 0.8,
            "evidence_usage_rate": 1.0
        }
    }
    
    # セッションファイルの保存
    log_dir = "intelligent_collaboration_logs"
    os.makedirs(log_dir, exist_ok=True)
    
    session_file = os.path.join(log_dir, f"intelligent_session_{demo_session['session_info']['session_id']}.json")
    
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(demo_session, f, ensure_ascii=False, indent=2)
    
    print(f"✅ デモセッションを作成しました: {session_file}")
    return demo_session['session_info']['session_id']


def run_full_integration_test():
    """完全統合テストの実行"""
    print("🔬 === 完全統合テスト開始 ===\n")
    
    test_results = {}
    
    # 各テストの実行
    test_functions = [
        ("環境設定", test_environment_setup),
        ("エージェント生成", test_agent_factory), 
        ("協調システム", test_collaboration_system),
        ("Web検索", test_web_search_agent),
        ("MCP統合", test_mcp_integration),
        ("結果分析", test_result_analyzer),
        ("HTMLビューアー", test_html_viewer)
    ]
    
    for test_name, test_func in test_functions:
        try:
            result = test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name}テストで例外発生: {e}")
            test_results[test_name] = False
    
    # デモセッション作成（分析・ビューアーテスト用）
    print("\n" + "="*60)
    demo_session_id = create_demo_session()
    
    if demo_session_id:
        # デモセッションでの分析テスト
        print("\n📊 デモセッション分析テスト")
        try:
            from result_analyzer import ResultAnalyzer
            analyzer = ResultAnalyzer()
            session_data = analyzer.load_session(demo_session_id)
            analysis = analyzer.analyze_session(session_data)
            print("✅ デモセッション分析成功")
            
            # HTML報告書生成テスト
            print("\n📄 デモセッションHTML報告書生成")
            from html_viewer import HTMLViewer
            viewer = HTMLViewer()
            report_file = viewer.generate_session_report(demo_session_id)
            print(f"✅ HTML報告書生成: {report_file}")
            
        except Exception as e:
            print(f"❌ デモセッションテストエラー: {e}")
    
    # 結果サマリー
    print("\n" + "="*60)
    print("🎯 === テスト結果サマリー ===")
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print(f"\n📊 総合結果: {passed}/{total} テスト通過")
    
    if passed == total:
        print("🎉 全てのテストが成功しました！システムは正常に動作しています。")
    elif passed >= total * 0.8:
        print("⚠️ 大部分のテストが成功しましたが、いくつか修正が必要です。")
    else:
        print("❌ 重要な問題があります。修正が必要です。")
    
    return passed, total


def main():
    """メイン実行関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="統合システムテスト")
    parser.add_argument("--quick", action="store_true", help="クイックテストのみ実行")
    parser.add_argument("--demo", action="store_true", help="デモセッション作成のみ")
    parser.add_argument("--component", type=str, help="特定コンポーネントのみテスト")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_session_id = create_demo_session()
        print(f"✅ デモセッション作成完了: {demo_session_id}")
        return
    
    if args.component:
        component_tests = {
            "environment": test_environment_setup,
            "agents": test_agent_factory,
            "collaboration": test_collaboration_system,
            "websearch": test_web_search_agent,
            "mcp": test_mcp_integration,
            "analyzer": test_result_analyzer,
            "html": test_html_viewer
        }
        
        if args.component in component_tests:
            result = component_tests[args.component]()
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"\n{args.component}テスト結果: {status}")
        else:
            print(f"❌ 不明なコンポーネント: {args.component}")
            print(f"利用可能: {', '.join(component_tests.keys())}")
        return
    
    if args.quick:
        print("⚡ クイックテスト実行")
        env_ok = test_environment_setup()
        if env_ok:
            print("✅ 基本環境は正常です")
        else:
            print("❌ 環境設定に問題があります")
        return
    
    # フル統合テスト実行
    passed, total = run_full_integration_test()
    
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    main()