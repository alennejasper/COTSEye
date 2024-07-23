from managements.models import Status
from reports.models import Post
from datetime import timedelta
from django.utils import timezone

def coordinates(request):
    try:
        six_months_ago = timezone.now() - timedelta(days = 180) 

        map_posts = Post.objects.filter(creation_date__gte = six_months_ago)

        map_statuses = Status.objects.filter(creation_date__gte = six_months_ago)
    
    except:
        map_posts = None

        map_statuses = None

    context = {"map_posts": map_posts, "map_statuses": map_statuses}
    
    return (context)