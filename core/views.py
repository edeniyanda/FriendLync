from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .models import Profile, Post, LikePost
from django.contrib.auth.decorators import login_required


@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    feed_list = Post.objects.all()
    # for post in feed_list:
    #     post_user_profile = Profile.objects.get(user=post.user)
    #     post_user_img_url = print(post_user_profile.profile_img.url)
    return render(request, 'index.html', {
        "user_profile" : user_profile,
        "posts" : feed_list                                                         
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
    if request.method == "POST":
        user= request.user.username
        image = request.FILES.get("image_upload")
        caption = request.POST["caption"]

        new_post = Post.objects.create(user=user, image=image, caption=caption)

        new_post.save()
        return redirect("home_page")
    return redirect("home_page")

@login_required
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if not like_filter:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()

        return redirect("home_page")
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1 if post.no_of_likes != 0 else 0
        post.save()
        return redirect("home_page")

@login_required
def profile(request, pk):
    return render(request, "profile.html")