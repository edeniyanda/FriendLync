from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

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
                messages.info.exists(request, "Username Already Taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=confirmpassword)
                user.save()
        else:
            messages.info(request, "Password doesn't Match")
            return redirect("signup")
    else:
        return render(request, "signup.html")