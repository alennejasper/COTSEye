from managements.models import Status
from reports.models import Post


def coordinates(request):
    try:
        posts = Post.objects.filter(post_status = 1)

        statuses = Status.objects.all()
    
    except:
        posts = None

        statuses = None

    context = {"posts": posts, "statuses": statuses}
    
    return (context)