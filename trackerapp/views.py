from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from collections import Counter
from django.core.paginator import Paginator
from datetime import datetime, timedelta 

from .models import New_Post


def index(request):
    # Get all posts that are not archived
    if request.method == "GET":
        all_posts = New_Post.objects.filter(is_archived=False).order_by('-timestamp')

        # Set date to be archived at 90 days from the post's timestamp
        expired = datetime.now().date() + timedelta(days=90)

        # Check if any posts need to be archived
        for post in all_posts:
            if (expired - post.timestamp).days == 1:
                post.is_archived = True
                post.save()
        
        # Use cleaned up posts for Pagination
        cleaned_all_posts = New_Post.objects.filter(is_archived=False).order_by('-timestamp')
        paginator = Paginator(cleaned_all_posts, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Make new list to add cities only from all the posts
        cities_only = []
        for post in all_posts:
            cities_only.append(post.city)

        # Find which city has the highest amount of posts and save count and city in variables
        highest_activity = dict(Counter(cities_only))
        max_count = max(highest_activity.values())
        max_city = max(highest_activity)

        # Get all posts where diagnosis is "Infected"
        all_infections = New_Post.objects.filter(diagnosis="Infected").order_by('-timestamp')

        # Make new list to add cities only from all posts where diagnosis is "Infected"
        infections_only = []
        for post in all_infections:
            infections_only.append(post.city)

        # Find the city with the highest rate of infections and save count and city in variables
        highest_infection = dict(Counter(infections_only))
        max_count_infection = max(highest_infection.values())
        max_city_infection = max(highest_infection)

        return render(request, "trackerapp/index.html", {"page_obj": page_obj, "max_count":max_count, "max_city":max_city, 
        "max_count_infection":max_count_infection, "max_city_infection": max_city_infection })

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
    all_cities = New_Post.objects.all().order_by('-timestamp')
    filter_list = []

    # Error check for city and state search
    if request.method == "GET" and "city" in request.GET:
        state = request.GET['state']
        search = request.GET['city']
        if not search and not state:
            return render(request, "trackerapp/filter.html", {"message": "Please type in a city"})
        if not state or state == "Choose State...":
            return render(request, "trackerapp/filter.html", {"message": "Please choose a state"})

    # Check if state, city and zip code entered match database and save in list created
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
        return render(request, "trackerapp/filter.html", {"filter_list":filter_list.sort(reverse=True), "state":zip_code})
        
    

    