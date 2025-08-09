"""
Streamlit GUI - インテリジェント協調多エージェントシステム
シンプルで直感的なWebインターフェース
"""

import streamlit as st
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any, Optional

# システムモジュールのインポート（エラーハンドリング付き）
try:
    from main_intelligent_collaboration import IntelligentCollaborationSystem
    from result_analyzer import ResultAnalyzer
    from html_viewer import HTMLViewer
    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    MODULE_ERROR = str(e)

# ページ設定
st.set_page_config(
    page_title="インテリジェント協調多エージェントシステム",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    text-align: center;
    color: #1f77b4;
    margin-bottom: 2rem;
}

.stAlert {
    margin: 1rem 0;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #1f77b4;
}

.sidebar-header {
    font-size: 1.2rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
if 'discussion_result' not in st.session_state:
    st.session_state.discussion_result = None
if 'current_session_id' not in st.session_state:
    st.session_state.current_session_id = None

def check_environment():
    """環境チェック"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("🔑 OPENAI_API_KEYが設定されていません。環境変数を設定してください。")
        st.info("💡 .envファイルにOPENAI_API_KEY=your_api_keyを設定してください。")
        return False
    return True

def load_available_sessions():
    """利用可能なセッションを読み込み"""
    analyzer = ResultAnalyzer()
    return analyzer.list_available_sessions()

def run_discussion(topic: str, num_agents: int, max_rounds: int):
    """議論を実行"""
    if not check_environment():
        return None
    
    try:
        with st.spinner("🤖 議論を実行中...しばらくお待ちください"):
            # プログレスバー追加
            progress_bar = st.progress(0)
            progress_bar.progress(10)
            
            system = IntelligentCollaborationSystem()
            progress_bar.progress(20)
            
            result = system.run_intelligent_discussion(topic, num_agents, max_rounds)
            progress_bar.progress(100)
            
            # プログレスバーを削除
            progress_bar.empty()
            return result
    except ImportError as e:
        st.error(f"❌ モジュールインポートエラー: {str(e)}")
        st.info("💡 必要なPythonファイルが存在し、正しくインポートできることを確認してください。")
        return None
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {str(e)}")
        st.info("💡 エラーの詳細はターミナル/ログを確認してください。")
        return None

def display_discussion_results(result: Dict[str, Any]):
    """議論結果を表示"""
    if not result:
        return
    
    st.success("✅ 議論が完了しました！")
    
    # 基本情報
    session_info = result['session_info']
    final_conclusion = result['final_conclusion']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("参加エージェント", f"{session_info['num_agents']}人")
    
    with col2:
        st.metric("実施ラウンド", f"{session_info['actual_rounds']}ラウンド")
    
    with col3:
        consensus_level = final_conclusion['consensus_level']
        st.metric("合意度", f"{consensus_level:.2f}", delta=f"{consensus_level-0.5:.2f}")
    
    with col4:
        conflict_level = final_conclusion['conflict_level']
        conflict_emoji = {"harmony": "🤝", "mild": "⚠️", "moderate": "🔥", "strong": "💥"}.get(conflict_level, "❓")
        st.metric("対立レベル", f"{conflict_emoji} {conflict_level}")
    
    # 最終結論
    st.subheader("🎯 最終結論")
    st.write(final_conclusion['conclusion_text'])
    
    if final_conclusion.get('recommendation'):
        st.info(f"💡 **推奨事項**: {final_conclusion['recommendation']}")
    
    # エージェント情報
    st.subheader("👥 参加エージェント")
    agents = result['agents']
    
    for i, agent in enumerate(agents):
        with st.expander(f"🎭 {agent['name']} ({agent['expertise_area']})"):
            st.write(f"**特性**: {agent['personality']}")
            st.write(f"**議論スタイル**: {agent['debate_style']}")
            st.write(f"**専門分野**: {', '.join(agent['knowledge_focus'])}")

def display_session_analysis(session_id: str):
    """セッション分析を表示"""
    analyzer = ResultAnalyzer()
    
    # セッション読み込み
    session_data = analyzer.load_session(session_id)
    if not session_data:
        st.error(f"❌ セッション {session_id} が見つかりません")
        return
    
    # 分析実行
    with st.spinner("📊 分析中..."):
        analysis = analyzer.analyze_session(session_data)
    
    st.success("✅ 分析完了！")
    
    # 基本統計
    basic_stats = analysis['basic_stats']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("総発言数", basic_stats['total_opinions'])
    with col2:
        st.metric("エージェント数", basic_stats['total_agents'])
    with col3:
        consensus_achieved = "✅ 達成" if basic_stats['consensus_achieved'] else "❌ 未達成"
        st.metric("合意達成", consensus_achieved)
    
    # 合意度推移チャート
    st.subheader("📈 合意度推移")
    round_analysis = analysis['round_analysis']
    
    if len(round_analysis) > 1:
        # 合意度データの準備
        rounds = []
        consensus_levels = []
        
        for round_data in round_analysis:
            rounds.append(f"ラウンド{round_data['round_number']}")
            if round_data['collaboration_metrics']:
                consensus_levels.append(round_data['collaboration_metrics']['consensus_level'])
            else:
                consensus_levels.append(0.5)  # デフォルト値
        
        # Plotlyチャート作成
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rounds,
            y=consensus_levels,
            mode='lines+markers',
            name='合意度',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="合意度の推移",
            xaxis_title="ラウンド",
            yaxis_title="合意度",
            yaxis=dict(range=[0, 1]),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # エージェント分析
    st.subheader("🎭 エージェント分析")
    agent_analysis = analysis['agent_analysis']
    
    # エージェント性能チャート
    agent_names = list(agent_analysis.keys())
    confidence_scores = [data['average_confidence'] for data in agent_analysis.values()]
    influence_scores = [data['influence_score'] for data in agent_analysis.values()]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='平均信頼度',
        x=agent_names,
        y=confidence_scores,
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        name='影響力スコア',
        x=agent_names,
        y=influence_scores,
        marker_color='lightcoral'
    ))
    
    fig.update_layout(
        title="エージェント性能比較",
        xaxis_title="エージェント",
        yaxis_title="スコア",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 詳細データ表
    agent_df = pd.DataFrame([
        {
            "エージェント": name,
            "専門分野": data['expertise_area'],
            "平均信頼度": f"{data['average_confidence']:.2f}",
            "影響力": f"{data['influence_score']:.2f}",
            "一貫性": f"{data['opinion_consistency']:.2f}",
            "発言回数": data['total_responses']
        }
        for name, data in agent_analysis.items()
    ])
    
    st.subheader("📊 詳細データ")
    st.dataframe(agent_df, use_container_width=True)

def generate_html_report(session_id: str):
    """HTML報告書を生成"""
    try:
        viewer = HTMLViewer()
        report_file = viewer.generate_session_report(session_id)
        return report_file
    except Exception as e:
        st.error(f"❌ HTML報告書の生成に失敗しました: {str(e)}")
        return None

def display_html_report_in_streamlit(session_id: str):
    """StreamlitでHTML報告書を表示"""
    try:
        # HTML報告書生成
        report_file = generate_html_report(session_id)
        if not report_file:
            return
        
        # HTMLファイルを読み込み
        with open(report_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # StreamlitでHTMLを表示
        st.components.v1.html(html_content, height=800, scrolling=True)
        
    except Exception as e:
        st.error(f"❌ HTML報告書の表示に失敗しました: {str(e)}")

def display_conversation_details(session_id: str):
    """会話の詳細内容を表示"""
    analyzer = ResultAnalyzer()
    session_data = analyzer.load_session(session_id)
    
    if not session_data:
        st.error("❌ セッションデータが見つかりません")
        return
    
    st.header("💬 会話詳細")
    
    # セッション基本情報
    session_info = session_data['session_info']
    
    with st.expander("📋 セッション情報", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**トピック**: {session_info['topic']}")
            st.write(f"**セッションID**: {session_info['session_id']}")
        with col2:
            st.write(f"**実施日時**: {datetime.fromisoformat(session_info['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**ラウンド数**: {session_info['actual_rounds']}")
        with col3:
            st.write(f"**エージェント数**: {session_info['num_agents']}")
    
    # 背景情報
    if 'background_info' in session_data:
        with st.expander("🔍 背景情報"):
            bg_info = session_data['background_info']
            if 'search_summary' in bg_info:
                st.write(f"**関連記事数**: {bg_info['search_summary']['total_results']}")
                st.write(f"**平均関連性**: {bg_info['search_summary']['average_relevance']}")
            if 'trend_analysis' in bg_info:
                st.write(f"**トレンドスコア**: {bg_info['trend_analysis']['trend_score']}")
                st.write(f"**感情分析**: {bg_info['trend_analysis']['sentiment']['overall']}")
    
    # エージェント情報
    st.subheader("👥 参加エージェント")
    agents = session_data['agents']
    
    for agent in agents:
        with st.expander(f"🎭 {agent['name']} ({agent['expertise_area']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**役割**: {agent['role']}")
                st.write(f"**特性**: {agent['personality']}")
                st.write(f"**議論スタイル**: {agent['debate_style']}")
            with col2:
                st.write("**専門分野**:")
                for focus in agent['knowledge_focus']:
                    st.write(f"• {focus}")
                st.write("**相互作用パターン**:")
                for pattern in agent['interaction_patterns']:
                    st.write(f"• {pattern}")
    
    # ラウンド別詳細会話
    st.subheader("🔄 ラウンド別会話")
    discussion_rounds = session_data['discussion_rounds']
    
    for round_data in discussion_rounds:
        round_num = round_data['round_number']
        
        with st.expander(f"📞 ラウンド {round_num}", expanded=True):
            st.write(f"**実施時刻**: {datetime.fromisoformat(round_data['timestamp']).strftime('%H:%M:%S')}")
            
            # エージェント発言
            for i, response in enumerate(round_data['agent_responses']):
                agent_name = response['agent_name']
                agent_response = response['response']
                opinion = response['opinion']
                expertise = response['expertise_area']
                
                st.markdown(f"""
                <div style="
                    border: 2px solid #e1e5e9; 
                    border-radius: 10px; 
                    padding: 15px; 
                    margin: 10px 0; 
                    background: linear-gradient(90deg, #f8f9fa 0%, #ffffff 100%);
                    border-left: 5px solid #1f77b4;
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h4 style="margin: 0; color: #1f77b4;">🎭 {agent_name}</h4>
                        <span style="background: #1f77b4; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.8em;">
                            {expertise}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.write(f"**発言内容**:")
                st.write(agent_response)
                
                # 意見詳細
                col1, col2, col3 = st.columns(3)
                with col1:
                    opinion_emoji = {
                        "strongly_agree": "💚",
                        "agree": "✅",
                        "neutral": "🤝",
                        "disagree": "⚠️",
                        "strongly_disagree": "❌"
                    }
                    emoji = opinion_emoji.get(opinion['type'], "❓")
                    st.write(f"**意見**: {emoji} {opinion['type']}")
                
                with col2:
                    st.write(f"**信頼度**: {opinion['confidence']:.2f}")
                
                with col3:
                    if opinion['evidence']:
                        st.write(f"**根拠**: {', '.join(opinion['evidence'])}")
                    else:
                        st.write("**根拠**: なし")
                
                st.divider()
            
            # 協調分析結果
            if 'collaboration_analysis' in round_data:
                collab = round_data['collaboration_analysis']
                st.subheader("🤝 協調分析結果")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("対立レベル", collab['conflict_level'])
                    st.metric("合意度", f"{collab['consensus']['consensus_level']:.2f}")
                
                with col2:
                    st.write("**合意点**:")
                    for point in collab['consensus']['agreed_points']:
                        st.write(f"✅ {point}")
                    
                    st.write("**不一致点**:")
                    for point in collab['consensus']['disagreed_points']:
                        st.write(f"❗ {point}")
    
    # 最終結論
    st.subheader("🎯 最終結論")
    final_conclusion = session_data['final_conclusion']
    
    st.success(final_conclusion['conclusion_text'])
    st.info(f"💡 **推奨事項**: {final_conclusion['recommendation']}")
    
    # 合意した点と不一致点
    col1, col2 = st.columns(2)
    with col1:
        st.write("**✅ 合意点**:")
        for point in final_conclusion['agreed_points']:
            st.write(f"• {point}")
    
    with col2:
        st.write("**❗ 不一致点**:")
        for point in final_conclusion['disagreed_points']:
            st.write(f"• {point}")

def show_session_viewer(session_id: str):
    """セッション詳細ビューア"""
    st.header(f"📊 セッション詳細: {session_id}")
    
    # タブで切り替え
    tab1, tab2, tab3 = st.tabs(["💬 会話詳細", "📊 分析結果", "📄 HTML報告書"])
    
    with tab1:
        display_conversation_details(session_id)
    
    with tab2:
        display_session_analysis(session_id)
    
    with tab3:
        st.subheader("📄 HTML報告書")
        if st.button("🔄 HTML報告書を生成・表示", key=f"html_view_{session_id}"):
            with st.spinner("HTML報告書を生成中..."):
                display_html_report_in_streamlit(session_id)

def main():
    """メインアプリケーション"""
    
    # ヘッダー
    st.markdown('<h1 class="main-header">🤖 インテリジェント協調多エージェントシステム</h1>', unsafe_allow_html=True)
    
    # サイドバー
    with st.sidebar:
        st.markdown('<div class="sidebar-header">🛠️ 操作パネル</div>', unsafe_allow_html=True)
        
        mode = st.radio(
            "モードを選択",
            ["🚀 新しい議論を開始", "📊 過去の議論を分析", "📋 セッション一覧"],
            index=0
        )
    
    # モジュールチェック
    if not MODULES_LOADED:
        st.error(f"🚫 システムモジュールの読み込みに失敗しました: {MODULE_ERROR}")
        st.info("💡 必要なPythonファイルが存在することを確認してください。")
        st.stop()
    
    # 環境チェック
    if not check_environment():
        st.stop()
    
    if mode == "🚀 新しい議論を開始":
        st.header("🚀 新しい議論を開始")
        
        with st.form("discussion_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_area(
                    "議論トピック",
                    placeholder="例: AIの倫理的な活用方法について",
                    height=100,
                    help="議論したいトピックを入力してください"
                )
            
            with col2:
                num_agents = st.slider("参加エージェント数", 2, 6, 4, help="議論に参加するエージェントの数")
                max_rounds = st.slider("最大ラウンド数", 1, 5, 3, help="議論の最大ラウンド数")
            
            submitted = st.form_submit_button("🎯 議論を開始", type="primary", use_container_width=True)
        
        if submitted and topic:
            result = run_discussion(topic, num_agents, max_rounds)
            if result:
                st.session_state.discussion_result = result
                st.session_state.current_session_id = result['session_info']['session_id']
                st.rerun()
        elif submitted:
            st.warning("⚠️ 議論トピックを入力してください。")
        
        # 結果表示
        if st.session_state.discussion_result:
            st.divider()
            display_discussion_results(st.session_state.discussion_result)
            
            # アクションボタン
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💬 会話詳細を見る", key="view_details", type="primary"):
                    st.session_state.show_detailed_view = True
                    st.session_state.detailed_session_id = st.session_state.current_session_id
                    st.rerun()
            
            with col2:
                if st.button("📄 HTML報告書を表示", key="view_html"):
                    st.session_state.show_html_view = True
                    st.session_state.html_session_id = st.session_state.current_session_id
                    st.rerun()
            
            with col3:
                if st.button("💾 HTML報告書を生成", key="generate_html"):
                    if st.session_state.current_session_id:
                        with st.spinner("📄 HTML報告書を生成中..."):
                            report_file = generate_html_report(st.session_state.current_session_id)
                        if report_file:
                            st.success(f"✅ HTML報告書を生成しました: {report_file}")
                            st.info("💡 ファイルはローカルの html_reports/ フォルダに保存されました。")
        
        # 詳細ビュー表示
        if st.session_state.get('show_detailed_view') and st.session_state.get('detailed_session_id'):
            st.divider()
            show_session_viewer(st.session_state.detailed_session_id)
            if st.button("🔙 戻る", key="back_from_details"):
                st.session_state.show_detailed_view = False
                st.session_state.detailed_session_id = None
                st.rerun()
        
        # HTML表示
        if st.session_state.get('show_html_view') and st.session_state.get('html_session_id'):
            st.divider()
            st.subheader("📄 HTML報告書")
            display_html_report_in_streamlit(st.session_state.html_session_id)
            if st.button("🔙 戻る", key="back_from_html"):
                st.session_state.show_html_view = False
                st.session_state.html_session_id = None
                st.rerun()
    
    elif mode == "📊 過去の議論を分析":
        st.header("📊 過去の議論を分析")
        
        sessions = load_available_sessions()
        if not sessions:
            st.warning("📂 分析可能なセッションがありません。まず議論を実行してください。")
            return
        
        # セッション選択
        session_options = [f"{s['session_id']} ({s['created_time']})" for s in sessions]
        selected_option = st.selectbox("分析するセッションを選択", session_options)
        
        if selected_option:
            session_id = selected_option.split(" (")[0]
            
            # アクションボタン
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 詳細分析を見る", key=f"detailed_analysis_{session_id}"):
                    st.divider()
                    show_session_viewer(session_id)
            
            with col2:
                if st.button("📄 HTML報告書を表示", key=f"html_report_{session_id}"):
                    st.divider()
                    display_html_report_in_streamlit(session_id)
    
    elif mode == "📋 セッション一覧":
        st.header("📋 セッション一覧")
        
        sessions = load_available_sessions()
        if not sessions:
            st.info("📂 セッションがありません。")
            return
        
        st.write(f"**{len(sessions)}個のセッション**が保存されています。")
        
        for session in sessions:
            with st.expander(f"📊 {session['session_id']} - {session['created_time']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**セッションID**: {session['session_id']}")
                    st.write(f"**作成日時**: {session['created_time']}")
                    st.write(f"**ファイルサイズ**: {session['file_size']}")
                
                with col2:
                    # ボタンを縦に並べる
                    if st.button(f"💬 会話詳細", key=f"conversation_{session['session_id']}", use_container_width=True):
                        st.session_state.selected_session_for_detail = session['session_id']
                        st.rerun()
                    
                    if st.button(f"📊 分析結果", key=f"analyze_{session['session_id']}", use_container_width=True):
                        st.session_state.selected_session_for_analysis = session['session_id']
                        st.rerun()
                    
                    if st.button(f"📄 HTML報告書", key=f"html_{session['session_id']}", use_container_width=True):
                        st.session_state.selected_session_for_html = session['session_id']
                        st.rerun()
        
        # 選択されたセッションの詳細表示
        if st.session_state.get('selected_session_for_detail'):
            st.divider()
            show_session_viewer(st.session_state.selected_session_for_detail)
            if st.button("🔙 一覧に戻る", key="back_to_list_detail"):
                st.session_state.selected_session_for_detail = None
                st.rerun()
        
        # 選択されたセッションの分析結果
        if st.session_state.get('selected_session_for_analysis'):
            st.divider()
            display_session_analysis(st.session_state.selected_session_for_analysis)
            if st.button("🔙 一覧に戻る", key="back_to_list_analysis"):
                st.session_state.selected_session_for_analysis = None
                st.rerun()
        
        # 選択されたセッションのHTML報告書
        if st.session_state.get('selected_session_for_html'):
            st.divider()
            st.subheader(f"📄 HTML報告書: {st.session_state.selected_session_for_html}")
            display_html_report_in_streamlit(st.session_state.selected_session_for_html)
            if st.button("🔙 一覧に戻る", key="back_to_list_html"):
                st.session_state.selected_session_for_html = None
                st.rerun()
    
    # フッター
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem; margin-top: 2rem;'>
        🤖 インテリジェント協調多エージェントシステム v2.0<br>
        Powered by OpenAI GPT, Streamlit & Python
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()