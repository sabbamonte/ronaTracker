from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import New_Post

def index(request):
    if request.method == "GET":
        all_posts = New_Post.objects.all()
        return render(request, "trackerapp/index.html", {"all_posts": all_posts})

    else:
        if not request.POST.get('diagnosis'):
            print(request.POST.get('diagnosis'))
            return render(request, "trackerapp/filter.html", {"message": "Please choose a diagnosis"})
        if not request.POST['city']:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a city"})
        if not request.POST['zip']:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a zip code"})
        if not request.POST['state']:
            return render(request, "trackerapp/filter.html", {"message": "Please choose a state"})

        new_post = New_Post()
        new_post.name = request.POST['name']
        new_post.post = request.POST['post']
        new_post.diagnosis = request.POST['diagnosis']  
        new_post.city = request.POST['city']
        new_post.zip = request.POST['zip']
        new_post.state = request.POST['state']
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
        

def filter(request):
    if request.method == "GET":
        search = request.GET['city']
        if not search:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a city"})
        state = request.GET['state']
        if not state or state == "Choose State...":
            return render(request, "trackerapp/filter.html", {"message": "Please choose a state"})

        all_cities = New_Post.objects.all()
        filter_list = []
        for city in all_cities:
            if search.casefold() == city.city.casefold() and state.casefold() == city.state.casefold():
                filter_list.append(city)
            
        return render(request, "trackerapp/filter.html", {"filter_list":filter_list, "search":search})

    