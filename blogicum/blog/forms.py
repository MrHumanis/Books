from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from blog.models import Book, Author, Shelf

User = get_user_model()


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Author
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        widgets = {
            'text': forms.Textarea
        }
        model = Book


class ShelfForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = Shelf
        fields = "__all__"
