from django.http import JsonResponse
from django.shortcuts import render

from .autocomplete import suggest

# Create your views here.

def home(request):
    return render(request, 'home.html')

def check_interactions(request):
    return render(request, 'check_interactions.html')

def search_drug(request):
    return render(request, 'search_drug.html')

def autocomplete(request):
    """Return drug-name suggestions for ?q=<text> as JSON."""
    query = request.GET.get('q', '')
    return JsonResponse({'query': query, 'suggestions': suggest(query)})
