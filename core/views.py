from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Profile, Post, LikePost, Follow, Comment
from django.db.models import Q

@login_required
def home(request):

    liked_posts = LikePost.objects.filter(username=request.user.username).values_list('post_id', flat=True)
    posts = Post.objects.exclude(post_id__in=liked_posts)

    #user_suggestion
    user_following = Follow.objects.filter(follower=request.user.username).values_list('author', flat=True)
    all_users = User.objects.exclude(username=request.user.username)
    suggestion_list = all_users.exclude(username__in=user_following)

    context = {
        'suggestion_list' : suggestion_list,
        'posts' : posts,
    }

    return render(request, 'home.html', context)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, post_id=pk)
    post.delete()
    return redirect('home')

@login_required
def post_detail(request, pk):

    post = get_object_or_404(Post, post_id=pk)

    if request.method == "POST":
        author_profile = get_object_or_404(Profile, user=request.user)
        comment_content = request.POST.get('comment')

        new_comment = Comment.objects.create(post_id=post, author=author_profile, comment=comment_content)
        new_comment.save()

    post = Post.objects.get(post_id=pk)
    comments = Comment.objects.filter(post_id = post)
    print(comments)
    context = {
        'post' : post,
        'comments' : comments,
    }

    return render(request, 'post_detail.html', context)

def search(request):

    username = request.GET.get('username')

    if username:
        users = User.objects.filter(Q(username__icontains=username))
    else:
        users = User.objects.all()

    if username and not users.exists():
        users = User.objects.all()

    context = {
        'users' : users,
        'username' : username,
    }
    return render(request, 'search.html', context)

@login_required
def follow(request):
    if request.method == "POST":
        follower = request.POST.get('follower')
        author = request.POST.get('author')
 
        if Follow.objects.filter(follower=follower, author=author).first():
            delete_follower = Follow.objects.get(follower=follower, author=author)
            delete_follower.delete()
            return redirect('profile', author)
        elif follower == author:
            return redirect('profile', author)
        else:
            new_follower = Follow.objects.create(follower=follower, author=author)
            new_follower.save()
            return redirect('profile', author)

    else:
        return redirect('/')

@login_required
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        if request.FILES.get('image') is None:
            image = user_profile.pfp_image
        else:
            image = request.FILES.get('image')

        bio = request.POST.get('bio')
        location = request.POST.get('location')
        user_profile.bio = bio
        user_profile.pfp_image = image
        user_profile.location = location
        user_profile.save()
        return redirect('settings')

    context = {
        'user_profile' : user_profile,
    }
    return render(request, 'setting.html', context)

@login_required
def new_post(request):
    if request.method == "POST":
        post_image = request.FILES.get('post_image')
        caption = request.POST.get('caption')


        new_post = Post.objects.create(user=request.user, caption=caption, image=post_image)
        new_post.save()
        return redirect('home')
    
    return render(request, 'home.html')

@login_required
def like_post(request, pk):
    username = request.user.username
    post_id = pk

    post = Post.objects.get(post_id=pk)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username)

    if like_filter:
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        new_like = LikePost.objects.create(username=username, post_id=post_id)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))

def user_profile(request, username):
    user_object = User.objects.get(username=username)
    post_count = 0
    posts = Post.objects.filter(user=user_object)
    followers = Follow.objects.filter(author=username)
    if followers == None:
        followers = 0
    follower_count = followers.count()

    #user following count
    following = Follow.objects.filter(follower=username)
    if following == None:
        following_count = 0
    else:
        following_count = following.count()


    #follow unfollow button
    is_following = 0
    user = request.user
    check_follow = Follow.objects.filter(author=username, follower=user)
    if check_follow:
        is_following = 1
    else:
        is_following = 0

    post_count = posts.count()

    context = {
        'following_count' : following_count,
        'is_following' : is_following,
        'user_object' : user_object,
        'posts' : posts,
        'post_count' : post_count,
        'follower_count' : follower_count,
    }
    return render(request, 'profile.html', context)

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        get_by_username = User.objects.filter(username = username)
        get_by_email = User.objects.filter(email = email)

        if password1 != password2:
            messages.warning(request, "Password Doesn't Matching!")
            return redirect('signup')

        elif get_by_username.exists():
            messages.warning(request, "Username Already Exists! Try Another")
            return redirect('signup')

        elif get_by_email.exists():
            messages.warning(request, "Email Has Been Associated With Another Account! Try Logging In ")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        user_profile = Profile.objects.create(user=user, userid=user.id)
        user_profile.save()
        messages.success(request, "Account Created Successfully!")
        return redirect('signin')

    return render(request, 'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        valid_user = authenticate(username=username, password=password)

        if valid_user:
            login(request, valid_user)
            messages.success(request, 'Logged In Successfully!')
            return redirect('home')
        else:
            messages.warning(request, 'Invalid Credentials! Please Try Again')

    return render(request, 'signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('signin')