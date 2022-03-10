from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ProfileForm
from django.views.generic import UpdateView
from django.contrib import messages
from .models import Post


def blog(request):
    posts = Post.objects.all()
    posts = Post.objects.filter().order_by('-date_uploaded')
    return render(request, "blog/blog.html", {'posts': posts})


def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect("/")

@login_required(login_url='/login')
def upload_blog(request):
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            obj = form.instance
            alert = True
            return render(request, "blog/upload.html", {'obj': obj, 'alert': alert})
    else:
        form = PostForm()
    return render(request, "blog/upload.html", {'form': form})


class EditPost(UpdateView):
    model = Post
    template_name = 'blog/edit.html'
    fields = ['title', 'slug', 'content']


def user_profile(request, user_id):
    post = Post.objects.filter(id=user_id)
    return render(request, "blog/user.html", {'post': post})


def profile(request):
    return render(request, "blog/profile.html")


def update_profile(request):
    try:
        profiles = request.user.profile
    except Profile.DoesNotExist:
        profiles = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profiles)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "blog/update_profile.html", {'alert': alert})
    else:
        form = ProfileForm(instance=profiles)
    return render(request, "blog/update_profile.html", {'form': form})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first = request.POST['first']
        last = request.POST['last']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Error: passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password1)
        user.first = first
        user.last = last
        user.save()
        return render(request, 'blog/login.html')
    return render(request, "blog/register.html")


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You're logged in.")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'blog/blog.html')
    return render(request, "blog/login.html")


def Logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('/')