from django.shortcuts import render

import pysolr
import os

# Solr requires java to work, so we need to install java on heroku
# i.e. heroku buildpacks:add heroku/jvm

# start Solr server in background
os.system("./solr-7.7.3/bin/solr start")

# connect to the solr server
SOLR_BERT_URL = 'http://localhost:8983/solr/bert'
SOLR = pysolr.Solr(SOLR_BERT_URL)

# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def search(request):
    query = request.GET.get('q') or ""
    top_results = request.GET.get('top') or "15"
    search_method = request.GET.get('method') or "be"

    results = []

    if query:
        query_search = "text: (%s)" % (query)
        fl_search = "text,score"
        reviews_count = 500

        search_results = SOLR.search(query_search, **{
            'fl': fl_search
        }, rows=reviews_count)
        results = [{'text': result['text'][0], 'score': result['score']} for result in search_results]

        # print(results)

    args = {
        'q': query,
        'top': top_results,
        'method': search_method,
        'results': results,
    }

    return render(request, 'search.html', args)