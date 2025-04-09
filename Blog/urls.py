from django.urls import path
from .import views
from .views import home, article_detail, add_post, update_post, delete_post, add_category, CategoryPost, add_comment, update_profile, terms_of_service, cookie_policy, privacy_policy,like_post

urlpatterns = [
    #path('', views.home, name="home"), 
    path('', home, name="home"),
    path('article/<int:pk>', article_detail, name= "article-detail"),
    path('add_post/', add_post, name= "add_post"),
    path('add_category/', add_category, name= "add_category"),
    path('article/edit/<int:pk>', update_post, name='update_post'),
    path('article/<int:pk>/remove', delete_post, name='delete_post'),
    path('category/<str:cats>/' , CategoryPost, name='category'),
    path('article/<int:pk>/add_comment/', add_comment, name= "add_comment"),
    path('profile_pic/<int:pk>/', update_profile, name="profile_pic"),
    path("like/", like_post, name="like_post"),
    path('notifications/', views.notification_page, name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('terms/', terms_of_service, name='terms_of_service'),
    path('cookies/', cookie_policy, name='cookie_policy'),
    path('privacy/', privacy_policy, name='privacy_policy'),


]