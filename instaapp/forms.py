from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:

        model = Image

        exclude = ['posted_date', 'author']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [
            "comment",
        ]

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "profile_picture",
            "bio",
        ]