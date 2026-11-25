from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .autocomplete import suggest
from .models import DrugInteraction
from .rules import validate_pair

# Create your views here.

def home(request):
    return render(request, 'home.html')

def check_interactions(request):
    interaction = None
    drug1 = ''
    drug2 = ''
    searched = False
    error = None

    #Post means that information is sent to the server
    if request.method == 'POST':
        drug1 = request.POST.get('drug1', '').strip()
        drug2 = request.POST.get('drug2', '').strip()
        searched = True

        #Business rules (BR-01, BR-02, BR-03) live in rules.py
        error = validate_pair(drug1, drug2)

        if error is None:
            interaction = DrugInteraction.objects.filter(Q(drug_a__iexact=drug1, drug_b__iexact=drug2) | Q(drug_a__iexact=drug2, drug_b__iexact=drug1)).first()

        #Return HTML page with results
    return render(request, 'check_interactions.html', {
        'interaction': interaction,
        'drug1': drug1,
        'drug2': drug2,
        'searched': searched,
        'error': error
    })

def search_drug(request):
    return render(request, 'search_drug.html')

def autocomplete(request):
    """Return drug-name suggestions for ?q=<text> as JSON."""
    query = request.GET.get('q', '')
    return JsonResponse({'query': query, 'suggestions': suggest(query)})
