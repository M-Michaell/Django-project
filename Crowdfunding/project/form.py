from django import forms
from project.models import Campaign, Category,Comment,Reply,Rate,Report,Donation,Tag,Image,Comment_Report

#
# class CreateModelForm(forms.ModelForm):
#     # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
#
#     class Meta:
#         model = Campaign
#         fields = '__all__'



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