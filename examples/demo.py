import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SocialTrendAnalyzer

def run_demo():
    """Run a demo of the social trend analyzer"""
    print("🎯 SOCIAL TREND ANALYZER - LIVE DEMO")
    print("=" * 50)
    
    analyzer = SocialTrendAnalyzer()
    
    print("Starting data collection...")
    trends = analyzer.collect_all_trends()
    
    if trends:
        print(f"✅ Collected {len(trends)} trends!")
        analysis = analyzer.analyze_and_report()
        
        # Show some interesting stats
        if analysis and 'summary' in analysis:
            summary = analysis['summary']
            print(f"\n📈 DEMO STATS:")
            print(f"   • Total trends: {summary['total_trends']}")
            print(f"   • Data sources: {len(summary['sources'])}")
            print(f"   • Categories: {len(summary.get('categories', {}))}")
    else:
        print("❌ No trends collected in demo")

if __name__ == "__main__":
    run_demo()