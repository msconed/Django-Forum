from django.conf.urls import include
from django.urls import path
from .views import (
    home, detail, posts, create_post, latest_posts,
    search_result, profile_page, file_list, download_file, notifications_fn,)

urlpatterns = [
    path("", home, name="home"),
    path("detail/<slug>/", detail, name="detail"),
    path("posts/<slug>/", posts, name="posts"),
    path("<slug>/create_post/", create_post, name="create_post"),
    path("latest_posts", latest_posts, name="latest_posts"),
    path("search", search_result, name="search_result"),
    path("profile/", profile_page, name="profile_page"),
    path('submit-form/', detail, name='submit_form'),
    path('file-list/', file_list, name='file_list'),
    path('download-file/<str:file_name>/', download_file, name='download_file'),
    path('nt/', notifications_fn, name='nt'),

 #   path('steam-login/', steam_login, name='steam_login'),
 #   path('steam-auth/', steam_auth, name='steam_auth'),
 #   path('social-auth/', include('social_django.urls', namespace='social')),
]
