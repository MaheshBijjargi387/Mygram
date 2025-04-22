from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from Profile.models import*
# from Profile.models import*



def post_list(request):
    # Get the logged-in user
    profile_user = request.user

    # Initialize profile as None
    profile = None

    # Get profile image of the logged-in user if authenticated
    if request.user.is_authenticated:
        profile = ProfileImg.objects.filter(user=profile_user).first()

    # Fetch posts in descending order (latest post first)
    posts = Post.objects.all().order_by('-create_at')  # Make sure 'created_at' exists in your Post model

    # Fetch liked posts
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    return render(request, 'post/post_list.html', {
        'posts': posts, 
        'liked_post_ids': liked_post_ids,
        'profile': profile,
        'profile_user': profile_user,
    })



@login_required
def post_create(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        category_id = request.POST['category']
        tag_ids = request.POST.getlist('tags')
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id)

       
        post = Post.objects.create(
            title=title,
            content=content,
            image=image,
            category=category,
            user=request.user  
        )

        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)

        return redirect('post_list')

    return render(request, 'post/post_create.html', {'category': categories, 'tags': tags})


@login_required
def post_delete(request, id):
    get_object_or_404(Post, id=id).delete()
    return redirect('post_list')

@login_required
def update_post(request, id):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.category = Category.objects.get(id=request.POST['category'])
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        post.tags.clear()
        tag_ids = request.POST.getlist('tags')
        for tag_id in tag_ids:
            tag = Tag.objects.get(id=tag_id)
            post.tags.add(tag)
        post.save()
        return redirect('post_list')
    return render(request, 'post/update_post.html', {'categories': categories, 'tags': tags, "post": post})


def register_view(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'user already taken or exists ')
            return redirect('register')
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.save()
        messages.success(request, 'account createed successfully  ')
        return redirect('login_view')
    return render(request, 'post/register.html', )


def login_view(request):
    if request.method == "POST":
    
        username = request.POST['username']
        password = request.POST['password']
        # **credentials
        user = authenticate(request, username=username, password=password)
        if user :
            login(request,user)
            messages.success(request, 'login successfully  ')
            return redirect('post_list')
        else:
            messages.error(request, ' invalid credentials ')
            return redirect('login/')
            
    
    return render(request, 'post/login.html', )





@login_required
def logout_view(request):
    logout(request)
    messages.success(request, ' logout successfully ')
    return redirect('login_view')





@login_required 
def comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)  
    comments = Comment.objects.filter(post=post).order_by('-id')  
    count = Comment.objects.filter(post=post).count()
    if request.method == "POST":
        text = request.POST.get('text')

       
        Comment.objects.create(user=request.user, text=text, post=post)
        return redirect("comment", post_id=post.id)

    return render(request, 'post/comment.html', {'post': post, 'comments': comments,'count':count})
@login_required 
def only(request, id):
    onl = get_object_or_404(Post, id=id)
    liked_post_ids = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    like_count = Like.objects.filter(post=onl).count()  # 👉 Count likes for this post
    comments = Comment.objects.filter(post=onl).order_by('-id')
    comment_count = comments.count()

    return render(request, 'post/only.html', {
        'only': onl,
        'liked_post_ids': liked_post_ids,
        'comments': comments,
        'count': comment_count,
        'like_count': like_count,  # 👈 Pass to template
    })




@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_qs = Like.objects.filter(user=request.user, post=post)

    if like_qs.exists():
        like_qs.delete()  # Unlike
    else:
        Like.objects.create(user=request.user, post=post)  # Like

    return redirect(request.META.get('HTTP_REFERER', 'post_list'))




@login_required 
def search_view(request):
    # Fetch search query from GET request
    query = request.GET.get('q', '')

    # Filter posts based on the query
    results = Post.objects.filter(title__icontains=query)

    # Get the logged-in user
    profile_user = request.user

    # Get profile image of the logged-in user
    profile = None
    if request.user.is_authenticated:
        profile = ProfileImg.objects.filter(user=profile_user).first()

    context = {
        'query': query,
        'results': results,
        'post': Post.objects.all(),  
        'profile_user': profile_user,
        'profile': profile, 
        'profile_user': request.user,
    }

    return render(request, 'post/search.html', context)
