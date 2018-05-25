from django.shortcuts import render, redirect
from apps.login_app.models import *
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'login_app/index.html')

def log_reg(request):
    #picking the function
    if "confirm" in request.POST:
        response = User.objects.register_user(request.POST)
    else:
        response = User.objects.login_user(request.POST)

    if len(response["errors"]) > 0:
        for error in response['errors']:
            messages.error(request, error)
        # redirect the user back to the form to fix the errors
        return redirect(reverse('login:index'))
    else:
        messages.success(request, "You have successfully logged in!")
        request.session["status"] = "logged_in"
        request.session['user_id'] = response["user_id"]
        return redirect(reverse('login:dashboard'))

def dashboard(request):
    if request.session["status"] != "logged_in":
        messages.error(request, "You must be logged in to access the site")
        return redirect(reverse('login:index'))
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "posts": Post.objects.filter(poster=User.objects.get(id=request.session["user_id"]))
    }
    return render(request, 'login_app/dashboard.html', context)

# def fb_login(request):
#     print(request.POST)
#     return

def add_post(request):
    Post.objects.create(poster = User.objects.get(id=request.session["user_id"]), title=request.POST["title"], location=request.POST["location"], content=request.POST["content"])
    return redirect(reverse('login:dashboard'))

def show(request, post_id):
    context = {
        "post" : Post.objects.get(id=post_id),
        "user" : Post.objects.get(id=post_id).poster,
        "comments": Comment.objects.filter(post_id=post_id)
    }
    return render(request, 'login_app/show.html', context)

def logout(request):
    request.session["status"] = "logged_out"
    messages.error(request, "You have been logged out.")
    return redirect(reverse('login:index'))

def reply(request, post_id):
    Comment.objects.create(post_id=Post.objects.get(id=post_id), user_id=User.objects.get(id=request.session["user_id"]), content=request.POST["reply"])
    return redirect(reverse('login:show', kwargs={'post_id': post_id}))

def profile(request, id):
    context = {
    "user": User.objects.get(id=id),
    "posts": Post.objects.filter(poster=User.objects.get(id=id))
    }
    return render(request, "login_app/profile_page.html", context)
