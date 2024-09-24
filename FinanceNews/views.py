from django.shortcuts import render
from newsapi import NewsApiClient, NewsAPIException
from decouple import config
import requests

def index(request):
    # Set the default news source
    default_news_source = 'bbc-news'  # You can change this to any valid source

    # Get the news source from the request or use the default
    news_source = request.GET.get('news-source', default_news_source)

    newsapi = NewsApiClient(api_key=config("NEWS_API_KEY"))

    try:
        # Fetch news with a specified timeout (in seconds)
        top = newsapi.get_top_headlines(sources=news_source, timeout=15)
    except NewsAPIException as e:
        # Handle News API specific exceptions
        top = {}
        print(f"News API error: {e}")
    except requests.exceptions.Timeout:
        # Handle timeout error specifically
        top = {}
        print("Request timed out. Please try again later.")
    except requests.exceptions.RequestException as e:
        # Handle other network-related errors
        top = {}
        print(f"Request error: {e}")

    my_articles = top.get('articles', [])
    
    news = []
    desc = []
    img = []
    
    # Define the number of words you want for the description
    max_words_in_description = 20

    for i in range(len(my_articles)):
        f = my_articles[i]
        news.append(f['title'])
        
        # Check if the description is not None before splitting
        description = f.get('description', '')
        if description:
            # Split the description into words and take the first max_words_in_description words
            description_words = description.split()[:max_words_in_description]
            description = ' '.join(description_words)
        
        desc.append(description)
        
        img.append(f.get('urlToImage', ''))

    mylist = zip(news, desc, img)

    return render(request, 'Finance News/index.html', context={'mylist': mylist, 'selected_source': news_source})
