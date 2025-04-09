from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import logging
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm, PasswordChangingForm, ProfilePageForm
from Blog.models import Profile
from django.contrib import messages
from .forms import UserChangeForm
import uuid






@login_required
def create_profile_page(request):
    if request.method == 'POST':
        form = ProfilePageForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')  # Redirect to home or any page you want
    else:
        form = ProfilePageForm()

    return render(request, 'registration/Create_user_profile_page.html', {'form': form,})



@login_required
def edit_profile_page(request, pk):
    profile = get_object_or_404(Profile, user=request.user, id=pk)
    if request.method == 'POST':
        form = ProfilePageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or any page you want
    else:
        form = ProfilePageForm(instance=profile)

    return render(request, 'registration/edit_profile_page.html', {'form': form, 'profile' : profile})



def show_profile_page(request, pk):
    page_user = get_object_or_404(Profile, id=pk)
    return render(request, 'registration/user_profile.html', {'page_user': page_user})




@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # Keep the user logged in
            return redirect('password_success')
    else:
        form = PasswordChangingForm(request.user)

    return render(request, 'registration/change-password.html', {'form': form})


def password_success(request):
    return render(request, 'registration/password_success.html', {})


logger = logging.getLogger(__name__)  # Set up logging


def send_activation_email(user, activation_code):  
    if not activation_code:  
        print("❌ Activation code is missing!")  
        raise ValueError("Activation code is missing!")  

    # ✅ Get domain from settings
    domain = "https://www.theinfomall.com"  # Explicitly using www  

    activation_link = f"{domain}{reverse('activate', args=[activation_code])}"  

    print(f"✅ Activation Link: {activation_link}")  

    subject = "Activate Your Account"  

    # ✅ HTML Email Body
    message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <h2>Welcome to The Info Mall 🎉</h2>
        <p>Hi {user.username},</p>
        <p>Click the button below to activate your account:</p>
        <p>
            <a href="{activation_link}" 
               style="display: inline-block; padding: 10px 20px; font-size: 16px; 
                      color: white; background-color: #007bff; text-decoration: none;
                      border-radius: 5px;">
                Activate Account
            </a>
        </p>
        <p>Or copy and paste this link into your browser:</p>
         <p>ignore this email if you didnt make this action:</p>
        <p><a href="{activation_link}">{activation_link}</a></p>
        <p>Thanks for joining us! 🚀</p>
        <p>The Info Mall Team</p>
    </body>
    </html>
    """

    from_email = settings.DEFAULT_FROM_EMAIL  
    recipient_list = [user.email]  

    try:
        send_mail(
            subject, 
            "",  # Empty text body
            from_email, 
            recipient_list, 
            fail_silently=False, 
            html_message=message  # ✅ Sends an HTML email
        )
        print("✅ Activation email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send activation email: {e}")


def user_registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
                return render(request, 'registration/register.html', {'form': form})

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
                return render(request, 'registration/register.html', {'form': form})

            # Create user but set is_active to False
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            # Ensure Profile exists before assigning activation code
            profile, created = Profile.objects.get_or_create(user=user)

            # ✅ Generate and Save Activation Code
            profile.activation_code = str(uuid.uuid4())
            profile.save(update_fields=['activation_code'])  # ✅ Force saving activation code

            print(f"Generated activation code: {profile.activation_code}")  # ✅ Debugging print

            # ✅ Test Reverse URL Before Sending Email
            try:
                activation_url = reverse('activate', args=[str(profile.activation_code)])
                print(f"Activation URL: {activation_url}")
            except Exception as e:
                print(f"Error reversing URL: {e}")

            # ✅ Call send_activation_email with correct values
            send_activation_email(user, profile.activation_code)

            messages.success(request, "Registration successful! Check your email to activate your account.")
            return redirect(reverse_lazy('check_email'))

    else:
        form = SignUpForm()

    return render(request, 'registration/register.html', {'form': form})




def activate_account(request, activation_code):
    print(f"Activation code received: {activation_code}")
    
    try:
        # Find the user with this activation code
        user = User.objects.get(profile__activation_code=activation_code)

        # Activate the user
        user.is_active = True
        user.profile.activation_code = None  # Clear the activation code
        user.save()
        user.profile.save()

        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect(reverse_lazy('login'))

    except User.DoesNotExist:
        messages.error(request, "Invalid activation link or account already activated.")
        return redirect(reverse_lazy('login'))


def user_edit(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page after successful update
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'registration/edit_profile.html', {'form': form})


def check_email(request):
    return render(request, 'registration/check_email.html')




