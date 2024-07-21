from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Profile, Post
from django.contrib.auth.decorators import login_required


@login_required(login_url="signin")
def index(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'index.html', {
        "user_profile" : user_profile
    })

def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password1"]
        confirmpassword = request.POST["password2"]

        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Taken")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=confirmpassword)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect("settings")
        else:
            messages.info(request, "Password doesn't Match")
            return redirect("signup")
    else:
        return render(request, "signup.html")
   
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect("/")
        messages.info(request, "Invalid Username or Password")
        return redirect("signin")
    return render(request, "signin.html")

@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get("Image") is None:
            image = user_profile.profile_img
            bio = request.POST['about'] 
            location = request.POST['location'] 

            user_profile.profile_img = image
            user_profile.bio = bio 
            user_profile.location = location

            user_profile.save()
            return redirect("settings")
        
        if request.FILES.get("Image"):
            image = request.FILES.get("Image")

            bio = request.POST['about'] 
            location = request.POST['location'] 

            user_profile.profile_img = image
            user_profile.bio = bio 
            user_profile.location = location

            user_profile.save()
            return redirect("settings")
        
    return render(request, "setting.html", {
        "user_profile" : user_profile
    })

@login_required
def upload(request):
    print("I made it here")
    if request.method == "POST":
        user= request.user.username
        image = request.FILES.get("image_uplod")
        caption = request.POST["caption"]

        new_post = Post.objects.create(user=user, image=image, caption=caption)

        new_post.save()
        print("And I saved the Data")
        return redirect("home_page")
    return redirect("home_page")