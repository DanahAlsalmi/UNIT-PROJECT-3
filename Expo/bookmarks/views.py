from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from expos.models import *
from .models import *
# Create your views here.


def add_bookmark_view(request:HttpRequest, news_id):

    if not request.user.is_authenticated:
        return redirect("accounts:login_view")

    #add the favorite
    try:

        news = News.objects.get(id=news_id)

        user_bookmarked = Bookmark.objects.filter(user=request.user, news=News).first() #.first() bring the first Favorite object if exists else None
        
        if not user_bookmarked:
            new_bookmark = Bookmark(user=request.user, news=news)
            new_bookmark.save()
        else:
             user_bookmarked.delete()

        return redirect("expos:news_detail_view", news_id=news.id)
    except Exception as e:
        return redirect("main:home_view")
    


def my_bookmark_view(request: HttpRequest):

    bookmarks = Bookmark.objects.filter(user=request.user)

    return render(request, 'bookmarks/my_bookmark.html', {"bookmarks" : bookmarks})



