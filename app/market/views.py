from django.shortcuts import render

def index(request):
    context = {}
    return render(request, "market/index.html", context)