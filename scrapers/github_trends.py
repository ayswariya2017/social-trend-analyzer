import requests
from bs4 import BeautifulSoup
from datetime import datetime

class GitHubTrends:
    def get_trending_repositories(self):
        """Get trending GitHub repositories"""
        trends = []
        try:
            url = "https://github.com/trending"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find repository containers
            repos = soup.find_all('article', class_='Box-row')
            
            for i, repo in enumerate(repos[:10]):
                try:
                    # Extract repo name
                    title_elem = repo.find('h2')
                    if title_elem:
                        title = title_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
                        
                        # Extract description
                        desc_elem = repo.find('p')
                        description = desc_elem.get_text(strip=True) if desc_elem else "No description"
                        
                        trends.append({
                            'platform': 'GitHub',
                            'title': f"Trending: {title}",
                            'description': description,
                            'rank': i + 1,
                            'score': 100 - i * 8,
                            'url': f"https://github.com/{title}",
                            'timestamp': datetime.now(),
                            'category': 'Technology'
                        })
                        
                except Exception as e:
                    continue
            
            print(f"✅ GitHub: Found {len(trends)} trending repositories")
            
        except Exception as e:
            print(f"❌ GitHub error: {e}")
            # Return sample data if scraping fails
            trends = self.get_sample_github_data()
            
        return trends
    
    def get_sample_github_data(self):
        """Return sample GitHub data if scraping fails"""
        sample_repos = [
            "facebook/react", "microsoft/vscode", "torvalds/linux",
            "python/cpython", "pytorch/pytorch", "tensorflow/tensorflow",
            "vercel/next.js", "nodejs/node", "docker/docker-ce", "kubernetes/kubernetes"
        ]
        
        trends = []
        for i, repo in enumerate(sample_repos):
            trends.append({
                'platform': 'GitHub',
                'title': f"Trending: {repo}",
                'description': f"Popular {repo.split('/')[0]} repository",
                'rank': i + 1,
                'score': 100 - i * 8,
                'url': f"https://github.com/{repo}",
                'timestamp': datetime.now(),
                'category': 'Technology'
            })
        
        print("✅ GitHub: Using sample trending data")
        return trends