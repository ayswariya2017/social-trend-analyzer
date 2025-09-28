import pandas as pd
from datetime import datetime
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.news_scraper import NewsScraper
from scrapers.github_trends import GitHubTrends
from scrapers.twitter_trends import TwitterTrends
from analysis.analyzer import TrendAnalyzer

class SocialTrendAnalyzer:
    def __init__(self):
        self.scrapers = {
            'news': NewsScraper(),
            'github': GitHubTrends(),
            'twitter': TwitterTrends()
        }
        self.analyzer = TrendAnalyzer()
        self.results = {
            'trends': [],
            'analysis': {},
            'files': {}
        }
    
    def collect_all_trends(self):
        """Collect trends from all sources"""
        all_trends = []
        
        print("🚀 COLLECTING TRENDS FROM MULTIPLE SOURCES")
        print("=" * 50)
        
        # Get news trends
        news_trends = self.scrapers['news'].scrape_all_news()
        all_trends.extend(news_trends)
        
        # Get GitHub trends
        github_trends = self.scrapers['github'].get_trending_repositories()
        all_trends.extend(github_trends)
        
        # Get Twitter trends
        twitter_trends = self.scrapers['twitter'].get_trending_topics()
        all_trends.extend(twitter_trends)
        
        self.results['trends'] = all_trends
        return all_trends
    
    def analyze_and_report(self):
        """Analyze trends and generate reports"""
        trends = self.results['trends']
        
        if not trends:
            print("❌ No trends collected for analysis")
            return None
        
        # Analyze trends
        analysis = self.analyzer.analyze_trends(trends)
        self.results['analysis'] = analysis
        
        # Generate and display report
        report = self.analyzer.generate_report(analysis)
        print("\n" + report)
        
        # Save results
        csv_file, json_file = self.analyzer.save_analysis(
            trends, analysis, "social_trends"
        )
        
        self.results['files'] = {
            'csv': csv_file,
            'json': json_file
        }
        
        return analysis
    
    def display_summary(self):
        """Display final summary"""
        trends = self.results['trends']
        analysis = self.results['analysis']
        files = self.results['files']
        
        print("\n🎉 ANALYSIS COMPLETE!")
        print("=" * 40)
        
        if trends:
            print(f"✅ Successfully collected {len(trends)} trends")
            
            if 'summary' in analysis:
                summary = analysis['summary']
                print(f"📊 Sources: {list(summary['sources'].keys())}")
                print(f"📈 Average score: {summary['average_score']:.1f}")
            
            if files.get('csv'):
                print(f"💾 Data saved: {files['csv']}")
            if files.get('json'):
                print(f"📄 Analysis saved: {files['json']}")
        else:
            print("❌ No data was collected")

def main():
    print("🚀 SOCIAL MEDIA & NEWS TREND ANALYZER")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SocialTrendAnalyzer()
    
    # Collect trends from all sources
    trends = analyzer.collect_all_trends()
    
    if trends:
        # Analyze and generate reports
        analyzer.analyze_and_report()
        
        # Display final summary
        analyzer.display_summary()
    else:
        print("❌ No trends were collected from any source")

if __name__ == "__main__":
    main()