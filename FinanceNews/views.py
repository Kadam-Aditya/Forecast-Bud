from django.shortcuts import render
from newsapi import NewsApiClient  # Removed NewsAPIException import
import requests

def index(request):
    newsapi = NewsApiClient(api_key=config("NEWS_API_KEY"))

    try:
        top = newsapi.get_top_headlines(sources='bbc-news', timeout=5)
    except requests.exceptions.RequestException as e:
        # Handle all kinds of request exceptions here
        print(f"Request error: {e}")
        top = {}

    my_articles = top.get('articles', [])
    news = []
    desc = []
    img = []

    for f in my_articles:
        news.append(f['title'])
        description = f.get('description', '')[:20]  # Limiting description to 20 words
        desc.append(description)
        img.append(f.get('urlToImage', ''))

    mylist = zip(news, desc, img)
    return render(request, 'Finance News/index.html', context={'mylist': mylist})
