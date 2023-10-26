from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from account.models import CustomUser


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True) 
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'phone',
        ]
        # fields = '__all__'



class MyAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
