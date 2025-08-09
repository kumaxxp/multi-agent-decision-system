"""
HTMLビューアー - インテリジェント協調結果の可視化
議論結果をHTML形式で美しく表示
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from result_analyzer import ResultAnalyzer
import argparse
from pathlib import Path


class HTMLViewer:
    """HTML結果ビューアー"""
    
    def __init__(self):
        self.analyzer = ResultAnalyzer()
        self.template_dir = "html_templates"
        self.output_dir = "html_reports"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_session_report(self, session_id: str) -> str:
        """セッションのHTML報告書を生成"""
        
        # セッション読み込み
        session_data = self.analyzer.load_session(session_id)
        if not session_data:
            raise ValueError(f"セッション {session_id} が見つかりません")
        
        # 分析実行
        analysis = self.analyzer.analyze_session(session_data)
        
        # HTML生成
        html_content = self._generate_html_content(session_data, analysis)
        
        # ファイル保存
        output_file = os.path.join(self.output_dir, f"session_{session_id}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return output_file
    
    def _generate_html_content(self, session_data: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """HTML内容を生成"""
        
        session_info = session_data["session_info"]
        agents = session_data["agents"]
        discussion_rounds = session_data["discussion_rounds"]
        final_conclusion = session_data["final_conclusion"]
        
        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>議論分析レポート - {session_info['topic']}</title>
    <style>
        {self._get_css_styles()}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="container">
        {self._generate_header_section(session_info)}
        {self._generate_summary_section(analysis['basic_stats'])}
        {self._generate_agents_section(agents, analysis['agent_analysis'])}
        {self._generate_rounds_section(discussion_rounds, analysis['round_analysis'])}
        {self._generate_collaboration_section(analysis['collaboration_patterns'])}
        {self._generate_evolution_section(analysis['opinion_evolution'])}
        {self._generate_conclusion_section(final_conclusion)}
        {self._generate_charts_section()}
    </div>
    
    <script>
        {self._generate_javascript()}
    </script>
</body>
</html>
        """
        
        return html
    
    def _get_css_styles(self) -> str:
        """CSSスタイルを取得"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
            border-radius: 15px;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .session-info {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin-top: 20px;
            gap: 20px;
        }
        
        .info-item {
            background: rgba(255,255,255,0.1);
            padding: 15px 20px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .section {
            padding: 30px;
            border-bottom: 1px solid #eee;
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-left: 5px solid #3498db;
            padding-left: 15px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
            display: block;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .agent-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            transition: box-shadow 0.3s ease;
        }
        
        .agent-card:hover {
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        .agent-name {
            color: #2c3e50;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        
        .expertise-badge {
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 0.7em;
            margin-left: 10px;
        }
        
        .agent-metrics {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        
        .metric {
            text-align: center;
        }
        
        .metric-value {
            font-weight: bold;
            color: #27ae60;
        }
        
        .round-timeline {
            margin: 20px 0;
        }
        
        .round-item {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
        }
        
        .round-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .round-number {
            background: #3498db;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
        }
        
        .opinion-distribution {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin: 15px 0;
        }
        
        .opinion-count {
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
            margin: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .progress-bar {
            width: 100%;
            height: 10px;
            background: #ecf0f1;
            border-radius: 5px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            transition: width 0.3s ease;
        }
        
        .consensus-high { background: #27ae60; }
        .consensus-medium { background: #f39c12; }
        .consensus-low { background: #e74c3c; }
        
        .conclusion-section {
            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
            color: white;
            padding: 40px 30px;
        }
        
        .conclusion-text {
            font-size: 1.2em;
            margin-bottom: 20px;
            line-height: 1.8;
        }
        
        .recommendation {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .chart-container {
            margin: 20px 0;
            height: 400px;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 0 10px;
            }
            
            .header .session-info {
                flex-direction: column;
            }
            
            .stats-grid,
            .agent-grid {
                grid-template-columns: 1fr;
            }
        }
        """
    
    def _generate_header_section(self, session_info: Dict[str, Any]) -> str:
        """ヘッダーセクション生成"""
        return f"""
        <div class="header">
            <h1>🔍 議論分析レポート</h1>
            <div class="session-info">
                <div class="info-item">
                    <strong>トピック</strong><br>
                    {session_info['topic']}
                </div>
                <div class="info-item">
                    <strong>セッションID</strong><br>
                    {session_info['session_id']}
                </div>
                <div class="info-item">
                    <strong>実施日時</strong><br>
                    {datetime.fromisoformat(session_info['timestamp']).strftime('%Y年%m月%d日 %H:%M')}
                </div>
                <div class="info-item">
                    <strong>ラウンド数</strong><br>
                    {session_info['actual_rounds']}
                </div>
            </div>
        </div>
        """
    
    def _generate_summary_section(self, basic_stats: Dict[str, Any]) -> str:
        """サマリーセクション生成"""
        consensus_status = "✅ 達成" if basic_stats['consensus_achieved'] else "❌ 未達成"
        
        return f"""
        <div class="section">
            <h2>📊 基本統計</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">{basic_stats['total_agents']}</span>
                    <div class="stat-label">参加エージェント</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{basic_stats['total_opinions']}</span>
                    <div class="stat-label">総発言数</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{basic_stats['duration_rounds']}</span>
                    <div class="stat-label">実施ラウンド</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{consensus_status}</span>
                    <div class="stat-label">合意達成</div>
                </div>
            </div>
        </div>
        """
    
    def _generate_agents_section(self, agents: List[Dict[str, Any]], agent_analysis: Dict[str, Any]) -> str:
        """エージェントセクション生成"""
        
        agents_html = ""
        for agent in agents:
            name = agent['name']
            if name in agent_analysis:
                analysis = agent_analysis[name]
                agents_html += f"""
                <div class="agent-card">
                    <div class="agent-name">
                        👤 {name}
                        <span class="expertise-badge">{agent['expertise_area']}</span>
                    </div>
                    <div style="color: #666; margin: 10px 0;">
                        {agent['personality']}
                    </div>
                    <div class="agent-metrics">
                        <div class="metric">
                            <div class="metric-value">{analysis['average_confidence']:.2f}</div>
                            <div style="font-size: 0.8em;">平均信頼度</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{analysis['influence_score']:.2f}</div>
                            <div style="font-size: 0.8em;">影響力</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{analysis['opinion_consistency']:.2f}</div>
                            <div style="font-size: 0.8em;">一貫性</div>
                        </div>
                        <div class="metric">
                            <div class="metric-value">{analysis['total_responses']}</div>
                            <div style="font-size: 0.8em;">発言回数</div>
                        </div>
                    </div>
                </div>
                """
        
        return f"""
        <div class="section">
            <h2>👥 エージェント分析</h2>
            <div class="agent-grid">
                {agents_html}
            </div>
        </div>
        """
    
    def _generate_rounds_section(self, discussion_rounds: List[Dict[str, Any]], round_analysis: List[Dict[str, Any]]) -> str:
        """ラウンドセクション生成"""
        
        rounds_html = ""
        for i, (round_data, analysis) in enumerate(zip(discussion_rounds, round_analysis)):
            round_num = round_data['round_number']
            
            # 意見分布の表示
            opinion_dist = ""
            if analysis['opinion_distribution']:
                for opinion, count in analysis['opinion_distribution'].items():
                    opinion_dist += f'<div class="opinion-count"><strong>{count}</strong> {opinion}</div>'
            
            # コラボレーション情報
            collab_info = ""
            if analysis['collaboration_metrics']:
                collab = analysis['collaboration_metrics']
                consensus_level = collab.get('consensus_level', 0)
                progress_class = self._get_consensus_class(consensus_level)
                
                collab_info = f"""
                <div style="margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between;">
                        <span>合意度: {consensus_level:.2f}</span>
                        <span>対立レベル: {collab.get('conflict_level', 'N/A')}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill {progress_class}" style="width: {consensus_level * 100}%"></div>
                    </div>
                </div>
                """
            
            rounds_html += f"""
            <div class="round-item">
                <div class="round-header">
                    <span class="round-number">ラウンド {round_num}</span>
                    <span>平均信頼度: {analysis['average_confidence']:.2f}</span>
                </div>
                
                <div class="opinion-distribution">
                    {opinion_dist}
                </div>
                
                {collab_info}
                
                <div style="margin-top: 15px;">
                    <strong>証拠使用率:</strong> {analysis['evidence_usage_rate']:.2f}
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2>🔄 ラウンド別進展</h2>
            <div class="round-timeline">
                {rounds_html}
            </div>
        </div>
        """
    
    def _generate_collaboration_section(self, collaboration_patterns: Dict[str, Any]) -> str:
        """協調パターンセクション生成"""
        
        trend = collaboration_patterns['consensus_trend']
        trend_emoji = {
            'increasing': '📈 向上',
            'decreasing': '📉 低下',
            'stable': '➡️ 安定',
            'insufficient_data': '❓ データ不足'
        }.get(trend, trend)
        
        effectiveness = collaboration_patterns['collaboration_effectiveness']
        effectiveness_color = {
            'highly_effective': '#27ae60',
            'moderately_effective': '#f39c12',
            'partially_effective': '#e67e22',
            'low_effectiveness': '#e74c3c'
        }.get(effectiveness, '#95a5a6')
        
        return f"""
        <div class="section">
            <h2>🤝 協調パターン分析</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-value">{trend_emoji}</span>
                    <div class="stat-label">合意の傾向</div>
                </div>
                <div class="stat-card">
                    <span class="stat-value">{collaboration_patterns['final_consensus']:.2f}</span>
                    <div class="stat-label">最終合意度</div>
                </div>
                <div class="stat-card" style="background-color: {effectiveness_color}; color: white;">
                    <span class="stat-value" style="color: white;">{effectiveness}</span>
                    <div class="stat-label" style="color: rgba(255,255,255,0.8);">協調効果</div>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <canvas id="consensusChart" class="chart-container"></canvas>
            </div>
        </div>
        """
    
    def _generate_evolution_section(self, opinion_evolution: Dict[str, Any]) -> str:
        """意見進化セクション生成"""
        
        patterns_html = ""
        if 'evolution_patterns' in opinion_evolution:
            for agent_name, pattern_data in opinion_evolution['evolution_patterns'].items():
                pattern_emoji = {
                    'consistent': '🎯',
                    'slight_shift': '🔄',
                    'major_shift': '🔀'
                }.get(pattern_data['pattern'], '❓')
                
                confidence_change = pattern_data['confidence_change']
                confidence_direction = '⬆️' if confidence_change > 0 else ('⬇️' if confidence_change < 0 else '➡️')
                
                patterns_html += f"""
                <div class="agent-card">
                    <div class="agent-name">{pattern_emoji} {agent_name}</div>
                    <div style="margin: 10px 0;">
                        <strong>変化パターン:</strong> {pattern_data['pattern']}<br>
                        <strong>初期意見:</strong> {pattern_data['initial_opinion']} → 
                        <strong>最終意見:</strong> {pattern_data['final_opinion']}<br>
                        <strong>信頼度変化:</strong> {confidence_direction} {confidence_change:+.2f}
                    </div>
                </div>
                """
        
        return f"""
        <div class="section">
            <h2>🔄 意見進化分析</h2>
            <div style="margin: 20px 0;">
                <div class="stat-card">
                    <span class="stat-value">{opinion_evolution['stability_score']:.2f}</span>
                    <div class="stat-label">安定性スコア</div>
                </div>
            </div>
            
            <div class="agent-grid">
                {patterns_html}
            </div>
        </div>
        """
    
    def _generate_conclusion_section(self, final_conclusion: Dict[str, Any]) -> str:
        """結論セクション生成"""
        
        agreed_points = ""
        for point in final_conclusion.get('agreed_points', []):
            agreed_points += f"<li>✅ {point}</li>"
        
        disagreed_points = ""
        for point in final_conclusion.get('disagreed_points', []):
            disagreed_points += f"<li>❌ {point}</li>"
        
        return f"""
        <div class="conclusion-section">
            <h2 style="color: white; border-left: 5px solid white;">🎯 最終結論</h2>
            
            <div class="conclusion-text">
                {final_conclusion['conclusion_text']}
            </div>
            
            <div class="recommendation">
                <h3 style="color: white; margin-bottom: 10px;">💡 推奨事項</h3>
                <p style="font-size: 1.1em;">{final_conclusion['recommendation']}</p>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px;">
                <div class="recommendation">
                    <h4 style="color: white;">合意点</h4>
                    <ul style="margin-top: 10px;">
                        {agreed_points if agreed_points else "<li>特定の合意点なし</li>"}
                    </ul>
                </div>
                <div class="recommendation">
                    <h4 style="color: white;">不一致点</h4>
                    <ul style="margin-top: 10px;">
                        {disagreed_points if disagreed_points else "<li>特定の不一致点なし</li>"}
                    </ul>
                </div>
            </div>
        </div>
        """
    
    def _generate_charts_section(self) -> str:
        """チャートセクション生成"""
        return ""
    
    def _generate_javascript(self) -> str:
        """JavaScript生成"""
        return """
        // 合意度推移チャート
        const ctx = document.getElementById('consensusChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['ラウンド1', 'ラウンド2', 'ラウンド3'],
                datasets: [{
                    label: '合意度',
                    data: [0.3, 0.6, 0.8],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: '合意度の推移'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1
                    }
                }
            }
        });
        """
    
    def _get_consensus_class(self, level: float) -> str:
        """合意レベルに応じたCSSクラスを取得"""
        if level >= 0.7:
            return "consensus-high"
        elif level >= 0.4:
            return "consensus-medium"
        else:
            return "consensus-low"
    
    def generate_index_page(self) -> str:
        """インデックスページ生成"""
        sessions = self.analyzer.list_available_sessions()
        
        sessions_html = ""
        for session in sessions:
            sessions_html += f"""
            <div class="session-item">
                <div class="session-header">
                    <h3>{session['session_id']}</h3>
                    <span class="session-date">{session['created_time']}</span>
                </div>
                <div class="session-info">
                    <span>サイズ: {session['file_size']}</span>
                    <a href="session_{session['session_id']}.html" class="view-button">詳細を見る</a>
                </div>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>議論セッション一覧</title>
    <style>
        {self._get_index_css()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗂️ 議論セッション一覧</h1>
            <p>インテリジェント協調システムの実行結果</p>
        </div>
        
        <div class="sessions-list">
            {sessions_html if sessions_html else "<p>まだセッションがありません。main_intelligent_collaboration.py を実行してセッションを作成してください。</p>"}
        </div>
    </div>
</body>
</html>
        """
        
        index_file = os.path.join(self.output_dir, "index.html")
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(html)
        
        return index_file
    
    def _get_index_css(self) -> str:
        """インデックスページ用CSS"""
        return """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .sessions-list {
            padding: 30px;
        }
        
        .session-item {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
            transition: box-shadow 0.3s ease;
        }
        
        .session-item:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .session-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .session-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .view-button {
            background: #3498db;
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s ease;
        }
        
        .view-button:hover {
            background: #2980b9;
        }
        """


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description="HTML報告書ジェネレーター")
    parser.add_argument("--session", type=str, help="生成するセッションID")
    parser.add_argument("--index", action="store_true", help="インデックスページを生成")
    parser.add_argument("--all", action="store_true", help="全セッションの報告書を生成")
    
    args = parser.parse_args()
    
    viewer = HTMLViewer()
    
    if args.index:
        # インデックスページ生成
        index_file = viewer.generate_index_page()
        print(f"📄 インデックスページを生成しました: {index_file}")
        return
    
    if args.all:
        # 全セッション処理
        analyzer = ResultAnalyzer()
        sessions = analyzer.list_available_sessions()
        
        if not sessions:
            print("📂 セッションが見つかりませんでした。")
            return
        
        print(f"🔄 {len(sessions)}個のセッションを処理中...")
        
        for session in sessions:
            try:
                output_file = viewer.generate_session_report(session['session_id'])
                print(f"✅ {session['session_id']} → {output_file}")
            except Exception as e:
                print(f"❌ {session['session_id']} でエラー: {e}")
        
        # インデックスページも生成
        index_file = viewer.generate_index_page()
        print(f"📄 インデックスページ: {index_file}")
        print(f"🎉 全ての報告書が {viewer.output_dir} に生成されました！")
        return
    
    if args.session:
        # 特定セッション処理
        try:
            output_file = viewer.generate_session_report(args.session)
            print(f"✅ HTML報告書を生成しました: {output_file}")
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
        return
    
    # インタラクティブモード
    analyzer = ResultAnalyzer()
    sessions = analyzer.list_available_sessions()
    
    if not sessions:
        print("📂 セッションが見つかりませんでした。")
        print("まず main_intelligent_collaboration.py を実行してセッションを作成してください。")
        return
    
    print("📋 利用可能なセッション:")
    for i, session in enumerate(sessions, 1):
        print(f"  {i}. {session['session_id']} ({session['created_time']})")
    
    print(f"  {len(sessions) + 1}. 全セッション")
    print(f"  {len(sessions) + 2}. インデックスのみ")
    
    try:
        choice = int(input("\n生成したい番号を選択してください: "))
        
        if 1 <= choice <= len(sessions):
            session_id = sessions[choice - 1]['session_id']
            output_file = viewer.generate_session_report(session_id)
            print(f"✅ HTML報告書を生成しました: {output_file}")
        elif choice == len(sessions) + 1:
            # 全セッション
            for session in sessions:
                try:
                    output_file = viewer.generate_session_report(session['session_id'])
                    print(f"✅ {session['session_id']} → {output_file}")
                except Exception as e:
                    print(f"❌ {session['session_id']} でエラー: {e}")
            
            index_file = viewer.generate_index_page()
            print(f"📄 インデックスページ: {index_file}")
        elif choice == len(sessions) + 2:
            # インデックスのみ
            index_file = viewer.generate_index_page()
            print(f"📄 インデックスページを生成しました: {index_file}")
        else:
            print("❌ 無効な選択です。")
    
    except ValueError:
        print("❌ 無効な入力です。")


if __name__ == "__main__":
    main()