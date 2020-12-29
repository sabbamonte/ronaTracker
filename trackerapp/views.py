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
        new_post.post = request.POST['post']
        new_post.save()
        return HttpResponseRedirect(reverse("index"))  

def filter(request):

    # Show all posts in a list depending on the city and state entered by user
    if request.method == "GET":
        search = request.GET['city']
        if not search:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a city"})
        state = request.GET['state']
        if not state or state == "Choose State...":
            return render(request, "trackerapp/filter.html", {"message": "Please choose a state"})

        # Check if state and city entered match database and save in a list
        all_cities = New_Post.objects.all()
        filter_list = []
        for city in all_cities:
            if search.casefold() == city.city.casefold() and state.casefold() == city.state.casefold():
                filter_list.append(city)
            
        return render(request, "trackerapp/filter.html", {"filter_list":filter_list, "search":search})

    