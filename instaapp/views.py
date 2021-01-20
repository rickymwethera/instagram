from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Image, Comment, Profile
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, UserCreationForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic import DetailView
from django.urls import reverse

# Create your views here.
@login_required(login_url='/accounts/register/')
def welcome(request):
    images= Image.objects.all()
    profile = Profile.objects.all()
    comments= Comment.objects.all()
    for image in images:
        print('image', image)

    
    return render(request, 'index.html', {"images":images,"comments":comments, "profile":profile})

@login_required
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
            savecomment.user = request.user.username
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

def like_post(request, pk):
    post = get_object_or_404(Image, id=pk)
    liked= False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('detail', args=[str(pk)]))

def follow_unfollow(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(name=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.name in my_profile.following.all():
            my_profile.following.remove(obj.name)
        else:
            my_profile.following.add(obj.name)
        return redirect(request.META.get('HTTP_REFERER')) 
    return redirect('explore')

def comment(request,id):
    current_user = request.user
    image = Image.get_single_photo(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.image_id = id
            comment.save()
        return redirect('index')

    else:
        form = CommentForm()
        return render(request,'instagram/add_comment.html',{"form":form,"image":image})

class ProfileDetailView(DetailView):
    model = Profile
    template = "profile_detail.html"
    #get user profile
    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    #get my profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(name=self.request.user)
        if view_profile.name in my_profile.following.all():
            follow = True
        else:
            follow =False
        context["follow"] = follow
        return context
    
