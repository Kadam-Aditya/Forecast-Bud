from django.shortcuts import render
from newsapi import NewsApiClient
from decouple import config

def index(request):
    # Default news source is an empty string if not specified
    news_source = request.GET.get('news-source', "")

    newsapi = NewsApiClient(api_key=config("NEWS_API_KEY"))
    
    # Fetch news based on the selected source or from the business category
    if news_source:
        top = newsapi.get_top_headlines(sources=news_source)
    else:
        top = newsapi.get_top_headlines(category='business')

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

    return render(request, 'Finance News/index.html', context={'mylist': mylist, 'selected_source': news_source})
