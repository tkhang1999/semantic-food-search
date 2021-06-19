from django.shortcuts import render
from django.apps import apps

# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def search(request):
    query = request.GET.get('q') or ""
    top_results = request.GET.get('top') or "15"
    search_method = request.GET.get('method') or "bert"

    results = []

    if query:
        results = apps.get_app_config('search').search_utils.search_reviews(query, top_results, search_method)

    args = {
        'q': query,
        'top': top_results,
        'method': search_method,
        'results': results,
    }

    return render(request, 'search.html', args)


def contact(request):
    return render(request, 'contact.html', {})