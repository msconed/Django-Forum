from django.utils import timezone
from .models import Author

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                author = Author.objects.get(user=request.user)
                author.last_seen = timezone.now()
                author.save()
            except:
                pass
        return response

