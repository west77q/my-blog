from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, PasswordChangingForm, ProfilePageForm
from Blog.models import Profile


class CreateProfilePage(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "registration/Create_user_profile_page.html"
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePage(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    form_class = ProfilePageForm
    success_url = reverse_lazy('home')


class ShowProfilePage(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'


    def  get_context_data(self, *args, **kwargs):
         users = Profile.objects.all()
         context = super(ShowProfilePage, self).get_context_data(*args, **kwargs)

         page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

         context["page_user"] =  page_user
         return context





class PasswordsChangeView(PasswordChangeView):
    form_class= PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/password_success.html', {})


class UserRegistration(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
