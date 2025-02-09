from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from .models import Post,  Comment, Category, Profile, Like, Notification
from .forms import PostForm, EditForm, CommentForm, UserProfileForm, CategorForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
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




#Ensures that only authenticated users can access this view. If the user is not logged in, they are redirected to the login page.
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Retrieve the post object with the given post_id.

    # Check if the user has already liked the post
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        # If the user already has a like, toggle it
        like.like = not like.like
        like.save()
    else:
        # If the user has not liked yet, set it to True
        like.like = True
        like.save()

    # Handle notifications directly in the view
    if created and like.like and request.user != post.author:  # Check if it's a new like and not the post author liking their own post
        post_author = post.author  # Get the author of the post
        message = f"Your post '{post.title}' has been liked by {request.user.username}."
        post_url = reverse('article-detail', args=[post.id])

        # Create a notification for the post author
        Notification.objects.create(user=post_author, message=message,  url=post_url)

        print(f"A new like was added to post: {post.title} by {request.user.username}")

    return redirect('article-detail', pk=post.id)






class Home(ListView):
    model = Post 
    template_name = 'home.html'
    ordering = ['-post_date']


def  get_context_data(self, *args, **kwargs):
    cat_menu = Category.objects.all()
    context = super(Home, self).get_context_data(*args, **kwargs)
    context["cat_menu"] = cat_menu
    return context


#This view displays posts belonging to a specific category.
def CategoryPost(request, cats):
    category_posts = Post.objects.filter(category=cats.title().replace('-', ' '))
    return render(request, 'categories.html', {'cats':cats.title().replace('-', ' '), 'category_posts':category_posts}) 
    


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_detail.html'

    def  get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context




class AddPost(CreateView):
    model= Post
    form_class = PostForm
    queryset= Post.objects.all()
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')
    


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCategory(CreateView):
    model= Category
    form_class = CategorForm
    #queryset= Post.objects.all()
    template_name = 'add_category.html'
    #fields = '__all__'



class updatepost(UpdateView):
    model= Post
    form_class = EditForm
    queryset= Post.objects.all()
    template_name = 'update_post.html'
    #fields = '__all__'


class DeletePost(DeleteView):
     model= Post
     queryset= Post.objects.all()
     template_name = 'delete_post.html'
     success_url = reverse_lazy('home')



class AddComment(CreateView):
    model= Comment
    form_class = CommentForm
    queryset= Post.objects.all()
    template_name = 'add_comment.html'
    
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    success_url = reverse_lazy('home')



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


