from django import forms
from meansunz.models import Post, Category, UserProfile, Comment
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    # username = forms.CharField(label='')
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'textForm', 'placeholder': 'PASSWORD'}, ),
            'username': forms.TextInput(attrs={'class': 'textForm', 'placeholder': 'USERNAME'}),
            'email': forms.EmailInput(attrs={'class': 'textForm', 'placeholder': 'EMAIL'}),
        }

    # Hide Form Labels
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['email'].label = ''


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password', 'email')
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'textForm', 'placeholder': 'PASSWORD'}),
            'email': forms.EmailInput(attrs={'class': 'textForm', 'placeholder': 'EMAIL'}),
        }

    # Hide Form Labels
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = ''
        self.fields['email'].label = ''


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
        widgets = {
            'picture': forms.FileInput(attrs={}),
        }

    # Hide Form Labels
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['picture'].label = ''


class CategoryForm(forms.ModelForm):
    name = forms.CharField(Category.max_length, widget=forms.TextInput(attrs={'class': 'textForm',
                                                                              'placeholder': 'CATEGORY NAME'}))
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class': 'textForm', 'placeholder': 'TITLE'}))
    description = forms.CharField(max_length=1024, required=False,
                                  widget=forms.Textarea(attrs={'class': 'textArea', 'placeholder': 'DESCRIPTION'}))
    picture = forms.ImageField(required=False, help_text="Choose image (optional)")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    upvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    downvotes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    date = forms.DateTimeField(widget=forms.HiddenInput(), required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Post

        exclude = ('category', 'user')

    # Hide Form Labels
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ''
        self.fields['description'].label = ''
        self.fields['picture'].label = ''

    def clean_picture(self):
        image_file = self.cleaned_data.get('picture')
        accepted_files = ['png', 'gif', 'jpg', 'jpeg', 'bmp', 'wav', 'mp3']
        if image_file:
            if not image_file.name[-3:] in accepted_files:
                raise forms.ValidationError("Only {} files".format(accepted_files))
            if image_file.size > 4194304:
                raise forms.ValidationError("Only files up to 4MB")
        return image_file


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=512, widget=forms.Textarea(attrs={'class': 'textArea',
                                                                                             'placeholder': 'Comment'}))
    picture = forms.ImageField(required=False, help_text="Image(Optional)")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Comment
        fields = ('content', 'picture')

    def clean_picture(self):
        image_file = self.cleaned_data.get('picture')
        accepted_files = ['png', 'gif', 'jpg', 'jpeg', 'bmp', 'wav', 'mp3']
        if image_file:
            if not image_file.name[-3:] in accepted_files:
                raise forms.ValidationError("Only {} files".format(accepted_files))
            if image_file.size > 4194304:
                raise forms.ValidationError("Only files up to 4MB")
        return image_file
