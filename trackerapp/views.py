from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from .models import New_Post

def index(request):
    if request.method == "GET":
        all_posts = New_Post.objects.all()
        return render(request, "trackerapp/index.html", {"all_posts": all_posts})
    else:
        new_post = New_Post()
        new_post.name = request.POST['name']
        new_post.post = request.POST['post']
        new_post.diagnosis = request.POST['diagnosis']
        new_post.city = request.POST['city']
        new_post.zip = request.POST['zip']
        new_post.state = request.POST['state']
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
