from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def check_interactions(request):
    return render(request, 'check_interactions.html')

def search_drug(request):
    return render(request, 'search_drug.html')