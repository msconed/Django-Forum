from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from main.models import Author
from register.forms import UpdateForm
from django.contrib.auth import logout as lt
from django.contrib.auth.models import User
import random
import string
from .forms import UserRegistrationForm
from main.utils import authenticate_email


 # usernames = [user.username for user in User.objects.all()]


def generate_random_id():
    length = 15
    while True:
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        if not User.objects.filter(username=random_id).exists():
            return random_id

def create_author(request, user, username, user_id):

    author = Author(user=user, fullname=username, slug=user_id)
    author.save()

def register(request):
    form = UserRegistrationForm(request.POST or None)
    error = None
    if request.method == "POST":
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                error = 'Данный e-mail уже привязан к другому аккаунту.'
            if Author.objects.filter(fullname=form.cleaned_data['username']).exists():
                if error:
                    error = error + '\n' + 'Уже существует пользователь с таким ником.'
                else:
                    error = 'Уже существует пользователь с таким ником.'
            if not error:
                new_name = generate_random_id()
                username = form.cleaned_data['username']
                new_user = form.save()
                login(request, new_user)
               
                # Изменение username пользователя
                new_user.username = new_name
                new_user.save(update_fields=['username'])
                create_author(request, new_user, username, new_name)
                return redirect("home")
        
    context = {
        "form":form, 
        "title": "Регистрация | FORUM",
        'error': error,
    }
    return render(request, "register/signup.html", context)




def auth(request):
    form = AuthenticationForm(request, data=request.POST)
    error = None
    if request.method == "POST":
        if True:
            email = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate_email(email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error = 'Неверные данные.'
    context = {
        "form": form,
        "title": "Авторизация | FORUM",
        'error': error,
    }

    return render(request, "register/login.html", context)




@login_required
def update_profile(request):

    user = request.user
    form = UpdateForm(request.POST, request.FILES)
    print(request.POST)    
    print(request.FILES)
    if request.method == "POST":
        if form.is_valid():
            # Проверяем, есть ли созданный профиль для данного пользователя
            existing_profile = Author.objects.filter(user=user).first()
            if existing_profile:
                existing_profile.fullname = form.cleaned_data['fullname']
                existing_profile.bio = form.cleaned_data['bio']
                existing_profile.profile_pic = form.cleaned_data['profile_pic']
                existing_profile.save()
            else:
                update_profile = form.save(commit=False)
                update_profile.user = user
                update_profile.save()
                
            return redirect("home")

    context = {
        "form": form,
        "title": "Update Profile"
        
    }
    
    return render(request, "register/update.html", context)


@login_required
def logout(request):
    lt(request)
    return redirect("home")