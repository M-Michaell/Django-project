from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from account.models import CustomUser
import re


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                "id": "id_username",
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                "id": "firstName",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "class": "form-control form-control-lg",
                "id": "lastName",
            }
        )
    )

    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "type": "tel",
                "class": "form-control form-control-lg",
                "id": "phoneNumber",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "class": "form-control form-control-lg",
                "id": "emailAddress",
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control form-control-lg",
                "id": "password1",
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "class": "form-control form-control-lg",
                "id": "password2",
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "phone",
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        regex = r"^01(0|1|2|5)\d{8}$"
        match = re.match(regex, phone)
        print("match: ", match)
        if not match:
            raise forms.ValidationError("Phone number must be Egyptian number")
        return phone


class CustomEditAccountForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control",
            }
        )
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control",
            }
        ),
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control",
            }
        ),
    )

    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Egyption Phone Number",
                "class": "form-control",
            }
        ),
    )

    birthDate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "col-2 d-block"})
    )

    facebookProfile = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Facebook Account",
                "class": "form-control",
            }
        ),
    )

    country = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Country",
                "class": "form-control",
            }
        ),
    )

    image = forms.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone",
            "birthDate",
            "facebookProfile",
            "country",
            "image",
        ]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        regex = r"^01(0|1|2|5)\d{8}$"
        match = re.match(regex, phone)
        print("match: ", match)
        if not match:
            raise forms.ValidationError("Phone number must be Egyptian number")
        return phone


class MyAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "id": "typeEmailX-2",
                "class": "form-control form-control-lg",
            }
        )
    )

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "password",
                "id": "typePasswordX-2",
                "class": "form-control form-control-lg",
            }
        )
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct email and password."
        ),
        "inactive": ("This account is inactive."),
    }


class DeleteForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={"required": "Enter Your Password to Confirm."},
    )
