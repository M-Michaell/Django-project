from django import forms
from project.models import Campaign, Category, Tag

class CreateCampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {}
class CreateTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {}