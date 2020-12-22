from django.shortcuts import render
from django.http import HttpResponse
from .models import New_Post, Cities

def index(request):
    if request.method == "GET":
        return render(request, "trackerapp/index.html")
