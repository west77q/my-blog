from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Post,  Comment, Category, Profile, Notification
from .forms import PostForm, EditForm, CommentForm, UserProfileForm, CategorForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User




def notification_page(request):
    """Display notifications for the logged-in user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_notifications = notifications.filter(is_read=False)
    
    # Check if the related post or comment exists. If it doesn't, flag it as "removed."
    for notification in notifications:
        try:
            # Check if the related post or comment exists
            if notification.url:
                post_id = notification.url.split("/")[-1]  # Extract post_id from the URL
                post = Post.objects.get(id=post_id)  # Try to fetch the post
        except (Post.DoesNotExist, ValueError):  # Post doesn't exist or invalid URL
            notification.message += " (This post or comment no longer exists.)"
            notification.url = None  # Remove the URL from the notification
            notification.save()

    # Mark notifications as read when user accesses the notifications page
    notifications.update(is_read=True)

    return render(request, 'notification.html', {
        'notifications': notifications,
        'unread_notifications': unread_notifications
    })


def mark_as_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    
    # Check if the related post still exists before marking the notification as read
    try:
        # Check if the related post or comment exists
        if notification.url:
            post_id = notification.url.split("/")[-1]  # Extract post_id from the URL
            post = Post.objects.get(id=post_id)  # Try to fetch the post
    except (Post.DoesNotExist, ValueError):  # Post doesn't exist or invalid URL
        notification.message += " (This post or comment no longer exists.)"
        notification.save()

    # Mark the notification as read
    notification.is_read = True
    notification.save()

    return redirect('notifications')  # Redirect to notifications page



def like_post(request):
    if request.method == "POST" and request.user.is_authenticated:
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)  # Unlike
            liked = False
        else:
            post.likes.add(request.user)  # Like
            liked = True

            # Handle notifications
            if request.user != post.author:  # Ensure user isn't liking their own post
                post_author = post.author  # Get the post author
                message = f"Your post '{post.title}' has been liked by {request.user.username}."
                post_url = reverse('article-detail', args=[post.id])

                # Create a notification for the post author
                Notification.objects.create(user=post_author, message=message, url=post_url)

                print(f"A new like was added to post: {post.title} by {request.user.username}")

        return JsonResponse({"liked": liked, "like_count": post.likes.count()})
    
    return JsonResponse({"error": "Invalid request"}, status=400)
    



def home(request):
    posts = Post.objects.all().order_by('-post_date')
    cat_menu = Category.objects.all()
    return render(request, 'home.html', {
        'object_list': posts,
        'cat_menu': cat_menu,
    })


#This view displays posts belonging to a specific category.
def CategoryPost(request, cats):
    category_posts = Post.objects.filter(category=cats.title().replace('-', ' '))
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts}) 
    


def article_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    cat_menu = Category.objects.all()
    return render(request, 'article_detail.html', {
        'post': post,
        'cat_menu': cat_menu,
    })


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Send email notification to all authenticated users
            send_new_post_notification(post)

            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'add_post.html', {'form': form})


def send_new_post_notification(post):
    subject = f"New Post: {post.title}"
    message = f"A new post titled '{post.title}' has been published on the blog. Check it out at {settings.SITE_URL}."
    from_email = settings.EMAIL_HOST_USER

    # Get the email addresses of all authenticated users (active users)
    authenticated_users = User.objects.filter(is_active=True)
    recipient_list = [user.email for user in authenticated_users]

    # Send the email to all authenticated users
    send_mail(subject, message, from_email, recipient_list)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Or a specific category page
    else:
        form = CategorForm()
    return render(request, 'add_category.html', {'form': form})


@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('home')  # Prevent non-authors from editing the post

    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('article-detail', pk=post.pk)
    else:
        form = EditForm(instance=post)

    return render(request, 'update_post.html', {'form': form, 'post': post})




@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('article-detail', pk=post.pk)

    if request.method == 'POST':  # If the user confirms deletion
        post.delete()
        return redirect('home')

    return render(request, 'delete_post.html', {'post': post})  # Show confirmation page



@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('article-detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form, 'post': post})


@login_required
def update_profile(request):
    try:
        user_profile = request.user.Profile
    except Profile.DoesNotExist:
        user_profile = Profile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a profile page or wherever you want
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile_pic.html', {'form': form})    


def terms_of_service(request):
    return render(request, 'terms_of_service.html')


def cookie_policy(request):
    return render(request, 'cookie_policy.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


