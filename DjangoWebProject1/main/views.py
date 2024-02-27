
from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, PostForm
from django.db.models import Count

def home(request):
    forums = Category.objects.all()
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = forums.count()
    num_comments = Comment.objects.count()
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
        "title": 'FORUM'
    }
    return render(request, "forums.html", context)

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm()
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    
    if "comment-form" in request.POST:
        comment = request.POST.get("comment")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)
        

    if "reply-form" in request.POST:
        reply = request.POST.get("reply")
        comment_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=comment_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply)
        comment_obj.replies.add(new_reply.id)

    if "close-topic" in request.POST:
        post.closed = True
        post.save()

    if "open-topic" in request.POST:
        post.closed = False
        post.save()
        
    user_comment_count = Comment.objects.filter(post=post).values('user').annotate(post_count=Count('post'), reply_count=Count('replies'), comment_count=Count('user'))


    context = {
        "post":post,
        "title": post.title + ' | ' + 'FORUM',
        'form': form,
        'user_comment_count': user_comment_count,
    }
    update_views(request, post)

    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    paginator = Paginator(posts, 5)
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
        "title": str(category) + ' | ' + 'FORUM'
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n its valid")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            form.save_m2m()
            return redirect("home")
    context.update({
        "form": form,
        "title": "Создать топик" + ' | ' + 'FORUM',
    })
    return render(request, "create_post.html", context)

def latest_posts(request):
    posts = Post.objects.all().filter(approved=True)[:10]
    context = {
        "posts":posts,
        "title": "Последние 10 топиков" + ' | ' + 'FORUM',
    }

    return render(request, "latest-posts.html", context)

def search_result(request):

    return render(request, "search.html")