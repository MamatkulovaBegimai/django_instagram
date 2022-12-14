from django.shortcuts import render, redirect
from posts.models import Post, Comments

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-id')
    context = {
        'posts' : posts
    }
    return render(request, 'index.html', context)

def single_post(request, id):
    post = Post.objects.get(id = id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            post.delete()
            return redirect('index')
        if 'comment' in request.POST:
            text = request.POST.get('text')
            comment = Comments.objects.create(text = text, user = request.user, post = post)
            comment.save()
            return redirect('single_post', post.id)
        
    context = {
        'post':post
    }
    return render(request, 'comment.html', context)

def create_post(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        user = request.user
        post = Post.objects.create(title = title, description = description, image = image, user = user)
        post.save()
        return redirect('index')
    return render(request, 'create_post.html')

def update_post(request,id):
    user = request.user
    post = Post.objects.get(id = id)
    if post.user == user:
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            user = request.user
            post = Post.objects.get(id = id)
            post.title = title
            post.description = description
            post.image = image
            post.user = user
            post.save()
            return redirect('index')
    else:
        return redirect('index')
    return render(request, 'update_post.html')

