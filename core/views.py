from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.contrib import auth
# Create your views here.

def index(request):
    return render(request, 'index.html')

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

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect("signin")
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