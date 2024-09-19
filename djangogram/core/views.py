import random
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

from .models import Profile, Post, LikePost, FollowersCount


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following = []
    feed = []

    user_following_found = FollowersCount.objects.filter(follower=request.user.username)
    for user in user_following_found:
        user_following.append(user.user)

    for username in user_following:
        feed_items = Post.objects.filter(user=username)
        feed.append(feed_items)

    posts = list(chain(*feed))

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following_found:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    suggestions = [x for x in list(new_suggestions) if (x not in list(current_user))]

    random.shuffle(suggestions)

    username_profiles = []
    username_profiles_filtered = []

    for users in suggestions:
        username_profiles.append(users.id)

    for ids in username_profiles:
        profiles_filtered = Profile.objects.filter(id_user=ids)
        username_profiles_filtered.append(profiles_filtered)

    profile_suggestions = list(chain(*username_profiles_filtered))

    return render(request, 'index.html', {'user_profile': user_profile,
                                          'posts': posts, 'profile_suggestions': profile_suggestions[:4]})


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        bio = request.POST['bio']
        location = request.POST['location']
        image = request.FILES.get('image', None)

        update_user_profile(user_profile, bio, location, image)

        return redirect('settings')

    return render(request, "settings.html", {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

    return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_num = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers_num = len(FollowersCount.objects.filter(user=pk))
    user_following_num = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_num': user_posts_num,
        'button_text': button_text,
        'user_followers_num': user_followers_num,
        'user_following_num': user_following_num
    }

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    existing_like = LikePost.objects.filter(post_id=post_id, username=username).first()

    if existing_like is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()

        post.likes_num += 1
        post.save()

    else:
        existing_like.delete()

        post.likes_num -= 1
        post.save()

    return redirect('/')


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()

        return redirect('/profile/' + user)


    else:
        return redirect('/')


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profiles = []
        username_profiles_filtered = []

        for user in username_object:
            username_profiles.append(user.id)

        for ids in username_profiles:
            profiles = Profile.objects.filter(id_user=ids)
            username_profiles_filtered.append(profiles)

        username_profiles_filtered = list(chain(*username_profiles_filtered))

        return render(request, 'search.html',
                      {'user_profile': user_profile, 'username_profiles': username_profiles_filtered})
    return redirect('/')


@login_required(login_url='signin')
def update_user_profile(user_profile, bio, location, image=None):
    """Helper function to update user profile."""
    user_profile.bio = bio
    user_profile.location = location
    if image is not None:
        user_profile.profile_img = image
    user_profile.save()


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


##FIX COOKIE SETTING ON LOGOUT
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
