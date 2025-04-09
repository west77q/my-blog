from django.urls import path
from .views import UserRegistration, UserEditView, PasswordsChangeView, ShowProfilePage, EditProfilePage, CreateProfilePage,  activate_account, check_email
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/',UserRegistration.as_view(), name='register' ),
    path('edit_profile/',UserEditView.as_view(), name='edit_profile' ),
    path('password/',PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_success/', views.password_success, name="password_success"),
    path('<int:pk>/profile/', ShowProfilePage.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePage.as_view(), name='edit_profile_page'),
    path('Create_profile_page/', CreateProfilePage.as_view(), name='create_profile_page'),
    path('activate/<uuid:activation_code>/', activate_account, name='activate'),
    path('check_email/', check_email, name='check_email'),


]
