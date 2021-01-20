from django.conf.urls import url
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseRedirect
urlpatterns=[
    path('',views.welcome,name = 'welcome'),
    path('post/new/',views.create_post,name='create'),
    url(r'^post/(\d+)',views.detail,name = 'detail'),
    path('profile/', views.profile, name='profile'),
    url(r'like/(\d+)',views.like_post,name = 'like'),
    path(r'post/(\d+)/comment',views.comment,name = 'comment'),
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)