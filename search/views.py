from django.shortcuts import render

import pysolr
import os

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
        'results': results,
    }

    return render(request, 'search.html', args)