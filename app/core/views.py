from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Core module active. Welcome to f5rugby.")