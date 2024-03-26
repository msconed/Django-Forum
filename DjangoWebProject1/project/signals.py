from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Post, Notifications, Comment, Reply

@receiver(post_save, sender=Post)
def post_updated(sender, instance, **kwargs):
    subscribers = instance.subscribers.all()
    for subscriber in subscribers:
        Notifications.objects.create(
            user=subscriber,
            post=instance,
            comment_or_reply=None
        )

