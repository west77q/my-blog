from django.urls import path
from .views import  user_edit, password_change, show_profile_page, edit_profile_page, create_profile_page, password_success, user_registration, activate_account, check_email
from django.contrib.auth import views as auth_views
from . import views 


urlpatterns = [
    path('register/', user_registration, name='register'),
    path('edit_profile/', user_edit, name='edit_profile'),
    path('password/', password_change, name='registration/change-password.html'),
    path('password_success/', password_success, name="password_success"),
    path('<int:pk>/profile/', show_profile_page, name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', edit_profile_page, name='edit_profile_page'),
    path('Create_profile_page/', create_profile_page, name='create_profile_page'),
    path('activate/<uuid:activation_code>/', activate_account, name='activate'),
    path('check-email/', check_email, name='check_email'),


]
