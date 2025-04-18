from django import forms 
from .models import Post,  Comment, Category, Profile



choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for item in choices:
    choice_list.append(item)


choices = [('sport', 'sport'), ('entertainment', 'entertainment'), ('politics', 'politics'),]

class PostForm(forms.ModelForm):
     class Meta:
        model = Post 
        fields = ('title', 'title_tag','body','category','images')

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'title_tag' : forms.TextInput(attrs={'class' : 'form-control'}),
            #'author' : forms.Select(attrs={'class' : 'form-control'}),
            'category' : forms.Select(choices= choice_list ,attrs={'class' : 'form-control'}),
            'body' : forms.Textarea(attrs={'class' : 'form-control'}),
            'images' : forms.ClearableFileInput(attrs={'class' : 'form-control-file'}),
        }



class EditForm(forms.ModelForm):
     class Meta:
        model = Post 
        fields = ('title', 'title_tag','body')

        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'title_tag' : forms.TextInput(attrs={'class' : 'form-control'}),
            #'author' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'user name'}),
            #'author' : forms.Select(attrs={'class' : 'form-control'}),
            'body' : forms.Textarea(attrs={'class' : 'form-control'}),
        }




class CommentForm(forms.ModelForm):
     class Meta:
        model = Comment 
        fields = ('name','body')

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'body' : forms.Textarea(attrs={'class' : 'form-control'}),
        }        



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']


class CategorForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class' : 'form-control'}),
        }
