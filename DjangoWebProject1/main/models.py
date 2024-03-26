from random import randint
from typing import Any
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from tinymce.models import HTMLField
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone



User = get_user_model()




class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('main.Post', on_delete=models.CASCADE)
    reason = models.CharField(max_length=40, blank=True)
    comment_or_reply = models.ForeignKey('main.Comment', on_delete=models.CASCADE, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    steam_uid = models.CharField(max_length=40, blank=True)
    bio = HTMLField(blank=True)
    points = models.IntegerField(default=0) 
    last_seen = models.DateTimeField(default=timezone.now) 
    email_is_checked = models.BooleanField(default=False)
    profile_pic = ResizedImageField(size=[50, 80], quality=100, upload_to="authors", default='default.jpg', null=True, blank=True)

    notifications = models.ManyToManyField('Notifications', blank=True)

    def __str__(self):
        return self.fullname

    @property
    def num_posts(self):
        return Post.objects.filter(user=self).count()
    

    def is_online(self):
        now = timezone.now()
        fifteen_minutes_ago = now - timezone.timedelta(minutes=15)
        return self.last_seen >= fifteen_minutes_ago


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullname)
        super(Author, self).save(*args, **kwargs)
        

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    description = models.TextField(default="none")

    class Meta:
        verbose_name_plural = "categories"
    def __str__(self):
        return self.title
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse("posts", kwargs={
            "slug":self.slug
        })

    @property
    def num_posts(self):
        return Post.objects.filter(categories=self).count()
    
    @property
    def last_post(self):
        return Post.objects.filter(categories=self).latest("date")


class Reply(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:100]

    class Meta:
        verbose_name_plural = "replies"


class Comment(models.Model):
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = RichTextField()
    date = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField(Reply, blank=True)


    def __str__(self):
        return self.content[:100]

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = RichTextField()
    categories = models.ManyToManyField(Category, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    
    subscribers = models.ManyToManyField(
        User,
        blank=True,
        related_name="subscriptions",
        through="Subscription",
    )


    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    tags = TaggableManager(blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    closed = models.BooleanField(default=False)
    state = models.CharField(max_length=40, default="zero")
    
    def save(self, *args, **kwargs):
        posts = len(Post.objects.all())
        if not self.slug:
            self.slug = slugify(self.title + '_' + str(posts) + '_' + str(randint(1, 99999)))
        super(Post, self).save(*args, **kwargs)

    def subscribe(self, user):
        if user not in self.subscribers.all():
            self.subscribers.add(user)

            
    def unsubscribe(self, user):
        if user in self.subscribers.all():
            self.subscribers.remove(user)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("detail", kwargs={
            "slug":self.slug
        })

    @property
    def num_comments(self):
        return self.comments.count()
    
    @property
    def num_replies(self):
        return self.replies.count()

    @property
    def last_reply(self):
        return self.comments.latest("date")



class Subscription(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    


