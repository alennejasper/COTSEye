from reports.models import PostStatus, Post

def coordinates(request):
    try:
        posts = Post.objects.filter(id = 1)
    
    except:
        posts = None

    context = {"posts": posts}
    return (context)