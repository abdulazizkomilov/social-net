from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User, Comment


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'summary', 'participants', 'like', 'views']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'first_name', 'last_name']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body','parent']
        widgets = {
            'body' : TextInput(),
        }
