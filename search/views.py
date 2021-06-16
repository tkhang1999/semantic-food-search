from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html', {})


def search(request):
    query = request.GET.get('q')
    results = [
        "Good food",
        "Awesome food"
    ]

    args = {
        'q': query,
        'results': results,
    }

    return render(request, 'search.html', args)