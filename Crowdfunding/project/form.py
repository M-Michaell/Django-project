from datetime import datetime
from django.core.exceptions import ValidationError
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField

from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Comment_Report

from django import forms

from project.models import Campaign, Category

class CreateCampaignForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Title",
                "class": "form-control"
            }
        ))
    detail = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Details",
                "class": "form-control",
                'rows': '3'
            }
        ))
    total_target = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Total Target",
                "class": "form-control",
                "type": "number"
            }
        ))
    start_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Start date & time',
                'type': 'date',
                'class': 'form-control'
            }
        ))

    end_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'End date & time',
                'type': 'date',
                'class': 'form-control'
            }
        ))

    class Meta:
        model = Campaign
        fields = ['title', 'detail', 'total_target', 'tags', 'start_date', 'end_date', 'category', 'featured', 'image']


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {}




class Report_form(forms.ModelForm):
    class Meta:
        model=Report
        fields='__all__'
        
class Comment_report_form(forms.ModelForm):
    class Meta:
        model=Comment_Report
        fields='__all__'

        
class Reply_form(forms.ModelForm):
    class Meta:
        model=Reply
        fields='__all__'

        
class Donation_form(forms.ModelForm):
    class Meta:
        model=Donation
        fields='__all__'