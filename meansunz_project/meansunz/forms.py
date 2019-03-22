from django import forms
from meansunz.models import Post, Category, UserProfile, Comment
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'textForm', 'placeholder': 'PASSWORD'}),
            'username': forms.TextInput(attrs={'class': 'textForm', 'placeholder': 'USERNAME'}),
            'email': forms.EmailInput(attrs={'class': 'textForm', 'placeholder': 'EMAIL'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
        widgets = {
            'picture': forms.FileInput(attrs={}),
        }


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.max_length, help_text="Please enter the category name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=64, help_text="Title")
    description = forms.CharField(max_length=256, required=False, help_text="Text(Optional)")
    picture = forms.ImageField(required=False, help_text="Image(Optional)")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Post

        exclude = ('category', 'user')


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=1026, help_text="Text")
    picture = forms.ImageField(required=False, help_text="Image(Optional)")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Comment
        fields = ('content', 'picture')
