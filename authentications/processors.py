from managements.models import Status
from reports.models import Post


def coordinates(request):
    try:
        map_posts = Post.objects.filter(post_status = 1)

        map_statuses = Status.objects.all()
    
    except:
        map_posts = None

        map_statuses = None

    context = {"map_posts": map_posts, "map_statuses": map_statuses}
    
    return (context)