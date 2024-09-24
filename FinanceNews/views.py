from django.shortcuts import render
from newsapi import NewsApiClient
from decouple import config
import requests

def index(request):
    # Set the default news source
    default_news_source = 'Fortune'  # You can change this to any valid source

    # Get the news source from the request or use the default
    news_source = request.GET.get('news-source', default_news_source)

    newsapi = NewsApiClient(api_key=config("NEWS_API_KEY"))
    
    # Initialize the variables
    my_articles = []
    has_error = False  # A flag to track if there's an exception
    
    try:
        # Fetch news based on the selected source
        top = newsapi.get_top_headlines(sources=news_source)
        my_articles = top.get('articles', [])
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print(f"Request error: {e}")
        has_error = True  # Set the error flag to True
    
    news = []
    desc = []
    img = []
    
    # Define the number of words you want for the description
    max_words_in_description = 20

    for i in range(len(my_articles)):
        f = my_articles[i]
        news.append(f['title'])
        
        # Check if the description is not None before splitting
        description = f['description']
        if description:
            # Split the description into words and take the first max_words_in_description words
            description_words = description.split()[:max_words_in_description]
            description = ' '.join(description_words)
        else:
            description = ''  # Set an empty string if description is None
        
        desc.append(description)
        
        img.append(f['urlToImage'])

    mylist = zip(news, desc, img)

    # Pass the error flag to the template along with other context data
    return render(request, 'Finance News/index.html', context={
        'mylist': mylist,
        'selected_source': news_source,
        'has_error': has_error,  # Pass the error flag to the template
    })
