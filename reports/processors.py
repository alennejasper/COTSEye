from reports.models import Post

def coordinates(request):
    try:
        posts = Post.objects.filter(post_status = 1)
    
    except:
        posts = None

    context = {"posts": posts}
    
    return (context)