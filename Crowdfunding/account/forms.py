from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from account.models import CustomUser


class MyUserCreationForm(UserCreationForm):

    username = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "Name",
            "class": "form-control"
        }
    ))
    
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        ))
    
    phone = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Egyption Phone Number",
                "class": "form-control"
            }
        ))
    
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    
    
    
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
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control",
                
            }
        ))
    
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
                

            }
        ))
    
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
                

            }
        ))
    
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Egyption Phone Number",
                "class": "form-control",
                

            }
        ))
    
    birthDate = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',  
                'class': 'col-2 d-block'
            }
        )
    )
    
    facebookProfile = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Facebook Account",
                "class": "form-control",
                

            }
        ))
    
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Country",
                "class": "form-control",
            }
        ))
    
    image = forms.FileField(
        required=False
    )
    
    
    
    
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

    error_messages = {
        'invalid_login':(
            "Please enter a correct email and password. Note that both fields may be case-sensitive."
        ),
        'inactive':("This account is inactive."),
    }



class DeleteForm(forms.Form):
        password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Enter Your Password to Confirm.'
        }
    )
