from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from Profile.models import*




@login_required
def profile_image(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if image:
          
            ProfileImg.objects.update_or_create(
                user=request.user,
                defaults={'image': image}
            )
            return redirect('user_profile_image')  
    return render(request, 'profile/profile.html')

@login_required
def user_profile_image(request, username):
    user = get_object_or_404(User, username=username) 
    posts = Post.objects.filter(user=user)  
    profile = ProfileImg.objects.filter(user=user).first()

   
    followers_count = user.followers_set.count()
    following_count = user.following_set.count()

   
    is_following = False
    if request.user.is_authenticated:
        is_following = Following.objects.filter(follower=request.user, following=user).exists()

    return render(request, 'profile/show_profile.html', {
        'profile_user': user,
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'posts': posts,
    })


@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if request.user != target_user:
        already_following = Following.objects.filter(follower=request.user, following=target_user).exists()
        if not already_following:
            Following.objects.create(follower=request.user, following=target_user)

    return redirect('user_profile_image', username=target_user.username)


@login_required
def unfollow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    Following.objects.filter(follower=request.user, following=target_user).delete()

    return redirect('user_profile_image', username=target_user.username)


