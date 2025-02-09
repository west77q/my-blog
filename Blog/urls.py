from django.urls import path
from .import views
from .views import Home, ArticleDetailView, AddPost, updatepost, DeletePost, AddCategory, CategoryPost, AddComment, update_profile

urlpatterns = [
    #path('', views.home, name="home"), 
    path('', Home.as_view(), name="home"),
    path('article/<int:pk>', ArticleDetailView.as_view(), name= "article-detail"),
    path('add_post/', AddPost.as_view(), name= "add_post"),
    path('add_category/', AddCategory.as_view(), name= "add_category"),
    path('article/edit/<int:pk>', updatepost.as_view(), name='update_post'),
    path('article/<int:pk>/remove', DeletePost.as_view(), name='delete_post'),
    path('category/<str:cats>/' , CategoryPost, name='category'),
    path('article/<int:pk>/add_comment/', AddComment.as_view(), name= "add_comment"),
    path('profile_pic/<int:pk>/', update_profile, name="profile_pic"),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('notifications/', views.notification_page, name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    


]