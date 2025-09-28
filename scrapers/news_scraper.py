import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

class NewsScraper:
    def __init__(self):
        self.sources = {
            'BBC News': 'https://www.bbc.com/news',
            'Reuters': 'https://www.reuters.com/'
        }
    
    def scrape_bbc_news(self):
        """Scrape BBC News headlines"""
        trends = []
        try:
            url = "https://www.bbc.com/news"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for headlines with multiple selectors
            selectors = [
                'h1', 'h2', 'h3',
                '[data-testid="card-headline"]',
                '.gs-c-promo-heading',
                '.sc-49c1fbfc-1'
            ]
            
            for selector in selectors:
                headlines = soup.select(selector)
                for i, headline in enumerate(headlines[:10]):
                    text = headline.get_text(strip=True)
                    if text and len(text) > 15:
                        trends.append({
                            'platform': 'BBC News',
                            'title': text,
                            'rank': len(trends) + 1,
                            'score': 100 - len(trends) * 5,
                            'url': url,
                            'timestamp': datetime.now(),
                            'category': 'News'
                        })
                if trends:
                    break
            
            print(f"✅ BBC News: Found {len(trends)} headlines")
            
        except Exception as e:
            print(f"❌ BBC News error: {e}")
            
        return trends
    
    def scrape_reuters(self):
        """Scrape Reuters News"""
        trends = []
        try:
            url = "https://www.reuters.com/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for Reuters headlines
            headlines = soup.find_all(['h1', 'h2', 'h3', 'a'], class_=True)
            
            for i, headline in enumerate(headlines):
                if len(trends) >= 8:
                    break
                    
                text = headline.get_text(strip=True)
                if text and len(text) > 20 and not any(word in text.lower() for word in ['subscribe', 'login', 'sign up']):
                    trends.append({
                        'platform': 'Reuters',
                        'title': text[:150] + '...' if len(text) > 150 else text,
                        'rank': len(trends) + 1,
                        'score': 90 - len(trends) * 8,
                        'url': url,
                        'timestamp': datetime.now(),
                        'category': 'News'
                    })
            
            print(f"✅ Reuters: Found {len(trends)} articles")
            
        except Exception as e:
            print(f"❌ Reuters error: {e}")
            
        return trends
    
    def scrape_all_news(self):
        """Scrape from all news sources"""
        all_trends = []
        
        print("📰 Scraping news headlines...")
        all_trends.extend(self.scrape_bbc_news())
        time.sleep(1)  # Be respectful
        all_trends.extend(self.scrape_reuters())
        
        return all_trends