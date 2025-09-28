SCRAPING_CONFIG = {
    'request_timeout': 10,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'max_trends_per_source': 15,
    'delay_between_requests': 1
}

ANALYSIS_CONFIG = {
    'min_trend_score': 10,
    'top_trends_count': 5,
    'output_formats': ['csv', 'json']
}

SOURCES = {
    'news': ['BBC News', 'Reuters'],
    'social': ['GitHub', 'Twitter']
}