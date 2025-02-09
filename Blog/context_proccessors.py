from .models import Category
from. models import Notification





def navbar_context(request):

    return { 'cat_menu': Category.objects.all(), }




def notifications(request):
    if request.user.is_authenticated:
        # fetch unread notifications for the logged in user
        unread_notifications =Notification.objects.filter(user=request.user, is_read=False)
        all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

        return{

            'unread_notifications' : unread_notifications, #unread notifications for badge
            'all_notifications' : all_notifications, # all notification to show in dropdown
        }
    return{}
    