import pandas as pd
from datetime import datetime
import json
import os

class TrendAnalyzer:
    def __init__(self):
        self.output_dir = 'outputs'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def analyze_trends(self, trends):
        """Comprehensive trend analysis"""
        if not trends:
            return {"error": "No trends to analyze"}
        
        # Convert to DataFrame
        df = pd.DataFrame(trends)
        
        # Calculate platform statistics
        platform_stats = df['platform'].value_counts().to_dict()
        
        # Get top trends by score
        top_trends = df.nlargest(5, 'score')[['platform', 'title', 'score']].to_dict('records')
        
        # Calculate category distribution
        category_stats = df['category'].value_counts().to_dict() if 'category' in df.columns else {}
        
        analysis = {
            'summary': {
                'total_trends': len(df),
                'sources': platform_stats,
                'categories': category_stats,
                'average_score': df['score'].mean(),
                'collection_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'top_trends': top_trends,
            'platform_analysis': self._analyze_by_platform(df),
            'raw_data_count': len(trends)
        }
        
        return analysis
    
    def _analyze_by_platform(self, df):
        """Analyze trends by platform"""
        platform_analysis = {}
        
        for platform in df['platform'].unique():
            platform_df = df[df['platform'] == platform]
            platform_analysis[platform] = {
                'count': len(platform_df),
                'average_score': platform_df['score'].mean(),
                'top_trend': platform_df.nlargest(1, 'score')['title'].iloc[0] if not platform_df.empty else None
            }
        
        return platform_analysis
    
    def save_analysis(self, trends, analysis, filename_prefix):
        """Save analysis results to files"""
        if not trends:
            return None, None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        
        # Save trends to CSV
        df = pd.DataFrame(trends)
        csv_file = f"{self.output_dir}/{filename_prefix}_trends_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        
        # Save analysis to JSON
        json_file = f"{self.output_dir}/{filename_prefix}_analysis_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        return csv_file, json_file
    
    def generate_report(self, analysis):
        """Generate a readable report"""
        if 'error' in analysis:
            return "No trends available for reporting."
        
        summary = analysis['summary']
        top_trends = analysis['top_trends']
        
        report = []
        report.append("📊 TREND ANALYSIS REPORT")
        report.append("=" * 50)
        report.append(f"Total Trends Collected: {summary['total_trends']}")
        report.append(f"Data Sources: {', '.join(summary['sources'].keys())}")
        report.append(f"Collection Time: {summary['collection_time']}")
        report.append(f"Average Trend Score: {summary['average_score']:.1f}")
        
        report.append("\n🔥 TOP 5 TRENDING TOPICS:")
        for i, trend in enumerate(top_trends, 1):
            report.append(f"{i}. [{trend['platform']}] {trend['title']} (Score: {trend['score']})")
        
        report.append("\n📈 PLATFORM BREAKDOWN:")
        for platform, stats in analysis['platform_analysis'].items():
            report.append(f"   - {platform}: {stats['count']} trends (Avg Score: {stats['average_score']:.1f})")
        
        return "\n".join(report)