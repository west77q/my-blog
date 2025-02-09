from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from Blog.models import Profile


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'snap_url')

        # Define widgets outside the Meta class
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
            'snap_url': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control'}))
    first_name = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class' : 'form-control'}))
    last_name = forms.CharField(max_length=50, widget= forms.TextInput(attrs={'class' : 'form-control'}))

    class meta:
        model = User
        field = ('username','first_name', 'last_name','email','passsword1','password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'




class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=50, widget= forms.PasswordInput(attrs={'class' : 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=50, widget= forms.PasswordInput(attrs={'class' : 'form-control', 'type': 'password'}))

    class meta:
        model = User
        field = ('old_password','new_password1', ' new_password2 ')