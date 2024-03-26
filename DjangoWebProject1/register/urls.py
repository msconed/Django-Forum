from django.urls import path
from .views import register, auth, update_profile, logout

urlpatterns = [
    path("register/", register, name="register"),
    path("auth/", auth, name="auth"),
    path("update_profile/", update_profile, name="update_profile"),
    path("logout/", logout, name="logout"),
]