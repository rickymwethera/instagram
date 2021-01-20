from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Image, Comment, Profile
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, UserCreationForm, ProfileUpdateForm
from django.contrib import messages

# Create your views here.
def welcome(request):
    images= Image.objects.all()
    profile = Profile.objects.all()
    comments= Comment.objects.all()
    for image in images:
        print('image', image)

    
    return render(request, 'index.html', {"images":images,"comments":comments, "profile":profile})


def create_post(request):
    current_user = request.user
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            add=form.save(commit=False)
            # current_user = Profile.objects.get(name=request.user)
            # add.author = current_user
            add.save()
        return redirect('welcome')
    else:

        context = {'form':form}
        return render(request,'image_form.html',context)


def detail(request,post_id):
   
    image = Image.objects.get(id=post_id)
    pic = get_object_or_404(Image, pk=post_id)
    total_likes = pic.total_likes()
    liked = False
    if pic.likes.filter(id=request.user.id).exists():
        liked=True

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.image = pic
            savecomment.user = request.user.profile
            savecomment.save()
            return redirect('index')
    else:
        form = CommentForm()
    params = {
        'image': image,
        'pic':pic,
        'form': form,
        'total_likes':total_likes,
        'liked':liked}

    return render(request,"post_detail.html", params)


def profile(request):
    current_user=request.user
    profile_info = Profile.objects.filter(user=current_user).first()
    posts =  request.user.image_set.all()
    return render(request,'registration/profile.html',{"images":posts,"profile":profile_info,"current_user":current_user})

def edit_profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
        return redirect('profile')

    else:
        form = ProfileUpdateForm()
        return render(request,'registration/edit_profile.html',{"form":form})