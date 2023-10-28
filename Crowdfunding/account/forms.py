from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from account.models import CustomUser
import re

class MyUserCreationForm(UserCreationForm):
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
        
        
    def clean_phone(self):

        phone = self.cleaned_data.get('phone')
        regex = r'^01(0|1|2|5)\d{8}$'
        match = re.match(regex, phone)
        print('match: ',match)
        if not match:
            raise forms.ValidationError('Phone number must be Egyptian number')
        return phone


class CustomEditAccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone',
            'birthDate',
            'facebookProfile',
            'country',
            'image'
        ]

    def clean_phone(self):

        phone = self.cleaned_data.get('phone')
        regex = r'^01(0|1|2|5)\d{8}$'
        match = re.match(regex, phone)
        print('match: ',match)
        if not match:
            raise forms.ValidationError('Phone number must be Egyptian number')
        return phone


class MyAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))



class DeleteForm(forms.Form):
        password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Enter Your Password to Confirm.'
        }
    )
