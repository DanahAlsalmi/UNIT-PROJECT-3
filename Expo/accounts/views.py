from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Profile

# Create your views here.


def register_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            #create a new user
            user = User.objects.create_user(username=request.POST["username"], first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=request.POST["password"])
            user.save()

            user_profile = Profile(user=user)
            user_profile.save()

            return redirect("accounts:login_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/register.html", {"msg" : msg})

def login_view(request: HttpRequest):
    msg = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            login(request, user)
            return redirect("main:home_view")
        else:
            msg = "Please provide correct username and password"

    return render(request, "accounts/login.html", {"msg" : msg})

def logout_view(request: HttpRequest):

    if request.user.is_authenticated:
        logout(request)    

    return redirect("accounts:login_view")

def update_user_view(request: HttpRequest):
    msg = None

    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                user : User = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                try:
                    profile : Profile = request.user.profile
                except Exception as e:
                    profile = Profile(user=user, birth_date=request.POST["birth_date"] , job=request.POST["job"])
                    profile.save()

                profile.birth_date = request.POST["birth_date"]
                profile.job = request.POST["job"]

                if 'avatar' in request.FILES: profile.avatar = request.FILES["avatar"]
                profile.save()

                return redirect("accounts:user_profile_view", user_id = request.user.id)

            else:
                return redirect("accounts:login_view")
        except IntegrityError as e:
            msg = f"Please select another username"
        except Exception as e:
            msg = f"something went wrong {e}"

    return render(request, "accounts/update.html", {"msg" : msg})

def user_profile_view(request: HttpRequest, user_id):

    try:
        user = User.objects.get(id=user_id)

    except:
        return render(request, 'main/not_found.html')
    return render(request, 'accounts/profile.html', {"user":user})