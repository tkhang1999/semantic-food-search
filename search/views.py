from django.shortcuts import render
from django.apps import apps
from pysolr import SolrError

# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def search(request):
    query = request.GET.get('q') or ""
    top_results = request.GET.get('top') or "15"
    search_method = request.GET.get('method') or "bert"
    solr_error = ""

    results = None

    if query:
        try:
            results = apps.get_app_config('search').search_utils.search_reviews(query, top_results, search_method)
        except SolrError:
            solr_error = "Solr server may be loading at the moment, \
                please wait for a while and try loading the page again!"

    args = {
        'q': query,
        'top': top_results,
        'method': search_method,
        'results': results,
        'error': solr_error,
    }

    return render(request, 'search.html', args)


def about(request):
    return render(request, 'about.html', {})