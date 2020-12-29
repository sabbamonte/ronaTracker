from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import New_Post


def index(request):
    # Show all posts
    if request.method == "GET":
        all_posts = New_Post.objects.all()
        return render(request, "trackerapp/index.html", {"all_posts": all_posts})

    else:
        # Create new post and error check for blanks
        new_post = New_Post()
        if not request.POST['city']:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a city"})
        new_post.city = request.POST['city'].title()
        if request.POST['state'] == "Choose...":
            return render(request, "trackerapp/filter.html", {"message": "Please choose a state"})
        new_post.state = request.POST['state']
        if not request.POST['zip']:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a zip code"})
        new_post.zip = request.POST['zip']
        if not request.POST.get('diagnosis'):
            return render(request, "trackerapp/filter.html", {"message": "Please choose a diagnosis"})
        new_post.diagnosis = request.POST['diagnosis'] 
        new_post.name = request.POST['name']
        if not request.POST['post']:
            return render(request, "trackerapp/filter.html", {"message": "Please specify your latest movements"})
        new_post.post = request.POST['post']
        new_post.save()
        return HttpResponseRedirect(reverse("index"))  

def filter(request):

    # Get all posts and create empty list
    all_cities = New_Post.objects.all()
    filter_list = []

    # Error check for city and state search
    if request.method == "GET" and "city" in request.GET:
        state = request.GET['state']
        search = request.GET['city']
        if not search and not state:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a city"})
        if not state or state == "Choose State...":
            return render(request, "trackerapp/filter.html", {"message": "Please choose a state"})

    # Check if state, city and zip code entered match database and save in list
        if not search:
            # Only check state if city not entered
            for city in all_cities:
                if state.casefold() == city.state.casefold():
                    filter_list.append(city)
        else:
            for city in all_cities:
                if search.casefold() == city.city.casefold() and state.casefold() == city.state.casefold():
                    filter_list.append(city)
        return render(request, "trackerapp/filter.html", {"filter_list":filter_list, "search":search, "state":state})

    if request.method == "GET" and "zip" in request.GET:
        zip_code = request.GET['zip']
        if not request.GET['zip']:
            return render(request, "trackerapp/filter.html", {"message": "Please enter a zip code"})
        for city in all_cities:
            if int(zip_code) == city.zip:
                filter_list.append(city)
        return render(request, "trackerapp/filter.html", {"filter_list":filter_list, "state":zip_code})
        
    

    