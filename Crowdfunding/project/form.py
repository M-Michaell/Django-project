from django import forms
from project.models import Image
# from project.models import Campaign
#
# class CreateModelForm(forms.ModelForm):
#     # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
#
#     class Meta:
#         model = Campaign
#         fields = '__all__'
class CustomizedImageCreationForm(forms.ModelForm):

    class Meta:
        model = Image
        
        fields = '__all__'
