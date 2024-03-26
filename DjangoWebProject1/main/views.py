import mimetypes
import os
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, PostForm
from django.db.models import Count
from django.http import HttpResponse
import hashlib
from social_django.models import UserSocialAuth
from django.contrib.auth.decorators import login_required
from main.models import Notifications
from register.forms import UpdateImageForm

def md5(fname):
    with open(fname, 'rb') as file:
        content = file.read()
        hash_value = hashlib.md5(content).hexdigest()
    return hash_value

def file_list(request):
    # Получить путь к базовому каталогу
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
    
    base_folder = os.path.dirname(os.path.dirname(base_dir))
    
    server_files_folder = "D:/arma mods/stalker"
    
    files = os.listdir(server_files_folder)
    
    # if request.user.is_authenticated:
    #     author = Author.objects.get(user=request.user)
    # else:
    #     author = ''

    files_with_md5 = {'files': []}



    for f in files:
        file_path = os.path.join(server_files_folder, f)
        if os.path.isfile(file_path):
            md5_hash = md5(file_path)
            files_with_md5['files'].append([f, md5_hash])
    
    return render(request, 'file_list.html', {'files': files_with_md5})

def download_file(request, file_name):
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
    base_folder = os.path.dirname(os.path.dirname(base_dir))
    
    server_files_folder = "D:/arma mods/stalker"
    
    file_path = os.path.join(server_files_folder, file_name)
    
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    
    return response

def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    num_comments = Comment.objects.count()

    try:
        author = Author.objects.get(user=request.user)
    except:
        author = ''
    
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = []

    context = {
        "forums":forums,
        'num_comments':num_comments + num_posts,
        "num_posts":num_posts,
        "num_users":num_users,
        "num_categories":num_categories,
        "last_post":last_post,
        "title": 'FORUM',
        "author": author
    }
    return render(request, "forums.html", context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm()
    if "delete-topic" in request.POST:
        post.delete()
        return redirect('http://127.0.0.1:8000/')
    
    try:
        author = Author.objects.get(user=request.user)
    except:
        author = ''
    
    if "comment-form" in request.POST and post.closed != True:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST and post.closed != True:
        reply = request.POST.get("reply")
        comment_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=comment_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)
    
    if "close-topic" in request.POST:
        post.closed = True
        post.save()
        #post.subscribe(user=request.user)
        

    if "open-topic" in request.POST:
        post.closed = False
        post.save()
        #post.unsubscribe(user=request.user)
        
    if "delete-message" in request.POST:
        message_id = request.POST.get("message-id")
        message = Comment.objects.get(id=message_id)
        for reply in message.replies.all():
            reply.delete()
        message.delete()

    if "delete-reply" in request.POST:
        reply_id = request.POST.get("reply-id")
        reply = Reply.objects.get(id=reply_id)
        reply.delete()


    user_comment_count = Comment.objects.filter(post=post).values('user').annotate(post_count=Count('post'), reply_count=Count('replies'), comment_count=Count('user'))

    if "subscribe" in request.POST:
        check = request.POST.get("subscribe")
        if check == "True":
            post.subscribe(request.user)
        else:
            post.unsubscribe(request.user)


    

    context = {
        "post":post,
        "title": post.title + ' | ' + 'FORUM',
        'form': form,
        'user_comment_count': user_comment_count,
        "author": author,
        'subs': post.subscribers.all(),
    }
    update_views(request, post)

    return render(request, "detail.html", context)




@login_required
def notifications_fn(request):
    notifications = Notifications.objects.filter(user=request.user).order_by('-date_created')
    for notification in notifications:
        notification.is_read = True
        notification.save()

    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications.html', context)



def posts(request, slug):
    try:
        author = Author.objects.get(user=request.user)
    except:
        author = ''

    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    paginator = Paginator(posts, 10)
    page = request.GET.get("page")
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 

    context = {
        "posts":posts,
        "forum": category,
        "title": str(category) + ' | ' + 'FORUM',
        "author": author,
        'posts_count': len(posts)
    }

    return render(request, "posts.html", context)



def create_post(request, slug):
    context = {}
    form = PostForm(request.POST or None)
    category = get_object_or_404(Category, slug=slug)

    try:
        author = Author.objects.get(user=request.user)
    except:
        author = ''

    if request.method == "POST":
        content = request.POST.get("content")
        title = request.POST.get("title")
        if title != '' and content != '':
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.title = form.cleaned_data.get('title')
            new_post.content = form.cleaned_data.get('content')
            new_post.save()
            form.save_m2m()
            new_post.categories.add(category.id)
            return redirect("home")

    context.update({
        "form": form,
        "title": "Создать топик" + ' | ' + 'FORUM',
        "author": author,
        'category': category,
        'slug': slug,
        'request': request,

    })

    return render(request, "create_post.html", context)

    context.update({
        "form": form,
        "title": "Создать топик" + ' | ' + 'FORUM',
        "author": author,
        'category': category,
        'slug': slug,
        'request': request
    })

    return render(request, "create_post.html", context)

def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    try:
        author = Author.objects.get(user=request.user)
    except:
        author = ''
    context = {
        "posts":posts,
        "title": "Последние 10 топиков" + ' | ' + 'FORUM',
        "author": author
    }

    return render(request, "latest-posts.html", context)

def search_result(request):
    try:
        author = Author.objects.get(user=request.user)
    except:
        author = ''

    context = {
        "author": author
    }

    return render(request, "search.html", context)


@login_required
def profile_page(request):
    posts = Post.objects.filter(approved=True)
    
    author = Author.objects.get(user=request.user)
    form = UpdateImageForm(request.POST or None, request.FILES)
    
    
    if "update-image" in request.POST:
        if form.is_valid():
                author.profile_pic = form.cleaned_data['profile_pic']
                author.save()
        
    context = {
        "author": author,
        'posts': posts,
        'form': form,
    }

    return render(request, "profile.html", context)


def steam_callback(request):
    user = request.user
    steam_user = UserSocialAuth.objects.get(user=user, provider='steam')
    steam_id = steam_user.uid
    print(steam_user)
    print(steam_id)
    # Делайте что-то с steam_id



